import asyncio, os, sys, json
from playwright.async_api import async_playwright

SITE = "file:///workspace/webpages/car-dealership"
OUT = "/workspace/webpages/car-dealership/build/shots"
os.makedirs(OUT, exist_ok=True)

PAGES = [
    ("home", f"{SITE}/index.html", 1440, 900, True),
    ("inventory", f"{SITE}/inventory.html", 1440, 900, True),
    ("detail", f"{SITE}/cars/gvm-036.html", 1440, 900, True),
    ("contact", f"{SITE}/contact.html", 1440, 900, False),
    ("about", f"{SITE}/about.html", 1440, 900, False),
    ("mobile-home", f"{SITE}/index.html", 390, 844, True),
    ("mobile-inv", f"{SITE}/inventory.html", 390, 844, False),
]

async def main():
    report = {}
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for name, url, w, h, full in PAGES:
            page = await b.new_page(viewport={"width": w, "height": h}, device_scale_factor=1)
            errors = []
            page.on("console", lambda m: errors.append(f"console:{m.type}:{m.text}") if m.type == "error" else None)
            page.on("pageerror", lambda e: errors.append(f"pageerror:{e}"))
            failed = []
            page.on("requestfailed", lambda r: failed.append(r.url) if not r.url.startswith("data:") else None)
            await page.goto(url, wait_until="networkidle", timeout=60000)
            await page.wait_for_timeout(1200)
            # scroll to trigger reveals
            await page.evaluate("""async () => {
              await new Promise(res => {
                let y = 0; const step = () => {
                  y += 700; window.scrollTo(0, y);
                  if (y < document.body.scrollHeight) setTimeout(step, 60); else { window.scrollTo(0,0); setTimeout(res, 300); }
                }; step();
              });
            }""")
            await page.wait_for_timeout(600)
            await page.screenshot(path=f"{OUT}/{name}.png", full_page=full)
            broken = await page.evaluate("""() => Array.from(document.images)
                .filter(i => !i.complete || i.naturalWidth === 0)
                .map(i => i.currentSrc || i.src)""")
            counts = await page.evaluate("""() => ({
                imgs: document.images.length,
                cards: document.querySelectorAll('.car-card').length,
                h1: (document.querySelector('h1')||{}).textContent || '',
                scrollW: document.documentElement.scrollWidth,
                clientW: document.documentElement.clientWidth
            })""")
            report[name] = {"broken": broken, "errors": errors, "failed_requests": failed, **counts}
            print(name, json.dumps(report[name], indent=1)[:900], flush=True)
            await page.close()
        await b.close()
    json.dump(report, open(f"{OUT}/report.json", "w"), indent=1)
    print("\nSUMMARY")
    for k, v in report.items():
        print(f"{k}: imgs={v['imgs']} cards={v['cards']} broken={len(v['broken'])} errors={len(v['errors'])} overflow={'YES' if v['scrollW']>v['clientW']+2 else 'no'}")

asyncio.run(main())
