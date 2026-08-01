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
PAPER = (247, 247, 244)
INK = (23, 25, 29)
INK2 = (88, 93, 101)
INK3 = (139, 144, 152)
SINK = (239, 239, 234)
RULE2 = (199, 201, 194)
WARM = (221, 133, 37)
FIT = [(244, 245, 242), (228, 237, 233), (203, 224, 217), (168, 206, 195), (127, 184, 170)]


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

    img = Image.new('RGB', (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 8], fill=INK)

    fonts = woff2_to_ttf(os.path.join(os.environ.get('OG_CACHE', '/tmp/og-fonts')))
    big = fonts.get('Radio Canada Big') or fonts.get('Radio Canada')
    reg = fonts.get('Radio Canada') or big
    F = lambda path, sz: ImageFont.truetype(path, sz) if path else ImageFont.load_default()

    M = 64
    d.text((M, 74), 'WHERE U BELONG', font=F(reg, 26), fill=INK3)
    d.text((M, 124), 'Where do', font=F(big, 74), fill=INK)
    d.text((M, 206), 'you belong?', font=F(big, 74), fill=INK)
    d.text((M, 320), 'Pick the five things that matter to you.', font=F(reg, 30), fill=INK2)
    d.text((M, 362), 'Rank them. Every town re-sorts against', font=F(reg, 30), fill=INK2)
    d.text((M, 404), 'your answer.', font=F(reg, 30), fill=INK2)

    n = len(data)
    d.text((M, 486), '%s places in %s' % ('{:,}'.format(n), cfg['country']),
           font=F(reg, 30), fill=INK)
    d.text((M, 528), 'ranked on real data, not on a listicle', font=F(reg, 26), fill=INK3)

    # the map, right half, clipped to its box exactly as the share card does: the
    # Canadian sheet is fitted to the inhabited band so the arctic runs off the top
    box_x, box_y, box_w, box_h = 640, 60, W - 640 - 40, H - 120
    k = min(box_w / 1000.0, box_h / mapgeo['height'])
    mw, mh = 1000 * k, mapgeo['height'] * k
    ox, oy = box_x + (box_w - mw) / 2, box_y + (box_h - mh) / 2
    layer = Image.new('RGB', (int(mw) + 2, int(mh) + 2), PAPER)
    ld = ImageDraw.Draw(layer)
    for rings in mapgeo['prov'].values():
        for rg in rings:
            pts = [(px * k, py * k) for px, py in rg]
            if len(pts) > 2:
                ld.polygon(pts, fill=SINK, outline=RULE2)
    for p in data:
        px, py = p['x'] * k, p['y'] * k
        c = FIT[min(4, int((p.get('pop') or 0) > 0) * 2 + 1)]
        ld.ellipse([px - 1.6, py - 1.6, px + 1.6, py + 1.6], fill=c)
    img.paste(layer, (int(ox), int(oy)))

    path = D(out_name)
    img.save(path, 'PNG', optimize=True)
    print('  %-16s %dx%d  %.0f KB' % (out_name, W, H, os.path.getsize(path) / 1024))
    return path


if __name__ == '__main__':
    print('open graph images:')
    build('US', 'index.html', 'og-us.png')
    build('CA', 'canada/index.html', 'og-canada.png')
