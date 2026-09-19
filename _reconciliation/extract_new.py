
import urllib.request, json, time

HDRS = {"tokenid": "b06663c4-62df-41b7-9111-6653e6b54592", "Content-Type": "application/json"}
URL = "https://api.fireberry.com/api/v3/query"

def fetch_all(object_type, fields, name, flt=None):
    all_rows, page = [], 1
    while True:
        body = {"objectType": object_type, "fields": [{"name": f} for f in fields],
                "pageSize": 500, "pageNumber": page}
        if flt: body["filter"] = flt
        req = urllib.request.Request(URL, data=json.dumps(body).encode(), headers=HDRS)
        for attempt in range(3):
            try:
                r = urllib.request.urlopen(req, timeout=60)
                d = json.loads(r.read()); break
            except Exception:
                if attempt == 2: raise
                time.sleep(2)
        rows = d.get("data", [])
        all_rows.extend(rows)
        if d.get("isLastPage") or not rows: break
        page += 1
        time.sleep(0.7)
    print(f"{name}: {len(all_rows)} rows, {page} pages", flush=True)
    return all_rows

out = {}
out["new_1002_leads"] = fetch_all(1002, ["name", "createdon", "pcfMarketingRecordType", "pcfMarketingRecordTypename"], "new 1002")
time.sleep(1)
out["new_1039_payments"] = fetch_all(1039, ["name", "createdon", "pcfNeedToPayIncludingVat", "pcfFirstPaymentDate", "pcfNumberOfPayments", "pcfStatus", "pcfStatusname", "pcfExternalSoftwareID1", "pcfPaymentType"], "new 1039")
time.sleep(1)
out["new_1018_paydocs"] = fetch_all(1018, ["name", "createdon", "pcfPayedIncludingVAT", "pcfPaymentDate", "pcfPaymetStatus", "pcfPaymetStatusname"], "new 1018")
time.sleep(1)
out["new_4_opps"] = fetch_all(4, ["name", "createdon", "statuscode", "pcfincomingcashflow"], "new 4")

with open(r"C:\Users\sahar\Claude Code\RevitalYaish\_reconciliation\new_crm_extract.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False)
print("saved", flush=True)
