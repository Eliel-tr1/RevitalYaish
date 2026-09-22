
import urllib.request, json, time
HDRS = {"tokenid": "b06663c4-62df-41b7-9111-6653e6b54592", "Content-Type": "application/json"}
URL = "https://api.fireberry.com/api/v3/query"
all_rows, page = [], 1
while True:
    req = urllib.request.Request(URL,
        data=json.dumps({"objectType": 1018,
            "fields": [{"name":"pcfExternalSoftwareID1"},{"name":"pcfPaymentDate"},{"name":"pcfPayedIncludingVAT"},{"name":"pcfAccountid"},{"name":"createdon"}],
            "pageSize": 500, "pageNumber": page}).encode(), headers=HDRS)
    d = None
    for attempt in range(5):
        try:
            r = urllib.request.urlopen(req, timeout=60)
            d = json.loads(r.read()); break
        except Exception as e:
            print(f"p{page} a{attempt}: {str(e)[:50]}", flush=True)
            time.sleep(5)
    rows = d.get("data", [])
    all_rows.extend(rows)
    print(f"page {page}: +{len(rows)} (total {len(all_rows)})", flush=True)
    if d.get("isLastPage") or not rows: break
    page += 1
    time.sleep(1.0)
with open(r"C:\Users\sahar\Claude Code\RevitalYaish\_reconciliation\docs_full_with_acct.json", "w", encoding="utf-8") as f:
    json.dump(all_rows, f, ensure_ascii=False)
print("saved", flush=True)
