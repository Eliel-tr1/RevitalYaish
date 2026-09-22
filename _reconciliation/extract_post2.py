
import urllib.request, json, time
HDRS = {"tokenid": "b06663c4-62df-41b7-9111-6653e6b54592", "Content-Type": "application/json"}
URL = "https://api.fireberry.com/api/v3/query"
all_rows, page = [], 1
while True:
    req = urllib.request.Request(URL,
        data=json.dumps({"objectType": 1018,
            "fields": [{"name":"pcfExternalSoftwareID1"},{"name":"pcfPaymentDate"},{"name":"pcfPayedIncludingVAT"},{"name":"pcfAccountid"}],
            "pageSize": 500, "pageNumber": page}).encode(), headers=HDRS)
    d = None
    for attempt in range(4):
        try:
            r = urllib.request.urlopen(req, timeout=60)
            d = json.loads(r.read()); break
        except Exception as e:
            print(f"p{page} a{attempt}: {str(e)[:40]}", flush=True)
            time.sleep(5)
    rows = d.get("data", [])
    all_rows.extend(rows)
    if d.get("isLastPage") or not rows: break
    page += 1
    time.sleep(1.0)
with open(r"C:\Users\sahar\Claude Code\RevitalYaish\_reconciliation\docs_post_cleanup_full.json", "w", encoding="utf-8") as f:
    json.dump(all_rows, f, ensure_ascii=False)
print("saved", len(all_rows), flush=True)
