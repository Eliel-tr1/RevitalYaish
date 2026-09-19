# -*- coding: utf-8 -*-
"""
Reconciliation: GROW (xlsx) vs Old CRM vs New CRM - monthly aggregates.
Outputs: reconciliation_report.json + printed tables.
Read-only across all systems. Run anytime; for future months re-export GROW xlsx.
"""
import json, os, sys
from collections import defaultdict, Counter

BASE = os.path.dirname(os.path.abspath(__file__))

def load(name):
    p = os.path.join(BASE, name)
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else None

def month_of(v):
    return str(v)[:7] if v else None

report = {}

# ---------- 1. GROW (cash truth) ----------
grow = load("grow_transactions.json")
grow_monthly = defaultdict(lambda: {"n_charged": 0, "cash": 0.0, "refunds": 0.0,
                                    "regular": 0, "installments_first": 0, "standing": 0, "refunded": 0})
for t in grow:
    m = month_of(t["charge_date"])
    g = grow_monthly[m]
    st = t["status"]
    amt = t["amount_paid"] or 0
    if st == "זיכוי":
        g["refunded"] += 1
        g["refunds"] += amt  # negative
        continue
    if st == "זוכה":
        # a charge that was later credited - keep in cash but note
        g["n_charged"] += 1
        g["cash"] += amt
        continue
    g["n_charged"] += 1
    g["cash"] += amt
    pt = t["payment_type"]
    if pt == "רגיל": g["regular"] += 1
    elif pt == "תשלומים": g["installments_first"] += 1
    elif pt == 'הו"ק': g["standing"] += 1

report["grow_monthly"] = {m: dict(v) for m, v in sorted(grow_monthly.items())}

# ---------- 2. Old CRM ----------
old = load("old_crm_extract.json") or {}
old_leads = old.get("old_1004_leads", [])
old_pays = old.get("old_1003_payments", [])

old_leads_monthly = Counter(month_of(l.get("createdon")) for l in old_leads)
report["old_leads_monthly"] = {m: old_leads_monthly[m] for m in sorted(old_leads_monthly)}

old_pays_monthly = defaultdict(lambda: {"n": 0, "sum": 0.0})
for p in old_pays:
    m = month_of(p.get("pcfsystemfield113")) or month_of(p.get("createdon"))
    amt = p.get("pcfsystemfield108")
    if amt in (None, "", 0):
        amt = p.get("pcfsystemfield109")
    try: amt = float(amt or 0)
    except: amt = 0.0
    old_pays_monthly[m]["n"] += 1
    old_pays_monthly[m]["sum"] += amt
report["old_payments_monthly"] = {m: dict(v) for m, v in sorted(old_pays_monthly.items())}

# ---------- 3. New CRM ----------
new = load("new_crm_extract.json") or {}
new_leads = new.get("new_1002_leads", [])
new_pays = new.get("new_1039_payments", [])
new_docs = new.get("new_1018_paydocs", [])
new_opps = new.get("new_4_opps", [])

new_leads_monthly = Counter(month_of(l.get("createdon")) for l in new_leads)
report["new_leads_monthly"] = {m: new_leads_monthly[m] for m in sorted(new_leads_monthly)}

# Payments (1039): sale-month = pcfFirstPaymentDate; cash per doc (1018) by pcfPaymentDate
new_sales_monthly = defaultdict(lambda: {"n": 0, "total": 0.0})
for p in new_pays:
    m = month_of(p.get("pcfFirstPaymentDate")) or month_of(p.get("createdon"))
    new_sales_monthly[m]["n"] += 1
    try: new_sales_monthly[m]["total"] += float(p.get("pcfNeedToPayIncludingVat") or 0)
    except: pass
report["new_sales_monthly"] = {m: dict(v) for m, v in sorted(new_sales_monthly.items())}

new_cash_monthly = defaultdict(lambda: {"n": 0, "sum": 0.0})
no_date = 0
for d in new_docs:
    m = month_of(d.get("pcfPaymentDate"))
    if not m:
        no_date += 1
        continue
    new_cash_monthly[m]["n"] += 1
    try: new_cash_monthly[m]["sum"] += float(d.get("pcfPayedIncludingVAT") or 0)
    except: pass
report["new_cash_monthly"] = {m: dict(v) for m, v in sorted(new_cash_monthly.items())}
report["new_cash_docs_without_date"] = no_date

# Opps by status
opp_status = Counter(str(o.get("statuscode")) for o in new_opps)
report["new_opps_by_status"] = dict(opp_status)

# Migration coverage
report["migration"] = {
    "old_leads_total": len(old_leads),
    "old_leads_migrated": sum(1 for l in old_leads if l.get("pcfNewSystemId")),
    "old_pays_total": len(old_pays),
    "old_pays_migrated": sum(1 for p in old_pays if p.get("pcfNewSystemId")),
    "new_pays_total": len(new_pays),
    "new_docs_total": len(new_docs),
}

# ---------- 4. Comparison table ----------
months = sorted(set(report["grow_monthly"]) | set(report["old_payments_monthly"]) | set(report["new_cash_monthly"]))
rows = []
for m in months:
    g = report["grow_monthly"].get(m, {})
    o = report["old_payments_monthly"].get(m, {})
    n_cash = report["new_cash_monthly"].get(m, {})
    n_sales = report["new_sales_monthly"].get(m, {})
    rows.append({
        "month": m,
        "grow_cash": round(g.get("cash", 0)),
        "grow_n": g.get("n_charged", 0),
        "old_pay_n": o.get("n", 0),
        "old_pay_sum": round(o.get("sum", 0)),
        "new_cash_n": n_cash.get("n", 0),
        "new_cash_sum": round(n_cash.get("sum", 0)),
        "new_sales_n": n_sales.get("n", 0),
        "new_sales_total": round(n_sales.get("total", 0)),
        "gap_grow_vs_new_cash": round(g.get("cash", 0) - n_cash.get("sum", 0)),
    })
report["comparison_cash"] = rows

# Leads comparison (only months where old system existed)
lead_rows = []
all_lead_months = sorted(set(report["old_leads_monthly"]) | set(report["new_leads_monthly"]))
for m in all_lead_months:
    lead_rows.append({
        "month": m,
        "old": report["old_leads_monthly"].get(m, 0),
        "new": report["new_leads_monthly"].get(m, 0),
        "gap": report["new_leads_monthly"].get(m, 0) - report["old_leads_monthly"].get(m, 0),
    })
report["comparison_leads"] = lead_rows

with open(os.path.join(BASE, "reconciliation_report.json"), "w", encoding="utf-8") as f:
    json.dump(report, f, ensure_ascii=False, indent=1)

# ---------- Print ----------
print("=== תזרים חודשי: GROW מול ישן מול חדש ===")
print(f"{'חודש':8} {'גרואו כסף':>11} {'ישן כסף':>11} {'חדש תזרים':>11} {'פער גרואו-חדש':>14} {'גרואו n':>8} {'חדש תזרים n':>12}")
for r in rows:
    print(f"{r['month']:8} {r['grow_cash']:>11,} {r['old_pay_sum']:>11,} {r['new_cash_sum']:>11,} {r['gap_grow_vs_new_cash']:>14,} {r['grow_n']:>8} {r['new_cash_n']:>12}")

print("\n=== לידים חודשי: ישן מול חדש (חודשים אחרונים) ===")
for r in lead_rows[-10:]:
    print(f"{r['month']:8} ישן={r['old']:>5}  חדש={r['new']:>5}  פער={r['gap']:>5}")

print("\n=== מיגרציה ===")
for k, v in report["migration"].items():
    print(f"  {k}: {v}")
print("\n=== סטטוסים תהליכי מכירה (חדש) ===")
print(report["new_opps_by_status"])
