
import urllib.request, json
HDRS = {"tokenid": "b06663c4-62df-41b7-9111-6653e6b54592", "Content-Type": "application/json"}
body = {"objectType": 14, "fields": [{"name": "name"}, {"name": "pcfItempriceIncludingVAT"}, {"name": "pcfProductType"}, {"name": "pcfDurationWeeks"}], "pageSize": 100, "pageNumber": 1}
req = urllib.request.Request("https://api.fireberry.com/api/v3/query", data=json.dumps(body).encode(), headers=HDRS)
r = urllib.request.urlopen(req, timeout=30)
prods = json.loads(r.read()).get("data", [])
for p in prods:
    print(f"  {p.get('name')!r} | price={p.get('pcfItempriceIncludingVAT')} | type={p.get('pcfProductType')} | weeks={p.get('pcfDurationWeeks')} | id={p.get('_id')}")
json.dump(prods, open(r"C:\Users\sahar\Claude Code\RevitalYaish\_reconciliation\products.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("saved", len(prods))
