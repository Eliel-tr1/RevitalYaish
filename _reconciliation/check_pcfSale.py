
import urllib.request, json
HDRS = {"tokenid": "b06663c4-62df-41b7-9111-6653e6b54592", "Content-Type": "application/json"}
for ot in (1018, 1039):
    req = urllib.request.Request(f"https://api.fireberry.com/metadata/records/{ot}/fields", headers=HDRS)
    r = urllib.request.urlopen(req, timeout=30)
    d = json.loads(r.read())
    fields = d if isinstance(d, list) else d.get("Fields") or d.get("data") or []
    for f in fields:
        if f.get("fieldName") == "pcfSale":
            print(f"{ot} pcfSale: {f.get('label')!r}")
