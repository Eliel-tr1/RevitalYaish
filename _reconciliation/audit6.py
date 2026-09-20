
import urllib.request, json
HDRS = {"tokenid": "b06663c4-62df-41b7-9111-6653e6b54592", "Content-Type": "application/json"}
req = urllib.request.Request("https://api.fireberry.com/metadata/records/1018/fields", headers=HDRS)
r = urllib.request.urlopen(req, timeout=30)
d = json.loads(r.read())
fields = d if isinstance(d, list) else d.get("Fields") or d.get("data") or []
for f in fields:
    if f.get("fieldName") in ("pcfPayedIncludingVAT", "pcfPayed", "pcfsystemfield100", "pcfPaymetStatus"):
        print(json.dumps(f, ensure_ascii=False)[:400])
