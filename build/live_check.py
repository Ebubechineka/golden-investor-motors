import asyncio, json
from playwright.async_api import async_playwright

BASE = "https://static.teamily.ai/sites/04d8d422-16a7-4609-8892-022dcc1cd463/webpages/car-dealership"

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        results = {}
        for name, url in [("home", f"{BASE}/index.html"),
                          ("inventory", f"{BASE}/inventory.html"),
                          ("detail", f"{BASE}/cars/gvm-036.html"),
                          ("detail2", f"{BASE}/cars/gvm-074.html"),
                          ("about", f"{BASE}/about.html"),
                          ("contact", f"{BASE}/contact.html")]:
            pg = await b.new_page(viewport={"width": 1440, "height": 900})
            resp = await pg.goto(url, wait_until="load", timeout=90000)
            await pg.wait_for_timeout(1500)
            r = await pg.evaluate("""async () => {
              document.querySelectorAll('img[loading="lazy"]').forEach(i => i.loading='eager');
              await new Promise(res => { let y=0; const s=()=>{ y+=700; window.scrollTo(0,y);
                if (y < document.documentElement.scrollHeight) setTimeout(s,50);
                else { window.scrollTo(0,0); setTimeout(res,1200);} }; s(); });
              const imgs = Array.from(document.images);
              return {
                imgs: imgs.length,
                broken: imgs.filter(i => !i.complete || i.naturalWidth===0).map(i=>i.src.split('/').pop()),
                h1: (document.querySelector('h1')||{}).textContent||'',
                cards: document.querySelectorAll('.car-card').length,
                cssLoaded: getComputedStyle(document.body).backgroundColor
              };
            }""")
            results[name] = {"status": resp.status if resp else None, **r}
            print(f"{name}: HTTP {resp.status if resp else '?'} | imgs={r['imgs']} broken={len(r['broken'])} cards={r['cards']} bg={r['cssLoaded']}")
            if r["broken"]:
                print("   BROKEN:", r["broken"][:6])
            await pg.close()
        await b.close()
        json.dump(results, open("/workspace/webpages/car-dealership/build/live_check.json","w"), indent=1)

asyncio.run(main())
