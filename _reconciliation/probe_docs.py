
# -*- coding: utf-8 -*-
import urllib.request, json
HDRS = {"tokenid": "b06663c4-62df-41b7-9111-6653e6b54592", "Content-Type": "application/json"}
req = urllib.request.Request("https://api.fireberry.com/api/v3/query",
    data=json.dumps({"objectType": 1018,
        "fields": [{"name":"name"},{"name":"pcfExternalSoftwareID1"},{"name":"pcfPaymentCollection"},{"name":"pcfAccountid"}],
        "pageSize": 500, "pageNumber": 1,
        "filter": [{"type":"and","conditions":[
            {"fieldName":"pcfPaymentDate","operator":"ge","value":"2026-09-10 00:00:00"},
            {"fieldName":"pcfPaymentDate","operator":"le","value":"2026-09-19 23:59:59"}]}]}).encode(),
    headers=HDRS)
try:
    r = urllib.request.urlopen(req, timeout=60)
    d = json.loads(r.read())
    rows = d.get("data", [])
    hk = [x for x in rows if chr(1492)+chr(1501)+'"' + chr(1511) in (x.get("name") or "")]
    print("rows:", len(rows), "hk-ish:", len(hk))
    for x in rows[:8]: print("  ", json.dumps(x, ensure_ascii=False))
except Exception as e:
    body = getattr(e, "read", lambda: b"")()
    print("FAIL", e, body[:200])
