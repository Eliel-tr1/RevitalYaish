
import urllib.request, json, time
HDRS = {"tokenid": "b06663c4-62df-41b7-9111-6653e6b54592", "Content-Type": "application/json"}
URL = "https://api.fireberry.com/api/v3/query"
all_rows, page = [], 1
while True:
    body = {"objectType": 4,
            "fields": [{"name":"name"},{"name":"statuscode"},{"name":"pcfProduct"},{"name":"accountid"},{"name":"pcfclosedate"},{"name":"createdon"}],
            "pageSize": 500, "pageNumber": page}
    req = urllib.request.Request(URL, data=json.dumps(body).encode(), headers=HDRS)
    for attempt in range(3):
        try:
            r = urllib.request.urlopen(req, timeout=60)
            d = json.loads(r.read()); break
        except Exception:
            if attempt == 2: raise
            time.sleep(3)
    rows = d.get("data", [])
    all_rows.extend(rows)
    print(f"page {page}: +{len(rows)} (total {len(all_rows)})", flush=True)
    if d.get("isLastPage") or not rows: break
    page += 1
    time.sleep(0.7)
with open(r"C:\Users\sahar\Claude Code\RevitalYaish\_reconciliation\opps_all.json", "w", encoding="utf-8") as f:
    json.dump(all_rows, f, ensure_ascii=False)
print("saved", len(all_rows), flush=True)
