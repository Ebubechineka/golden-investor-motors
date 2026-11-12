import os, re, glob, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
pages = ["index.html", "inventory.html", "about.html", "contact.html"] + \
        [os.path.relpath(p, ROOT) for p in sorted(glob.glob(f"{ROOT}/cars/*.html"))]

# ---------- 1. internal link integrity ----------
broken = []
checked = 0
for rel in pages:
    base = os.path.dirname(os.path.join(ROOT, rel))
    html = open(os.path.join(ROOT, rel), encoding="utf-8").read()
    for href in re.findall(r'href="([^"]+)"', html):
        if href.startswith(("http", "mailto:", "tel:", "#", "data:")):
            continue
        target = href.split("#")[0].split("?")[0]
        if not target:
            continue
        checked += 1
        if not os.path.exists(os.path.normpath(os.path.join(base, target))):
            broken.append((rel, href))
print(f"internal links checked: {checked}")
print(f"BROKEN LINKS: {len(broken)}")
for b in broken[:10]:
    print("   ", b)

# ---------- 2. placeholder / lorem scan ----------
BAD = ["lorem", "ipsum", "placeholder", "TODO", "FIXME", "xxx", "coming soon",
       "sample text", "dummy", "your text here", "insert ", "tbd", "undefined", "null,"]
hits = []
for rel in pages:
    txt = open(os.path.join(ROOT, rel), encoding="utf-8").read().lower()
    for b in BAD:
        if b in txt:
            for m in re.finditer(re.escape(b), txt):
                hits.append((rel, b, txt[max(0, m.start()-45):m.start()+45].replace("\n", " ")))
print(f"\nplaceholder hits: {len(hits)}")
for h in hits[:12]:
    print("   ", h)

# ---------- 3. brand + contact consistency ----------
brand_ok = 0
for rel in pages:
    txt = open(os.path.join(ROOT, rel), encoding="utf-8").read()
    if "Golden Investor" in txt and "logo-mark.png" in txt and "favicon" in txt:
        brand_ok += 1
print(f"\npages with brand name + logo + favicon: {brand_ok}/{len(pages)}")

# ---------- 4. every car has price + description + photo ----------
import sys
sys.path.insert(0, f"{ROOT}/build")
from cars_data import CARS
issues = []
for c in CARS:
    if not c["desc"] or len(c["desc"]) < 80:
        issues.append((c["id"], "short desc"))
    if not c["price"] or c["price"] < 1_000_000:
        issues.append((c["id"], "bad price"))
    if not os.path.exists(f"{ROOT}/assets/img/cars/{c['id']}.jpg"):
        issues.append((c["id"], "missing photo"))
    if not os.path.exists(f"{ROOT}/cars/{c['id']}.html"):
        issues.append((c["id"], "missing page"))
print(f"cars: {len(CARS)}  data issues: {len(issues)}")
for i in issues[:10]:
    print("   ", i)

# ---------- 5. price range sanity ----------
prices = [c["price"] for c in CARS]
print(f"\nprice range: N{min(prices):,} – N{max(prices):,}")
print(f"makes: {len(set(c['brand'] for c in CARS))}  bodies: {sorted(set(c['body'] for c in CARS))}")
print(f"conditions: {sorted(set(c.get('cond','Brand New') for c in CARS))}")
