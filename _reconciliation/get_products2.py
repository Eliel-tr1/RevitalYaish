
import urllib.request, json
HDRS = {"tokenid": "b06663c4-62df-41b7-9111-6653e6b54592", "Content-Type": "application/json"}
def q(ot, fields, n=500):
    body = {"objectType": ot, "fields": [{"name": f} for f in fields], "pageSize": n, "pageNumber": 1}
    req = urllib.request.Request("https://api.fireberry.com/api/v3/query", data=json.dumps(body).encode(), headers=HDRS)
    r = urllib.request.urlopen(req, timeout=30)
    return json.loads(r.read()).get("data", [])
try:
    prods = q(14, ["name", "pcfItempriceIncludingVAT", "pcfProductType", "pcfDurationWeeks", "_id"])
    for p in prods:
        print(f"  {p.get('name')!r} | price={p.get('pcfItempriceIncludingVAT')} | type={p.get('pcfProductType')} | weeks={p.get('pcfDurationWeeks')} | id={p['_id']}")
    json.dump(prods, open(r"C:\Users\sahar\Claude Code\RevitalYaish\_reconciliation\products.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
except Exception as e:
    body = getattr(e, "read", lambda: b"")()
    print("FAIL", body[:200])
