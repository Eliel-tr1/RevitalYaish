# -*- coding: utf-8 -*-
"""קריאת מטא-דאטה של אובייקט 4 + דגימת רשומות. קריאה בלבד."""
import json, sys, time
import requests

TOKEN = "b06663c4-62df-41b7-9111-6653e6b54592"
BASE = "https://api.fireberry.com"
H = {"tokenid": TOKEN, "Content-Type": "application/json"}

def md(path):
    r = requests.get(BASE + path, headers=H, timeout=30)
    print(path, r.status_code)
    return r

fields = md("/metadata/records/4/fields").json()
with open("md_obj4_fields.json", "w", encoding="utf-8") as f:
    json.dump(fields, f, ensure_ascii=False, indent=1)

# list field names compactly
rows = fields if isinstance(fields, list) else fields.get("data", fields)
names = []
for it in rows:
    if isinstance(it, dict):
        names.append((it.get("fieldName") or it.get("name"), it.get("displayName") or it.get("label"), it.get("fieldObjectType") or it.get("targetObjectType")))
print("total fields:", len(names))
for n in names:
    print(n)
