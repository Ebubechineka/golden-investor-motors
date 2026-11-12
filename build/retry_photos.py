#!/usr/bin/env python3
"""Retry failed photo fetches sequentially with backoff."""
import json, os, sys, time
sys.path.insert(0, os.path.dirname(__file__))
from cars_data import CARS
import fetch_photos as fp

credits_path = os.path.join(os.path.dirname(__file__), "photo_credits.json")
credits = json.load(open(credits_path))
todo = [c for c in CARS if credits.get(c["id"], {}).get("status") not in ("ok", "cached")]
print("retrying", len(todo), "cars")

for i, car in enumerate(todo, 1):
    cid = car["id"]
    for attempt in range(4):
        cid2, status, meta = fp.fetch(car)
        if status in ("ok", "cached"):
            credits[cid] = {"status": status, "meta": meta}
            print(f"[{i}/{len(todo)}] {cid} OK {meta['title'] if meta else ''}", flush=True)
            break
        wait = 6 * (attempt + 1)
        print(f"[{i}/{len(todo)}] {cid} {status} attempt {attempt+1}, waiting {wait}s", flush=True)
        time.sleep(wait)
    else:
        credits[cid] = {"status": "FAILED", "meta": None}
        print(f"[{i}/{len(todo)}] {cid} GAVE UP", flush=True)
    json.dump(credits, open(credits_path, "w"), indent=1)
    time.sleep(2)

bad = [k for k, v in credits.items() if v["status"] not in ("ok", "cached")]
print("\nSTILL FAILED:", bad)
