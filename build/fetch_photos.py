#!/usr/bin/env python3
"""Fetch real car photographs from Wikimedia Commons for each inventory item."""
import json, os, re, sys, time, urllib.parse, urllib.request
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(__file__))
from cars_data import CARS

OUT = os.path.join(os.path.dirname(__file__), "..", "assets", "img", "cars")
os.makedirs(OUT, exist_ok=True)
UA = {"User-Agent": "GoldenVistaMotorsSiteBuilder/1.0 (static site build; contact admin@example.com)"}
API = "https://commons.wikimedia.org/w/api.php"


def api(params):
    url = API + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=45) as r:
        return json.load(r)


def search(term, limit=12):
    try:
        d = api({
            "action": "query", "format": "json", "generator": "search",
            "gsrsearch": f"{term} filetype:bitmap", "gsrnamespace": 6, "gsrlimit": limit,
            "prop": "imageinfo", "iiprop": "url|size|mime|extmetadata", "iiurlwidth": 1400,
        })
    except Exception as e:
        print("  search fail", term, e)
        return []
    pages = d.get("query", {}).get("pages", {})
    out = []
    for p in pages.values():
        ii = p.get("imageinfo", [{}])[0]
        if not ii:
            continue
        w, h = ii.get("width", 0), ii.get("height", 0)
        if ii.get("mime") not in ("image/jpeg", "image/png"):
            continue
        if w < 900 or h < 500:
            continue
        ar = w / h if h else 0
        if ar < 1.15:          # want landscape
            continue
        meta = ii.get("extmetadata", {})
        out.append({
            "title": p["title"],
            "url": ii.get("thumburl") or ii.get("url"),
            "w": w, "h": h, "ar": ar,
            "artist": re.sub("<[^>]+>", "", meta.get("Artist", {}).get("value", "")).strip(),
            "lic": meta.get("LicenseShortName", {}).get("value", ""),
            "page": ii.get("descriptionurl", ""),
        })
    return out


def score(cand, car):
    t = cand["title"].lower()
    s = 0
    make = car["make"].lower().replace("-", " ")
    model = car["model"].lower().replace("-", " ")
    if make.split()[0] in t:
        s += 6
    # model tokens
    toks = [x for x in re.split(r"[^a-z0-9]+", model) if len(x) > 1]
    for tok in toks:
        if tok in t:
            s += 4
    if str(car["year"]) in t:
        s += 3
    if "interior" in t or "engine" in t or "dashboard" in t or "logo" in t or "badge" in t:
        s -= 8
    if "rear" in t or "back" in t:
        s -= 1
    s += min(cand["ar"], 1.9) * 1.5
    s += min(cand["w"], 2000) / 2000
    return s


def fetch(car):
    cid = car["id"]
    dest = os.path.join(OUT, f"{cid}.jpg")
    if os.path.exists(dest) and os.path.getsize(dest) > 20000:
        return cid, "cached", None
    cands = []
    for term in car["q"]:
        cands += search(term)
        if len(cands) >= 8:
            break
    if not cands:
        return cid, "NO_CANDIDATES", None
    # dedupe
    seen, uniq = set(), []
    for c in cands:
        if c["title"] in seen:
            continue
        seen.add(c["title"])
        uniq.append(c)
    uniq.sort(key=lambda c: score(c, car), reverse=True)
    for c in uniq[:4]:
        try:
            req = urllib.request.Request(c["url"], headers=UA)
            with urllib.request.urlopen(req, timeout=60) as r:
                data = r.read()
            if len(data) < 20000:
                continue
            with open(dest, "wb") as f:
                f.write(data)
            return cid, "ok", c
        except Exception as e:
            print("  dl fail", cid, e)
            continue
    return cid, "ALL_DOWNLOADS_FAILED", None


def main():
    results = {}
    with ThreadPoolExecutor(max_workers=6) as ex:
        for cid, status, meta in ex.map(fetch, CARS):
            results[cid] = {"status": status, "meta": meta}
            print(f"{cid} {status} {meta['title'] if meta else ''}")
    with open(os.path.join(os.path.dirname(__file__), "photo_credits.json"), "w") as f:
        json.dump(results, f, indent=1)
    bad = [k for k, v in results.items() if v["status"] not in ("ok", "cached")]
    print("\nFAILED:", bad)


if __name__ == "__main__":
    main()
