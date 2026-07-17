"""Emit staging/index.html: the current build with a STAGING banner injected,
so root (production) and /staging/ (work in progress) are never confused."""
import os
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
html=open(os.path.join(ROOT,'index.html')).read()
banner='''<div style="background:#B33A1E;color:#fff;font:600 12px/1.35 system-ui,sans-serif;
  padding:7px 14px;text-align:center;letter-spacing:.02em">
  STAGING &middot; work in progress, may be rough &middot;
  <a href="../" style="color:#fff">the stable version is here &rarr;</a>
</div>'''
# an in-flow strip at the very top, so it pushes the page down and never covers
# the header or the mobile tab bar
i=html.index('<div class="sheet">')
html=html[:i]+banner+html[i:]
html=html.replace('<title>Where To Live / Canada</title>','<title>[STAGING] Where To Live / Canada</title>')
open(os.path.join(ROOT,'staging','index.html'),'w').write(html)
print("staging/index.html written,",round(os.path.getsize(os.path.join(ROOT,'staging','index.html'))/1024),"KB")
