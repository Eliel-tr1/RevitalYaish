
import urllib.request, json
HDRS = {"tokenid": "b06663c4-62df-41b7-9111-6653e6b54592", "Content-Type": "application/json"}
# Metadata for object 4: find category + account + status fields
req = urllib.request.Request("https://api.fireberry.com/metadata/records/4/fields", headers=HDRS)
r = urllib.request.urlopen(req, timeout=30)
d = json.loads(r.read())
fields = d if isinstance(d, list) else d.get("Fields") or d.get("data") or []
print("total fields:", len(fields))
for f in fields:
    fn, lb = f.get("fieldName"), f.get("label")
    if fn and ("pcf" in fn.lower()[:3] or fn in ("name","statuscode","createdon","ownerid")):
        print(f"  {fn}: {lb!r} type={f.get('systemFieldTypeId','')[:8]}")
