import asyncio
from playwright.async_api import async_playwright

SITE = "file:///workspace/webpages/car-dealership"
OUT = "/workspace/webpages/car-dealership/build/shots"

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for name, rel, full in [("contact", "contact.html", True), ("about", "about.html", True),
                                ("detail2", "cars/gvm-074.html", True)]:
            pg = await b.new_page(viewport={"width": 1440, "height": 900})
            await pg.goto(f"{SITE}/{rel}", wait_until="load", timeout=60000)
            await pg.evaluate("""async () => {
              document.querySelectorAll('img[loading="lazy"]').forEach(i => i.loading='eager');
              await new Promise(r => { let y=0; const s=()=>{ y+=700; window.scrollTo(0,y);
                if (y < document.documentElement.scrollHeight) setTimeout(s,50);
                else { window.scrollTo(0,0); setTimeout(r,900);} }; s(); });
            }""")
            await pg.wait_for_timeout(700)
            await pg.screenshot(path=f"{OUT}/{name}.png", full_page=full)
            print(name, "ok")
            await pg.close()
        await b.close()

asyncio.run(main())
