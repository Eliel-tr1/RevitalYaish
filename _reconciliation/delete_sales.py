# -*- coding: utf-8 -*-
# Backup the 10 sale-process records in full, then delete ONE as pilot.
import json, urllib.request, urllib.error, time
HDRS = {"tokenid": "b06663c4-62df-41b7-9111-6653e6b54592", "Content-Type": "application/json"}
IDS = ["3421E629-5C83-4302-9964-0E0C364CE883","35AA2086-FE5A-4628-A582-D3131354E7A9",
"FC7C3BD6-9AA8-45C4-B74C-F02AF3A9DB94","52B283EB-BE9C-43CB-9915-19E8B8F5FBAE",
"CF41528B-66BD-4B9B-A046-2895027E1897","1EBD38AD-4B23-4B98-BDB5-AC4A874BFAF7",
"D0B72253-04EF-4CB2-9DE4-B5D9EC111118","ADFB7E35-754F-4479-A28E-475A75F6142D",
"5CC1284C-7E47-4B97-8D79-685F95597FB0","21DF4DDC-D879-49ED-BA44-57641A622D90"]
def get(path, method="GET", body=None):
    req = urllib.request.Request("https://api.fireberry.com"+path, data=json.dumps(body).encode() if body else None, headers=HDRS, method=method)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        try: return e.code, json.loads(e.read().decode())
        except Exception: return e.code, {}

backup = {}
ok = 0
for i in IDS:
    st, d = get(f"/api/record/4/{i}")
    backup[i] = {"status": st, "data": d}
    ok += st == 200
    time.sleep(0.8)
json.dump(backup, open("../claude/BACKUP_2026-09-22_10_תהליכי_מכירה_לפני_מחיקה.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
print("backup ok:", ok, "/", len(IDS))
