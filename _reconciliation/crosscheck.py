# -*- coding: utf-8 -*-
import json
from collections import defaultdict
from datetime import datetime, date

CAT = {  # product categorycode -> sale category
 "100": "בוסט", "101": "פרימיום", "102": "ליווי",
}
# per-product name fallback
def cat_of(row):
    prod = row.get("pcfProductname")
    if not prod: return None
    if prod == "סדנה בוסט" or prod == "הרצאת אורח": return "בוסט"
    if prod.startswith("תוכנית ליווי"): return "פרימיום"
    if prod.startswith("תוכנית המשך") or prod == "הו\"ק טסט": return "ליווי"
    return None

opps = json.load(open("obj4_all.json", encoding="utf-8"))
coach = json.load(open("obj1051_all.json", encoding="utf-8"))

# coaching active per account: any 1051 record with pcfStatus in active set
ACTIVE_COACH = {"1", "2", "4", "5"}   # קליטה/בתהליך/הקפאה/בתהליך ביטול - still running
ENDED_COACH = {"3", "6", "7", "8"}
coach_active = defaultdict(lambda: None)  # accountid -> True/False/None
for c in coach:
    acc = c.get("pcfaccountid")
    if not acc: continue
    st = str(c.get("pcfStatus"))
    if st in ACTIVE_COACH: coach_active[acc] = True
    elif coach_active.get(acc) is not True: coach_active[acc] = False

by_acc = defaultdict(list)
for o in opps:
    acc = o.get("accountid")
    if not acc: continue
    o["_cat"] = cat_of(o)
    by_acc[acc].append(o)

def parse_dt(s):
    if not s: return None
    return datetime.fromisoformat(s.replace("Z","+00:00"))

WON = "11"
violations = []
stats = defaultdict(int)
for acc, sales in by_acc.items():
    active = coach_active.get(acc)  # True/False/None
    closed_cats_seen = set()
    sales.sort(key=lambda r: parse_dt(r.get("createdon")) or datetime.min.replace(tzinfo=None))
    has_closed = defaultdict(bool)
    for s in sales:
        cat, st = s["_cat"], str(s.get("statuscode"))
        if cat is None:
            # rule 4: no-category sale while boost+premium+coaching all closed and coaching active
            if {"בוסט","פרימיום","ליווי"} <= set(c for c,v in has_closed.items() if v) and active:
                violations.append((acc, s, "תהליך בלי מוצר כשבוסט+פרימיום+ליווי סגורים והליווי פעיל"))
            stats["no_cat"] += 1
            continue
        if has_closed[cat]:
            # previous same-category closed; new one valid only if coaching not active
            if active:
                violations.append((acc, s, f"{cat} נוסף כשכבר נסגר {cat} קודם והליווי עדיין פעיל"))
        if st == WON:
            has_closed[cat] = True

print("accounts:", len(by_acc))
print("coaching active:", sum(1 for v in coach_active.values() if v), "| ended:", sum(1 for v in coach_active.values() if v is False))
print("no-cat sales:", stats["no_cat"])
print("violations:", len(violations))
json.dump([{"account":a,"sale_id":s.get("_id"),"name":s.get("name"),"cat":s["_cat"],"status":s.get("statuscode"),"createdon":s.get("createdon"),"reason":r} for a,s,r in violations],
          open("violations.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
