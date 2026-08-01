#!/usr/bin/env python3
"""Generate the Open Graph preview image for each country.

Why this exists: the app had og:title and og:description but no og:image, and Meta
will not render a preview card without one, so every link shared anywhere previewed
as a bare grey text row.

Why it is a STATIC image per country rather than per result: the entire answer lives
in the URL fragment, and RFC 3986 sec 3.5 says the fragment is separated from the URI
before dereference and never reaches the server. GitHub Pages has no request-time
runtime. So a crawler asking for this page cannot be told which result to draw. One
honest generic image per country is the answer; per-city static stubs would be the
upgrade, and that is thousands of files.

Run: python3 src/build_og.py     (needs the scratchpad venv for woff2 decoding)
Output: og-us.png, og-canada.png at 1200x630, the ratio Meta and Vercel both document.
"""
import base64, io, json, math, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = lambda *p: os.path.join(ROOT, *p)

from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 630
# Hardiness Zone world: printed ink ground, stock type, five zone bands
INK    = (11, 42, 33)
INK2   = (18, 53, 40)
STOCK  = (244, 235, 212)
ONINK2 = (175, 200, 184)
ONINK3 = (134, 164, 146)
SIGNAL = (233, 185, 73)
FIT    = [(51, 80, 122), (60, 127, 140), (111, 162, 74), (217, 162, 27), (214, 70, 28)]
PAPER, SINK, RULE2, INK3, WARM = INK, INK2, INK2, ONINK3, SIGNAL


def woff2_to_ttf(cache_dir):
    """Pull the two faces out of fonts/faces.css and convert them. They are inlined
    as base64 woff2 because the app ships as one self-contained file."""
    os.makedirs(cache_dir, exist_ok=True)
    css = open(D('fonts/faces.css')).read()
    out = {}
    # Each family ships TWO subsets: Latin Extended (U+0100-02BA...) and basic Latin
    # (U+0000-00FF). Taking the first block per family grabbed the extended one,
    # which contains no ASCII at all, and every character rendered as a tofu box.
    # Match on the unicode-range instead of on order.
    blocks = re.findall(r"font-family:'([^']+)'.*?base64,([A-Za-z0-9+/=]+)\)[^}]*?unicode-range:([^;]+);", css, re.S)
    for fam, b64, urange in blocks:
        if 'U+0000-00FF' not in urange.replace(' ', '').upper():
            continue                      # not the block with the alphabet in it
        path = os.path.join(cache_dir, fam.replace(' ', '_') + '.ttf')
        if fam in out:
            continue
        try:
            from fontTools.ttLib import TTFont
            f = TTFont(io.BytesIO(base64.b64decode(b64)))
            f.flavor = None
            f.save(path)
            out[fam] = path
        except Exception as e:
            print('  could not convert %s: %s' % (fam, e))
    return out


def load(p, default=None):
    try:
        with open(D(p)) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return default


def build(cc, page, out_name):
    """page is the built html we read DATA and MAPGEO back out of, so the image can
    never drift from what the app actually ships."""
    html = open(D(page)).read()
    data = json.loads(re.search(r'const DATA=(\[.*?\]);const MAPGEO', html, re.S).group(1))
    mapgeo = json.loads(re.search(r';const MAPGEO=(\{.*?\});</script>', html, re.S).group(1))
    cfg = json.loads(re.search(r'const CFG=(\{.*?\});const DATA=', html, re.S).group(1))

    img = Image.new('RGB', (W, H), INK)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 14], fill=SIGNAL)

    fonts = woff2_to_ttf(os.path.join(os.environ.get('OG_CACHE', '/tmp/og-fonts')))
    big = fonts.get('Radio Canada Big') or fonts.get('Radio Canada')
    reg = fonts.get('Radio Canada') or big
    F = lambda path, sz: ImageFont.truetype(path, sz) if path else ImageFont.load_default()

    M = 64
    d.text((M, 76), 'WHERE U BELONG', font=F(reg, 26), fill=SIGNAL)
    d.text((M, 126), 'WHERE DO', font=F(big, 82), fill=STOCK)
    d.text((M, 214), 'YOU BELONG?', font=F(big, 82), fill=STOCK)
    d.text((M, 336), 'Pick the five things that matter to you.', font=F(reg, 30), fill=ONINK2)
    d.text((M, 378), 'Rank them. Every town re-sorts against', font=F(reg, 30), fill=ONINK2)
    d.text((M, 420), 'your answer.', font=F(reg, 30), fill=ONINK2)

    n = len(data)
    d.text((M, 494), '%s places in %s' % ('{:,}'.format(n), cfg['country']),
           font=F(reg, 30), fill=STOCK)
    d.text((M, 536), 'ranked on real data, not on a listicle', font=F(reg, 26), fill=ONINK3)

    # the map, right half, clipped to its box exactly as the share card does: the
    # Canadian sheet is fitted to the inhabited band so the arctic runs off the top
    box_x, box_y, box_w, box_h = 640, 60, W - 640 - 40, H - 120
    k = min(box_w / 1000.0, box_h / mapgeo['height'])
    mw, mh = 1000 * k, mapgeo['height'] * k
    ox, oy = box_x + (box_w - mw) / 2, box_y + (box_h - mh) / 2
    # the same zone flood the app draws: nearest place wins each cell, so the
    # preview is the product's own map rather than a decorative outline
    lw, lh = int(mw) + 2, int(mh) + 2
    layer = Image.new('RGB', (lw, lh), INK)
    mask = Image.new('L', (lw, lh), 0)
    md = ImageDraw.Draw(mask)
    for rings in mapgeo['prov'].values():
        for rg in rings:
            pts = [(px * k, py * k) for px, py in rg]
            if len(pts) > 2:
                md.polygon(pts, fill=255)
    # coarse nearest-place field, then paste through the country mask
    STEP = 3
    pxs = [(p['x'] * k, p['y'] * k, i) for i, p in enumerate(data)]
    band = [FIT[min(4, i * 5 // max(1, len(data)))] for i in range(len(data))]
    from math import inf
    buckets = {}
    for bxp, byp, i in pxs:
        buckets.setdefault((int(bxp // 40), int(byp // 40)), []).append((bxp, byp, i))
    ld = ImageDraw.Draw(layer)
    for yy in range(0, lh, STEP):
        for xx in range(0, lw, STEP):
            bb, bd = None, inf
            for r in range(0, 5):
                for by in range(int(yy // 40) - r, int(yy // 40) + r + 1):
                    for bx in range(int(xx // 40) - r, int(xx // 40) + r + 1):
                        for (bxp, byp, i) in buckets.get((bx, by), ()):
                            dd = (bxp - xx) ** 2 + (byp - yy) ** 2
                            if dd < bd: bd, bb = dd, i
                if bb is not None and r: break
            if bb is None: continue
            ld.rectangle([xx, yy, xx + STEP, yy + STEP], fill=band[bb])
    img.paste(layer, (int(ox), int(oy)), mask)

    path = D(out_name)
    img.save(path, 'PNG', optimize=True)
    print('  %-16s %dx%d  %.0f KB' % (out_name, W, H, os.path.getsize(path) / 1024))
    return path


if __name__ == '__main__':
    print('open graph images:')
    build('US', 'index.html', 'og-us.png')
    build('CA', 'canada/index.html', 'og-canada.png')
