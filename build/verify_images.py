import asyncio, json
from playwright.async_api import async_playwright

SITE = "file:///workspace/webpages/car-dealership"
PAGES = ["index.html", "inventory.html", "about.html", "contact.html", "cars/gvm-036.html",
         "cars/gvm-001.html", "cars/gvm-100.html", "cars/gvm-074.html"]

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        total_bad = 0
        for rel in PAGES:
            page = await b.new_page(viewport={"width": 1440, "height": 900})
            await page.goto(f"{SITE}/{rel}", wait_until="load", timeout=60000)
            # force every image (lazy) to load by setting loading=eager and scrolling fully
            res = await page.evaluate("""async () => {
              document.querySelectorAll('img[loading="lazy"]').forEach(i => i.loading = 'eager');
              await new Promise(r => {
                let y = 0;
                const step = () => {
                  y += 600; window.scrollTo(0, y);
                  if (y < document.documentElement.scrollHeight) setTimeout(step, 40);
                  else { window.scrollTo(0,0); setTimeout(r, 900); }
                }; step();
              });
              const imgs = Array.from(document.images);
              const bad = imgs.filter(i => !i.complete || i.naturalWidth === 0)
                              .map(i => i.currentSrc || i.src);
              return { total: imgs.length, bad };
            }""")
            total_bad += len(res["bad"])
            print(f"{rel}: {res['total']} images, {len(res['bad'])} failed")
            for u in res["bad"][:5]:
                print("   FAILED:", u.split("/")[-1])
            await page.close()

        # link integrity
        page = await b.new_page()
        await page.goto(f"{SITE}/inventory.html", wait_until="load")
        hrefs = await page.evaluate("() => Array.from(document.querySelectorAll('a[href]')).map(a => a.getAttribute('href'))")
        print("\nsample hrefs:", sorted(set(hrefs))[:8])
        await page.close()
        await b.close()
        print("\nTOTAL FAILED IMAGES:", total_bad)

asyncio.run(main())
