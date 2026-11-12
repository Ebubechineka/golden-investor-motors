#!/usr/bin/env python3
"""Generate the Golden Investor Motors static site."""
import os, re, sys, html

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from cars_data import CARS

BRAND = "Golden Investor Motors"
BRAND_UP = "GOLDEN INVESTOR MOTORS"
PHONE_DISPLAY = "+234 816 298 8462"
PHONE_RAW = "2348162988462"
WA = f"https://wa.me/{PHONE_RAW}"
EMAIL = "sales@goldenvistamotors.com"
ADDRESS = "Plot 14, Adeola Odeku Street, Victoria Island, Lagos"
HOURS = "Mon – Sat: 9:00am – 6:30pm · Sun: 1:00pm – 5:00pm"


def money(n):
    return "₦{:,.0f}".format(n)


def e(s):
    return html.escape(str(s), quote=True)


ICON = {
    "cal": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7"><rect x="3" y="5" width="18" height="16" rx="2"/><path d="M8 3v4M16 3v4M3 10h18"/></svg>',
    "road": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7"><path d="M4 21 8 3M20 21 16 3M12 6v3M12 13v3M12 20v1"/></svg>',
    "gear": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7"><path d="M6 4v16M18 4v16M6 9h12M6 15h12"/><circle cx="6" cy="4" r="1.6"/><circle cx="18" cy="4" r="1.6"/></svg>',
    "fuel": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7"><path d="M4 21V5a2 2 0 0 1 2-2h5a2 2 0 0 1 2 2v16M3 21h11M4 9h9M16 8l3 3v7a2 2 0 0 1-4 0v-4h-1"/></svg>',
    "check": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 12.5 9 17.5 20 6.5"/></svg>',
    "shield": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7"><path d="M12 3l7 3v6c0 4.5-3 7.5-7 9-4-1.5-7-4.5-7-9V6l7-3z"/><path d="M9 12l2 2 4-4"/></svg>',
    "doc": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7"><path d="M6 3h8l4 4v14H6z"/><path d="M14 3v4h4M9 12h6M9 16h6"/></svg>',
    "key": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7"><circle cx="8" cy="8" r="4"/><path d="M11 11l9 9M17 17l2-2M14 14l2-2"/></svg>',
    "wa": '<svg viewBox="0 0 24 24"><path d="M17.5 14.4c-.3-.2-1.8-.9-2.1-1-.3-.1-.5-.2-.7.1s-.8 1-.9 1.2c-.2.2-.3.2-.6.1-.3-.2-1.3-.5-2.4-1.5-.9-.8-1.5-1.8-1.6-2.1-.2-.3 0-.4.1-.6l.5-.6c.1-.2.2-.3.3-.5 0-.2 0-.3 0-.5s-.7-1.6-.9-2.2c-.2-.5-.4-.5-.6-.5h-.5c-.2 0-.5.1-.7.4-.2.3-.9.9-.9 2.1s.9 2.4 1 2.6c.1.2 1.7 2.7 4.2 3.7 2.1.8 2.5.7 3 .6.5-.1 1.5-.6 1.7-1.2.2-.6.2-1.1.2-1.2-.1-.2-.2-.2-.5-.4z"/><path d="M12 2C6.5 2 2 6.5 2 12c0 1.8.5 3.4 1.3 4.9L2 22l5.3-1.4c1.4.8 3 1.2 4.7 1.2 5.5 0 10-4.5 10-10S17.5 2 12 2zm0 18.2c-1.5 0-3-.4-4.2-1.2l-.3-.2-3.1.8.8-3-.2-.3C4.2 15 3.8 13.5 3.8 12 3.8 7.5 7.5 3.8 12 3.8s8.2 3.7 8.2 8.2-3.7 8.2-8.2 8.2z"/></svg>',
}

NAV = [("index.html", "Home"), ("inventory.html", "Inventory"), ("about.html", "About"),
       ("contact.html", "Contact")]


def head(title, desc, path, extra=""):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:type" content="website">
<meta property="og:image" content="{path}assets/img/logo.png">
<link rel="icon" href="{path}assets/img/favicon.ico" sizes="any">
<link rel="icon" type="image/png" href="{path}assets/img/favicon-32.png" sizes="32x32">
<link rel="apple-touch-icon" href="{path}assets/img/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;0,700;1,500;1,600&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{path}assets/css/style.css">
{extra}</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
"""


def header(path, active):
    parts = []
    for href, label in NAV:
        cur = ' aria-current="page"' if href == active else ''
        parts.append(f'<a href="{path}{href}"{cur}>{label}</a>')
    links = "".join(parts)
    return f"""<header class="site-header">
  <div class="wrap header-inner">
    <a class="brand" href="{path}index.html" aria-label="{BRAND_UP} — home">
      <span class="brand-mark"><img src="{path}assets/img/logo-mark.png" alt="{BRAND_UP} logo" width="46" height="46"></span>
      <span class="brand-text">
        <span class="brand-name">Golden Investor</span>
        <span class="brand-sub">Motors</span>
      </span>
    </a>
    <nav class="nav" id="nav" aria-label="Main">
      {links}
    </nav>
    <div class="header-cta">
      <a class="btn btn-gold btn-sm" href="{path}inventory.html">Browse inventory</a>
      <button class="nav-toggle" id="navToggle" aria-label="Toggle menu" aria-expanded="false" aria-controls="nav"><span></span></button>
    </div>
  </div>
</header>
<main id="main">
"""


def footer(path):
    return f"""</main>
<footer class="site-footer">
  <div class="wrap footer-grid">
    <div>
      <a class="footer-brand" href="{path}index.html" aria-label="{BRAND_UP} — home">
        <span class="brand-mark"><img src="{path}assets/img/logo-mark.png" alt="{BRAND_UP} logo" width="54" height="54"></span>
        <span class="brand-text">
          <span class="brand-name">Golden Investor</span>
          <span class="brand-sub">Motors</span>
        </span>
      </a>
      <p class="muted" style="font-size:.88rem;max-width:34ch">Carefully sourced, honestly described cars. Every listing is inspected, documented and priced for the Nigerian market.</p>
    </div>
    <div class="footer-col">
      <h4>Explore</h4>
      <ul>
        <li><a href="{path}inventory.html">All inventory</a></li>
        <li><a href="{path}inventory.html?body=SUV">SUVs</a></li>
        <li><a href="{path}inventory.html?body=Sedan">Sedans</a></li>
        <li><a href="{path}inventory.html?body=Pickup">Pickups</a></li>
        <li><a href="{path}about.html">About us</a></li>
      </ul>
    </div>
    <div class="footer-col">
      <h4>Buying</h4>
      <ul>
        <li><a href="{path}contact.html">Book a viewing</a></li>
        <li><a href="{path}contact.html#faq">Common questions</a></li>
        <li><a href="{path}about.html#inspection">Our inspection</a></li>
        <li><a href="{path}contact.html">Trade-in enquiry</a></li>
      </ul>
    </div>
    <div class="footer-col">
      <h4>Visit &amp; contact</h4>
      <ul>
        <li><p>{e(ADDRESS)}</p></li>
        <li><a href="tel:+{PHONE_RAW}">{PHONE_DISPLAY}</a></li>
        <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
        <li><p class="dim" style="font-size:.82rem">{e(HOURS)}</p></li>
      </ul>
    </div>
  </div>
  <div class="wrap footer-bottom">
    <span>© 2026 {BRAND_UP}. All rights reserved.</span>
    <span><a href="{path}inventory.html">Inventory</a> · <a href="{path}contact.html">Contact</a> · <a href="{path}about.html">About</a></span>
  </div>
</footer>
<a class="wa-float" href="{WA}" target="_blank" rel="noopener" aria-label="Chat with us on WhatsApp">{ICON['wa']}</a>
<script src="{path}assets/js/site.js" defer></script>
</body>
</html>
"""


def spec_li(car):
    bits = [f"<li>{ICON['cal']}{car['year']}</li>"]
    if car.get("range_km"):
        bits.append(f"<li>{ICON['road']}{car['range_km']:,} km range</li>")
    elif car.get("power_kw"):
        bits.append(f"<li>{ICON['road']}{int(car['power_kw'])} kW</li>")
    else:
        bits.append(f"<li>{ICON['road']}{e(car['body'])}</li>")
    if car.get("power_kw"):
        bits.append(f"<li>{ICON['gear']}{int(car['power_kw'])} kW</li>")
    else:
        bits.append(f"<li>{ICON['gear']}{e(car['trans'][:4])}.</li>")
    bits.append(f"<li>{ICON['fuel']}{e(car['fuel'])}</li>")
    return '<ul class="car-specs">' + "".join(bits) + "</ul>"


def photo(car, kind="ext", idx=0):
    """Return the image path for a car, falling back gracefully."""
    ph = car.get("photos") or {}
    lst = ph.get(kind) or []
    if idx < len(lst):
        return lst[idx]
    # fall back to the other kind, then to a placeholder
    other = ph.get("int" if kind == "ext" else "ext") or []
    if other:
        return other[0]
    return "assets/img/logo.png"


def src(path, url):
    """Resolve an image reference: absolute URLs stay absolute, local paths get the page prefix."""
    if url.startswith(("http://", "https://", "//", "data:")):
        return url
    return f"{path}{url}"


def car_card(car, path):
    cond = car.get("cond", "Brand New")
    badge = "badge-ok" if cond == "Brand New" else "badge-gold"
    return f"""<article class="car-card">
  <div class="car-media">
    <div class="car-badges"><span class="badge {badge}">{e(cond)}</span></div>
    <a href="{path}cars/{car['id']}.html" aria-label="View {e(car['brand'])} {e(car['model'])}">
      <img src="{src(path, photo(car))}" alt="{e(car['year'])} {e(car['brand'])} {e(car['model'])} in {e(car['color'])}" width="1200" height="750" loading="lazy">
    </a>
  </div>
  <div class="car-body">
    <span class="car-make">{e(car['brand'])} · {e(car['body'])}</span>
    <h3 class="car-title"><a href="{path}cars/{car['id']}.html">{e(car['model'])}</a></h3>
    {spec_li(car)}
    <div class="car-foot">
      <div class="car-price">{money(car['price'])}<small>asking price</small></div>
      <a class="btn btn-ghost btn-sm" href="{path}cars/{car['id']}.html">Details</a>
    </div>
  </div>
</article>"""


# ------------------------------------------------------------------ HOME
def build_home():
    featured = CARS[:6]
    hero_car = CARS[0]
    cats = [
        ("SUV", "SUVs &amp; crossovers", "High-riding, family-ready"),
        ("Sedan", "Sedans", "Comfortable executive driving"),
        ("Hatchback", "Hatchbacks", "City-sized, efficient"),
        ("Minivan", "MPVs &amp; minivans", "Space for the whole family"),
    ]
    cat_html = ""
    for key, label, sub in cats:
        pool = [c for c in CARS if c["body"] == key]
        n = len(pool)
        if not pool:
            continue
        cid = pool[0]["id"]
        cat_html += f"""<a class="cat-tile" href="inventory.html?body={key}">
  <img src="{photo(pool[0])}" alt="{label}" width="1200" height="750" loading="lazy">
  <div class="cat-tile-body">
    <h3>{label}</h3>
    <p>{sub}</p>
    <span class="go">Browse →</span>
  </div>
</a>"""

    featured_html = "".join(car_card(c, "") for c in featured)
    n_total = len(CARS)

    body = f"""
<section class="hero">
  <div class="hero-bg"><img src="{photo(hero_car)}" alt="" width="1200" height="750"></div>
  <div class="wrap hero-inner">
    <div class="hero-grid">
      <div>
        <span class="eyebrow">Victoria Island, Lagos</span>
        <h1 class="display h1">The Chinese car<br>market, <em>curated.</em></h1>
        <p class="lede">A hand-picked collection of Chinese cars — BYD, NIO, XPeng, Zeekr, Li Auto, Changan, GAC Aion, Wuling and more. Every listing carries its real factory specification, exterior and interior photography, and a price in naira.</p>
        <div class="hero-actions">
          <a class="btn btn-gold btn-lg" href="inventory.html">Browse the inventory</a>
          <a class="btn btn-ghost btn-lg" href="contact.html">Book a viewing</a>
        </div>
      </div>
      <div class="hero-card">
        <div class="hero-card-img"><img src="{photo(hero_car)}" alt="{e(hero_car['year'])} {e(hero_car['brand'])} {e(hero_car['model'])}" width="1200" height="750"></div>
        <div class="hero-card-body">
          <span class="hero-card-tag">This week's pick</span>
          <h3>{e(hero_car['year'])} {e(hero_car['brand'])} {e(hero_car['model'])}</h3>
          <p class="muted" style="font-size:.86rem;margin-top:.4rem">{e(hero_car['body'])} · {e(hero_car['fuel'])}{(' · ' + str(hero_car['range_km']) + ' km range') if hero_car.get('range_km') else ''}</p>
          <div class="price">{money(hero_car['price'])}</div>
          <a class="btn btn-gold btn-block" style="margin-top:1.1rem" href="cars/{hero_car['id']}.html">View this car</a>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="sec-head">
      <div>
        <span class="eyebrow">The collection</span>
        <h2 class="display h2">Browse by body style</h2>
      </div>
      <a class="btn btn-ghost btn-sm" href="inventory.html">See everything →</a>
    </div>
    <div class="cat-grid">{cat_html}</div>
  </div>
</section>

<section class="section section-alt">
  <div class="wrap">
    <div class="sec-head">
      <div>
        <span class="eyebrow">Handpicked</span>
        <h2 class="display h2">Featured this month</h2>
      </div>
      <a class="btn btn-ghost btn-sm" href="inventory.html">See everything →</a>
    </div>
    <div class="car-grid">{featured_html}</div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="sec-head">
      <div>
        <span class="eyebrow">Why buy from us</span>
        <h2 class="display h2">Fewer surprises, by design</h2>
      </div>
    </div>
    <div class="trust-grid">
      <div class="trust-card">
        <div class="ico">{ICON['shield']}</div>
        <h3>150-point inspection</h3>
        <p>Battery health, motors, suspension, bodywork and electricals checked by our workshop before a car is listed or handed over.</p>
      </div>
      <div class="trust-card">
        <div class="ico">{ICON['doc']}</div>
        <h3>Full documentation</h3>
        <p>Customs papers, factory specification sheets and ownership documents verified and transferred properly — no shortcuts.</p>
      </div>
      <div class="trust-card">
        <div class="ico">{ICON['key']}</div>
        <h3>7-day exchange</h3>
        <p>If something major surfaces in the first week that we missed, we fix it or exchange the vehicle.</p>
      </div>
      <div class="trust-card">
        <div class="ico">{ICON['wa']}</div>
        <h3>Straight answers</h3>
        <p>Message us on WhatsApp and you speak to someone who has physically seen the car, not a call centre.</p>
      </div>
    </div>
  </div>
</section>

<section class="section section-tight">
  <div class="wrap">
    <div class="cta-band">
      <span class="eyebrow" style="justify-content:center">Ready when you are</span>
      <h2 class="display h2">Come and see it in person</h2>
      <p class="lede">Our showroom is on Adeola Odeku Street, Victoria Island. Walk in, or tell us which car you want to see and we will have it waiting, cleaned and charged.</p>
      <div class="hero-actions">
        <a class="btn btn-gold btn-lg" href="{WA}?text=Hello%20Golden%20Investor%20Motors%2C%20I%27d%20like%20to%20book%20a%20viewing" target="_blank" rel="noopener">Chat on WhatsApp</a>
        <a class="btn btn-ghost btn-lg" href="contact.html">Contact details</a>
      </div>
    </div>
  </div>
</section>
"""
    return head(f"{BRAND_UP} — Chinese Cars in Lagos, Nigeria",
                f"Golden Investor Motors: Chinese cars for sale in Lagos — BYD, NIO, XPeng, Zeekr, Li Auto and more. Real specifications, exterior and interior photos, transparent naira pricing.",
                "") + header("", "index.html") + body + footer("")


# ------------------------------------------------------------------ INVENTORY
def build_inventory():
    cards = "".join(car_card(c, "") for c in CARS)
    makes = sorted({c["brand"] for c in CARS})
    bodies = sorted({c["body"] for c in CARS})
    fuels = sorted({c["fuel"] for c in CARS})
    make_opts = "".join(f'<option value="{e(m)}">{e(m)}</option>' for m in makes)
    body_opts = "".join(f'<option value="{e(b)}">{e(b)}</option>' for b in bodies)
    fuel_opts = "".join(f'<option value="{e(f)}">{e(f)}</option>' for f in fuels)
    n = len(CARS)

    body = f"""
<section class="section" style="padding-bottom:0">
  <div class="wrap">
    <span class="eyebrow">Inventory</span>
    <h1 class="display h1" style="font-size:clamp(2.2rem,4.6vw,3.6rem);margin-top:1rem">Every car we have, in one place</h1>
    <p class="lede" style="margin-top:1rem">Updated as cars arrive and sell. Filter by make, body style, fuel or price.</p>
  </div>
</section>

<section class="section" style="padding-top:2.5rem">
  <div class="wrap">
    <div class="filters" role="search">
      <div class="field">
        <label for="q">Search</label>
        <input id="q" type="search" placeholder="e.g. Seal, ET5, Zeekr…" autocomplete="off">
      </div>
      <div class="field">
        <label for="fMake">Make</label>
        <select id="fMake"><option value="">All makes</option>{make_opts}</select>
      </div>
      <div class="field">
        <label for="fBody">Body</label>
        <select id="fBody"><option value="">All bodies</option>{body_opts}</select>
      </div>
      <div class="field">
        <label for="fFuel">Fuel</label>
        <select id="fFuel"><option value="">All fuels</option>{fuel_opts}</select>
      </div>
      <div class="field">
        <label for="fSort">Sort</label>
        <select id="fSort">
          <option value="featured">Featured</option>
          <option value="price-asc">Price: low to high</option>
          <option value="price-desc">Price: high to low</option>
          <option value="year-desc">Newest first</option>
          <option value="range-desc">Longest range</option>
        </select>
      </div>
    </div>

    <div class="results-bar">
      <p class="results-count" id="count">Showing all vehicles</p>
      <button class="btn btn-dark btn-sm" id="reset" type="button">Clear filters</button>
    </div>

    <div class="car-grid" id="grid">{cards}</div>
    <div class="empty-state" id="empty" hidden>
      <h3>No cars match those filters</h3>
      <p class="muted" style="margin-top:.5rem">Try widening the make or body style, or clear the filters to see everything.</p>
      <button class="btn btn-gold" style="margin-top:1.5rem" id="emptyReset" type="button">Show all vehicles</button>
    </div>
  </div>
</section>
"""
    extra = """<script>
document.addEventListener('DOMContentLoaded', function () {
  var grid = document.getElementById('grid');
  var cards = Array.prototype.slice.call(grid.children);
  var q = document.getElementById('q');
  var fMake = document.getElementById('fMake');
  var fBody = document.getElementById('fBody');
  var fFuel = document.getElementById('fFuel');
  var fSort = document.getElementById('fSort');
  var count = document.getElementById('count');
  var empty = document.getElementById('empty');

  cards.forEach(function (c, i) {
    c.dataset.idx = i;
    var mk = c.querySelector('.car-make').textContent.split('\u00b7');
    c.dataset.make = mk[0].trim();
    c.dataset.body = (mk[1] || '').trim();
    c.dataset.price = c.querySelector('.car-price').textContent.replace(/[^0-9]/g, '');
    c.dataset.title = c.querySelector('.car-title').textContent.toLowerCase();
    var spec = c.querySelectorAll('.car-specs li');
    c.dataset.year = spec[0].textContent.trim();
    var rng = 0;
    for (var k = 0; k < spec.length; k++) {
      var t = spec[k].textContent;
      if (t.indexOf('range') > -1) { rng = parseInt(t.replace(/[^0-9]/g, ''), 10) || 0; }
    }
    c.dataset.range = rng;
    c.dataset.fuel = spec[spec.length - 1].textContent.trim();
  });

  var params = new URLSearchParams(location.search);
  if (params.get('body')) fBody.value = params.get('body');
  if (params.get('make')) fMake.value = params.get('make');
  if (params.get('fuel')) fFuel.value = params.get('fuel');
  if (params.get('q')) q.value = params.get('q');

  function apply() {
    var term = q.value.trim().toLowerCase();
    var make = fMake.value, body = fBody.value, fuel = fFuel.value;
    var shown = 0;
    cards.forEach(function (c) {
      var ok = (!term || c.dataset.title.indexOf(term) > -1 || c.dataset.make.toLowerCase().indexOf(term) > -1)
        && (!make || c.dataset.make === make)
        && (!body || c.dataset.body === body)
        && (!fuel || c.dataset.fuel === fuel);
      c.hidden = !ok;
      if (ok) shown++;
    });
    count.textContent = shown === cards.length ? 'Showing all vehicles' : 'Showing matching vehicles';
    empty.hidden = shown !== 0;
    grid.hidden = shown === 0;
    sort();
  }

  function sort() {
    var v = fSort.value;
    var sorted = cards.slice().sort(function (a, b) {
      if (v === 'price-asc') return a.dataset.price - b.dataset.price;
      if (v === 'price-desc') return b.dataset.price - a.dataset.price;
      if (v === 'year-desc') return b.dataset.year - a.dataset.year;
      if (v === 'range-desc') return b.dataset.range - a.dataset.range;
      return a.dataset.idx - b.dataset.idx;
    });
    sorted.forEach(function (c) { grid.appendChild(c); });
  }

  [q, fMake, fBody, fFuel].forEach(function (el) { el.addEventListener('input', apply); });
  fSort.addEventListener('change', sort);
  function reset() { q.value = ''; fMake.value = ''; fBody.value = ''; fFuel.value = ''; fSort.value = 'featured'; apply(); }
  document.getElementById('reset').addEventListener('click', reset);
  document.getElementById('emptyReset').addEventListener('click', reset);
  apply();
});
</script>"""
    return head(f"All Inventory — {BRAND_UP}",
                f"Browse the Chinese cars in stock at Golden Investor Motors, Lagos. Filter by make, body style, fuel and price.",
                "") + header("", "inventory.html") + body + footer("") + extra


# ------------------------------------------------------------------ DETAIL
def build_detail(car, idx):
    others = [CARS[(idx + n) % len(CARS)] for n in (1, 2, 3)]
    related = "".join(car_card(c, "../") for c in others)
    cond = car.get("cond", "Brand New")
    badge = "badge-ok" if cond == "Brand New" else "badge-gold"
    wa_text = f"https://wa.me/{PHONE_RAW}?text=" + \
        f"I%27m%20interested%20in%20the%20{car['year']}%20{car['brand']}%20{car['model']}%20({car['id']})%20listed%20at%20{money(car['price'])}".replace(" ", "%20")

    ph = car.get("photos") or {}
    ext = ph.get("ext") or []
    inn = ph.get("int") or []
    gallery = [("Exterior", u) for u in ext] + [("Interior", u) for u in inn]
    if not gallery:
        gallery = [("Exterior", "assets/img/logo.png")]

    thumbs = "".join(
        f'<button type="button" class="{"active" if i == 0 else ""}" data-src="{src("../", u)}" aria-label="View {lab} photo {i+1}">'
        f'<img src="{src("../", u)}" alt="{e(car["brand"])} {e(car["model"])} {lab.lower()} photo {i+1}" width="1200" height="750" loading="lazy">'
        f'<span class="thumb-tag">{lab}</span></button>'
        for i, (lab, u) in enumerate(gallery))

    # spec rows — only include what we actually know
    rows = [("Year", str(car["year"])), ("Body", car["body"]), ("Fuel", car["fuel"])]
    if car.get("range_km"): rows.append(("Range", f"{car['range_km']:,} km"))
    if car.get("power_kw"): rows.append(("Power", f"{int(car['power_kw'])} kW"))
    if car.get("battery_kwh"): rows.append(("Battery", f"{car['battery_kwh']:g} kWh"))
    if car.get("length"): rows.append(("Length", f"{car['length']:,} mm"))
    if car.get("width"): rows.append(("Width", f"{car['width']:,} mm"))
    if car.get("height"): rows.append(("Height", f"{car['height']:,} mm"))
    if car.get("wheelbase"): rows.append(("Wheelbase", f"{car['wheelbase']:,} mm"))
    rows.append(("Colour", car["color"]))
    rows.append(("Condition", cond))
    spec_html = "".join(f'<div class="spec-cell"><dt>{e(k)}</dt><dd>{e(v)}</dd></div>' for k, v in rows)

    body = f"""
<div class="wrap">
  <nav class="breadcrumb" aria-label="Breadcrumb">
    <a href="../index.html">Home</a><span>/</span>
    <a href="../inventory.html">Inventory</a><span>/</span>
    <a href="../inventory.html?make={e(car['brand'])}">{e(car['brand'])}</a><span>/</span>
    <span style="color:var(--text-muted)">{e(car['model'])}</span>
  </nav>
</div>

<section style="padding-bottom:4rem">
  <div class="wrap">
    <div class="detail-grid">
      <div>
        <div class="gallery">
          <div class="gallery-main">
            <img id="galleryMain" src="{src("../", gallery[0][1])}" alt="{e(car['year'])} {e(car['brand'])} {e(car['model'])} in {e(car['color'])}" width="1200" height="750">
          </div>
          <div class="gallery-thumbs">{thumbs}</div>
        </div>

        <div style="margin-top:2.5rem">
          <span class="eyebrow">About this car</span>
          <h2 class="display h3" style="margin:1rem 0 1.25rem">{e(car['year'])} {e(car['brand'])} {e(car['model'])}</h2>
          <div class="prose">
            <p>{e(car['desc'])}</p>
            <p>Finished in {e(car['color'])}, this is a {cond.lower()} example supplied with full manufacturer documentation. Every car we list is inspected before handover and comes with our 7-day exchange window on major faults.</p>
          </div>
          <h3 class="display" style="font-size:1.3rem;margin-top:2rem">What you get</h3>
          <ul class="feature-list">
            <li>{ICON['check']}150-point mechanical inspection completed</li>
            <li>{ICON['check']}Full manufacturer specification sheet supplied</li>
            <li>{ICON['check']}Import and customs documents verified</li>
            <li>{ICON['check']}Charging cable and accessories included where applicable</li>
            <li>{ICON['check']}7-day exchange window on major faults</li>
            <li>{ICON['check']}Registration and transfer assistance included</li>
          </ul>
        </div>
      </div>

      <aside class="detail-panel">
        <span class="badge {badge}" style="margin-bottom:1rem;display:inline-block">{e(cond)}</span>
        <h1 class="display" style="font-size:1.9rem;line-height:1.15">{e(car['brand'])} {e(car['model'])}</h1>
        <p class="muted" style="margin-top:.35rem;font-size:.9rem">{e(car['body'])} · {e(car['fuel'])} · {e(car['color'])}</p>
        <div class="detail-price" style="margin-top:1.5rem">{money(car['price'])}<small>Asking price</small></div>

        <dl class="spec-table">{spec_html}</dl>

        <div class="detail-actions">
          <a class="btn btn-gold btn-block btn-lg" href="{wa_text}" target="_blank" rel="noopener">Enquire on WhatsApp</a>
          <a class="btn btn-ghost btn-block" href="../contact.html?car={e(car['id'])}">Book a viewing</a>
          <a class="btn btn-dark btn-block" href="tel:+{PHONE_RAW}">Call {PHONE_DISPLAY}</a>
        </div>

        <ul class="trust-row">
          <li>{ICON['shield']}Inspected</li>
          <li>{ICON['doc']}Documents clear</li>
          <li>{ICON['key']}Test drive available</li>
        </ul>
      </aside>
    </div>
  </div>
</section>

<section class="section" style="background:var(--surface-1);border-block:1px solid var(--line);padding-block:4rem">
  <div class="wrap">
    <div class="sec-head" style="margin-bottom:2rem">
      <div><span class="eyebrow">Keep looking</span><h2 class="display h3" style="margin-top:.8rem">Similar vehicles</h2></div>
      <a class="btn btn-ghost btn-sm" href="../inventory.html">All inventory →</a>
    </div>
    <div class="car-grid">{related}</div>
  </div>
</section>
"""
    return head(f"{car['year']} {car['brand']} {car['model']} — {money(car['price'])} | {BRAND_UP}",
                f"{car['year']} {car['brand']} {car['model']} for sale in Lagos. {car['body']}, {car['fuel']}. {money(car['price'])}.",
                "../") + header("../", "inventory.html") + body + footer("../")


# ------------------------------------------------------------------ ABOUT
def build_about():
    body = f"""
<section class="section" style="padding-bottom:0">
  <div class="wrap">
    <span class="eyebrow">Our story</span>
    <h1 class="display h1" style="font-size:clamp(2.2rem,4.6vw,3.6rem);margin-top:1rem;max-width:18ch">A dealership built on inspection, not sales talk</h1>
    <p class="lede" style="margin-top:1.5rem">Golden Investor Motors exists because buying a used car in Nigeria should not feel like a gamble. We buy carefully, inspect properly, document everything, and describe cars the way we would want them described to us.</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="detail-grid" style="grid-template-columns:1fr 1fr;align-items:center">
      <div class="gallery" style="border-radius:var(--r-lg)">
        <img src="assets/img/cars/gvm-036.jpg" alt="Golden Investor Motors showroom" width="1200" height="750">
      </div>
      <div>
        <span class="eyebrow">How we work</span>
        <h2 class="display h2" style="margin:1rem 0 1.25rem;font-size:2.1rem">Three things we refuse to do</h2>
        <div class="prose">
          <p><strong style="color:var(--text)">Sell a car we have not driven.</strong> Every vehicle goes through our workshop before listing. If a fault cannot be fixed economically, the car does not reach the showroom.</p>
          <p><strong style="color:var(--text)">Describe a car better than it is.</strong> Mileage is verified, condition is stated plainly, and photographs show the actual vehicle. What you read is what you see.</p>
          <p><strong style="color:var(--text)">Rush a handover.</strong> Documents are checked and transferred properly before keys change hands, even when a buyer is in a hurry.</p>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section" id="inspection" style="background:var(--surface-1);border-block:1px solid var(--line)">
  <div class="wrap">
    <span class="eyebrow">The inspection</span>
    <h2 class="display h2" style="margin:1rem 0 2.5rem">What a 150-point check actually covers</h2>
    <div class="trust-grid">
      <div class="trust-card"><div class="ico">{ICON['gear']}</div><h3>Mechanical</h3><p>Engine compression and leaks, gearbox behaviour through all gears, clutch or torque converter, differentials, exhaust integrity.</p></div>
      <div class="trust-card"><div class="ico">{ICON['road']}</div><h3>Chassis &amp; suspension</h3><p>Shock absorbers, bushings, control arms, wheel bearings, steering play, alignment, and a check for accident repair or chassis damage.</p></div>
      <div class="trust-card"><div class="ico">{ICON['shield']}</div><h3>Body &amp; paint</h3><p>Panel alignment, paint depth readings to detect respray, rust in known problem areas, glass, seals and underbody condition.</p></div>
      <div class="trust-card"><div class="ico">{ICON['doc']}</div><h3>Documents &amp; history</h3><p>Customs papers, chassis and engine number match, mileage plausibility, service records, and ownership chain where available.</p></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="cta-band">
      <h2 class="display h2">Talk to someone who has driven the car</h2>
      <p class="lede">Ask about any vehicle in stock and we will tell you what we found — including the things that are not perfect.</p>
      <div class="hero-actions">
        <a class="btn btn-gold btn-lg" href="{WA}" target="_blank" rel="noopener">Message us on WhatsApp</a>
        <a class="btn btn-ghost btn-lg" href="inventory.html">See the inventory</a>
      </div>
    </div>
  </div>
</section>
"""
    return head(f"About — {BRAND_UP}", "How Golden Investor Motors sources, inspects and documents every vehicle it sells in Lagos.",
                "") + header("", "about.html") + body + footer("")


# ------------------------------------------------------------------ CONTACT
def build_contact():
    faqs = [
        ("Can I inspect a car before paying?", "Always. Nothing leaves the lot without a viewing and a test drive. Book a slot and the car will be ready, cleaned and fuelled for you."),
        ("Do you accept trade-ins?", "Yes. Send us photos and the details of your current car on WhatsApp and we will give you a realistic trade-in figure the same day."),
        ("Is the mileage genuine?", "Mileage is checked against service records and plausibility before we list a car. Where history is incomplete, we say so on the listing rather than guessing."),
        ("What documents come with the car?", "Customs papers, proof of ownership and a bill of sale. We assist with registration and transfer at the relevant authority."),
        ("Can I pay in instalments?", "We work with a small number of vetted finance partners. Tell us the car and your preferred deposit and we will confirm what is possible."),
        ("Do you deliver outside Lagos?", "Yes — nationwide, by covered transporter. Delivery is quoted separately based on destination."),
    ]
    faq_html = "".join(f"""<div class="faq-item">
  <button class="faq-q" aria-expanded="false">{e(q)}<span class="plus"></span></button>
  <div class="faq-a"><p>{e(a)}</p></div>
</div>""" for q, a in faqs)

    body = f"""
<section class="section" style="padding-bottom:0">
  <div class="wrap">
    <span class="eyebrow">Get in touch</span>
    <h1 class="display h1" style="font-size:clamp(2.2rem,4.6vw,3.6rem);margin-top:1rem">Let's talk about the car</h1>
    <p class="lede" style="margin-top:1.5rem">Tell us which vehicle you are interested in, or describe what you need and we will point you at the right ones.</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="detail-grid">
      <div>
        <h2 class="display h3" style="margin-bottom:1.5rem">Visit the showroom</h2>
        <dl class="spec-table" style="grid-template-columns:1fr">
          <div class="spec-cell"><dt>Address</dt><dd>{e(ADDRESS)}</dd></div>
          <div class="spec-cell"><dt>Opening hours</dt><dd>{e(HOURS)}</dd></div>
          <div class="spec-cell"><dt>Phone / WhatsApp</dt><dd><a href="tel:+{PHONE_RAW}" style="color:var(--gold-400)">{PHONE_DISPLAY}</a></dd></div>
          <div class="spec-cell"><dt>Email</dt><dd><a href="mailto:{EMAIL}" style="color:var(--gold-400)">{EMAIL}</a></dd></div>
        </dl>
        <div class="gallery" style="margin-top:2rem;border-radius:var(--r-lg)">
          <img src="assets/img/cars/gvm-028.jpg" alt="Golden Investor Motors, Victoria Island" width="1200" height="750">
        </div>
      </div>
      <aside class="detail-panel">
        <h2 class="display" style="font-size:1.5rem">Book a viewing</h2>
        <p class="muted" style="font-size:.88rem;margin-top:.5rem">Fastest way to reach us is WhatsApp — we reply during opening hours.</p>
        <div class="detail-actions">
          <a class="btn btn-gold btn-block btn-lg" href="{WA}?text=Hello%20Golden%20Investor%20Motors%2C%20I%27d%20like%20to%20book%20a%20viewing" target="_blank" rel="noopener">Chat on WhatsApp</a>
          <a class="btn btn-ghost btn-block" href="tel:+{PHONE_RAW}">Call {PHONE_DISPLAY}</a>
          <a class="btn btn-dark btn-block" href="mailto:{EMAIL}?subject=Viewing%20enquiry">Send an email</a>
        </div>
        <ul class="trust-row">
          <li>{ICON['check']}Walk-ins welcome</li>
          <li>{ICON['check']}Test drives available</li>
        </ul>
      </aside>
    </div>
  </div>
</section>

<section class="section" id="faq" style="background:var(--surface-1);border-block:1px solid var(--line)">
  <div class="wrap" style="max-width:900px">
    <span class="eyebrow">Questions</span>
    <h2 class="display h2" style="margin:1rem 0 2rem;font-size:2.1rem">Before you buy</h2>
    <div class="faq">{faq_html}</div>
  </div>
</section>
"""
    return head(f"Contact — {BRAND_UP}", "Contact Golden Investor Motors in Victoria Island, Lagos. WhatsApp, phone, email and showroom details.",
                "") + header("", "contact.html") + body + footer("")


# ------------------------------------------------------------------ JS
SITE_JS = """(function () {
  var t = document.getElementById('navToggle');
  var nav = document.getElementById('nav');
  if (t && nav) {
    t.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      t.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }

  // FAQ accordion
  document.querySelectorAll('.faq-q').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var item = btn.parentElement;
      var open = item.classList.toggle('open');
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  });

  // Reveal on scroll
  var io = 'IntersectionObserver' in window ? new IntersectionObserver(function (entries) {
    entries.forEach(function (en) {
      if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); }
    });
  }, { threshold: 0.08 }) : null;
  document.querySelectorAll('.car-card, .cat-tile, .trust-card, .cta-band').forEach(function (el) {
    el.classList.add('reveal');
    if (io) { io.observe(el); } else { el.classList.add('in'); }
  });
})();
"""


def main():
    os.makedirs(os.path.join(ROOT, "cars"), exist_ok=True)
    os.makedirs(os.path.join(ROOT, "assets", "js"), exist_ok=True)

    files = {
        "index.html": build_home(),
        "inventory.html": build_inventory(),
        "about.html": build_about(),
        "contact.html": build_contact(),
        "assets/js/site.js": SITE_JS,
    }
    for name, content in files.items():
        with open(os.path.join(ROOT, name), "w", encoding="utf-8") as f:
            f.write(content)

    for i, car in enumerate(CARS):
        with open(os.path.join(ROOT, "cars", f"{car['id']}.html"), "w", encoding="utf-8") as f:
            f.write(build_detail(car, i))

    print(f"wrote {len(files)} pages + {len(CARS)} detail pages")


if __name__ == "__main__":
    main()