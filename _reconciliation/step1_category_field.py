# -*- coding: utf-8 -*-
"""Step 1: discover the category field on object 4 (sale process) - READ ONLY."""
import json, time, urllib.request

TOKEN = "b06663c4-62df-41b7-9111-6653e6b54592"
BASE = "https://api.fireberry.com"

def call(method, path, body=None):
    req = urllib.request.Request(BASE + path, method=method)
    req.add_header("tokenid", TOKEN)
    req.add_header("Content-Type", "application/json")
    data = json.dumps(body).encode() if body is not None else None
    try:
        with urllib.request.urlopen(req, data=data, timeout=30) as r:
            return r.status, json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        try:
            return e.code, json.loads(e.read().decode())
        except Exception:
            return e.code, {}

def get(path):
    req = urllib.request.Request(BASE + path)
    req.add_header("tokenid", TOKEN)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        try:
            return e.code, json.loads(e.read().decode())
        except Exception:
            return e.code, {}

st, meta = get("/metadata/records/4/fields")
print("metadata status:", st)
if st == 200:
    fields = meta.get("data", meta)
    # dump all field names + labels for manual inspection
    with open("step1_object4_fields.json", "w", encoding="utf-8") as f:
        json.dump(fields, f, ensure_ascii=False, indent=1)
    names = [x.get("systemname") or x.get("fieldName") or str(x)[:60] for x in (fields if isinstance(fields, list) else fields.get("Fields", []))]
    print("total fields:", len(names))
    # show candidates that mention category-like words
    for x in (fields if isinstance(fields, list) else []):
        lbl = str(x.get("label") or x.get("displayName") or "")
        nm = str(x.get("systemname") or x.get("fieldName") or "")
        for kw in ["קטגור", "סוג", "מוצר", "category", "type", "product"]:
            if kw in lbl or kw in nm.lower():
                print(nm, "|", lbl, "|", x.get("fieldobjecttype") or x.get("fieldObjectType"))
                break
else:
    print(json.dumps(meta, ensure_ascii=False)[:500])
