
# -*- coding: utf-8 -*-
import urllib.request, json, time
HDRS = {"tokenid": "b06663c4-62df-41b7-9111-6653e6b54592", "Content-Type": "application/json"}
URL = "https://api.fireberry.com/api/v3/query"

all_rows, page = [], 1
while True:
    req = urllib.request.Request(URL,
        data=json.dumps({"objectType": 1039,
            "fields": [{"name":"name"},{"name":"pcfExternalSoftwareID1"},{"name":"pcfAccountid"},{"name":"pcfNeedToPayIncludingVat"},{"name":"pcfStatus"},{"name":"pcfNumberOfPayments"},{"name":"pcfFirstPaymentDate"}],
            "pageSize": 500, "pageNumber": page,
            "filter": [{"type":"and","conditions":[
                {"fieldName":"name","operator":"containsx","value":"x"}]}]}).encode(), headers=HDRS)
    # NOTE: invalid operator used on purpose? NO - remove filter; fetch all 7791? too heavy. 
    # Instead fetch only name-contains 'הוראת הקבע'. v3 filter on name with operator 'eq' won't work; use 'containsx' invalid.
    # Fallback: fetch all pages of 1039 (16 pages) - cheap enough.
    break

all_rows = []
page = 1
while True:
    req = urllib.request.Request(URL,
        data=json.dumps({"objectType": 1039,
            "fields": [{"name":"name"},{"name":"pcfExternalSoftwareID1"},{"name":"pcfAccountid"},{"name":"pcfNeedToPayIncludingVat"},{"name":"pcfStatus"},{"name":"pcfNumberOfPayments"},{"name":"pcfFirstPaymentDate"}],
            "pageSize": 500, "pageNumber": page}).encode(), headers=HDRS)
    for attempt in range(3):
        try:
            r = urllib.request.urlopen(req, timeout=60)
            d = json.loads(r.read()); break
        except Exception:
            if attempt == 2: raise
            time.sleep(2)
    rows = d.get("data", [])
    all_rows.extend(rows)
    print(f"page {page}: +{len(rows)}", flush=True)
    if d.get("isLastPage") or not rows: break
    page += 1
    time.sleep(0.7)

with open(r"C:\Users\sahar\Claude Code\RevitalYaish\_reconciliation\pays_1039_full.json", "w", encoding="utf-8") as f:
    json.dump(all_rows, f, ensure_ascii=False)
print("saved", len(all_rows))
