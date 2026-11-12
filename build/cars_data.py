# Golden Investor Motors — inventory dataset (Chinese market)
# Generated from real manufacturer specifications. Each entry:
# id, brand, model, body, fuel, year, price (NGN), range_km, power_kw,
# battery_kwh, length, width, height, wheelbase, color, desc, photos
import json, os

_HERE = os.path.dirname(os.path.abspath(__file__))
_DATA = os.path.join(_HERE, "catalog.json")

with open(_DATA, encoding="utf-8") as _f:
    CARS = json.load(_f)

# normalise keys used by the templates
for _c in CARS:
    _c.setdefault("trim", "")
    _c.setdefault("mileage", 0)
    _c.setdefault("trans", "Automatic")
    _c.setdefault("cond", "Brand New")
    _c.setdefault("photos", {"ext": [], "int": []})
