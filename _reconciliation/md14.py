
import urllib.request, json
HDRS = {"tokenid": "b06663c4-62df-41b7-9111-6653e6b54592", "Content-Type": "application/json"}
def q(ot, fields, n=500, flt=None):
    body = {"objectType": ot, "fields": [{"name": f} for f in fields], "pageSize": n, "pageNumber": 1}
    if flt: body["filter"] = flt
    req = urllib.request.Request("https://api.fireberry.com/api/v3/query", data=json.dumps(body).encode(), headers=HDRS)
    r = urllib.request.urlopen(req, timeout=30)
    return json.loads(r.read()).get("data", [])

# metadata for 14 to find price field
req = urllib.request.Request("https://api.fireberry.com/metadata/records/14/fields", headers=HDRS)
r = urllib.request.urlopen(req, timeout=30)
d = json.loads(r.read())
fields = d if isinstance(d, list) else d.get("Fields") or d.get("data") or []
for f in fields:
    fn, lb = f.get("fieldName"), f.get("label")
    if fn and ("pcf" in fn.lower()[:3] or fn in ("name",)):
        print(f"  {fn}: {lb!r}")
