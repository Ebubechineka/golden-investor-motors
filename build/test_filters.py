import asyncio
from playwright.async_api import async_playwright

async def m():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 1440, "height": 900})
        await pg.goto("file:///workspace/webpages/car-dealership/inventory.html", wait_until="load")
        await pg.wait_for_timeout(800)
        r = await pg.evaluate("""() => {
          const f = document.querySelector('.filters');
          const cs = f ? getComputedStyle(f) : null;
          return {
            exists: !!f,
            display: cs && cs.display,
            height: f && Math.round(f.getBoundingClientRect().height),
            selects: document.querySelectorAll('.filters select').length,
            count: document.getElementById('count').textContent
          };
        }""")
        print("filters:", r)

        await pg.select_option("#fBody", "SUV")
        await pg.wait_for_timeout(400)
        r2 = await pg.evaluate("""() => ({
          count: document.getElementById('count').textContent,
          visible: Array.from(document.querySelectorAll('.car-card')).filter(c => !c.hidden).length
        })""")
        print("after SUV filter:", r2)

        await pg.fill("#q", "prado")
        await pg.wait_for_timeout(400)
        r3 = await pg.evaluate("""() => ({
          count: document.getElementById('count').textContent,
          titles: Array.from(document.querySelectorAll('.car-card')).filter(c => !c.hidden)
                    .map(c => c.querySelector('.car-title').textContent.trim())
        })""")
        print("after search 'prado':", r3)

        await pg.fill("#q", "zzzz")
        await pg.wait_for_timeout(400)
        r4 = await pg.evaluate("""() => ({
          count: document.getElementById('count').textContent,
          emptyShown: !document.getElementById('empty').hidden
        })""")
        print("after no-match search:", r4)

        # sort check
        await pg.fill("#q", "")
        await pg.select_option("#fBody", "")
        await pg.select_option("#fSort", "price-asc")
        await pg.wait_for_timeout(400)
        r5 = await pg.evaluate("""() => Array.from(document.querySelectorAll('.car-card')).slice(0,3)
              .map(c => c.querySelector('.car-price').textContent.replace(/[^0-9]/g,''))""")
        print("first 3 prices after price-asc:", r5)

        await b.close()

asyncio.run(m())
