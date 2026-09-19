
import urllib.request, json
HDRS = {"tokenid": "b06663c4-62df-41b7-9111-6653e6b54592", "Content-Type": "application/json"}
req = urllib.request.Request("https://api.fireberry.com/metadata/records/1/fields", headers=HDRS)
r = urllib.request.urlopen(req, timeout=30)
d = json.loads(r.read())
fields = d if isinstance(d, list) else d.get("Fields") or d.get("data") or []
for f in fields:
    fn, lb = f.get("fieldName"), f.get("label")
    if fn and (fn in ("name","accountname","fullname","lastname","firstname") or "שם" in (lb or "")):
        print(f"{fn}: {lb!r}")
