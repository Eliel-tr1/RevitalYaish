
import urllib.request, json
HDRS = {"tokenid": "b06663c4-62df-41b7-9111-6653e6b54592", "Content-Type": "application/json"}
def q(cond, label):
    req = urllib.request.Request("https://api.fireberry.com/api/v3/query",
        data=json.dumps({"objectType": 1039,
            "fields": [{"name":"name"},{"name":"pcfExternalSoftwareID1"},{"name":"pcfNumberOfPayments"}],
            "pageSize": 5, "pageNumber": 1,
            "filter": [{"type":"and","conditions":cond}]}).encode(), headers=HDRS)
    try:
        r = urllib.request.urlopen(req, timeout=60)
        d = json.loads(r.read())
        rows = d.get("data", [])
        print(label, "->", len(rows))
        return rows
    except Exception as e:
        body = getattr(e, "read", lambda: b"")()
        print(label, "FAIL", body[:100]); return []

rows = q([{"fieldName":"pcfNumberOfPayments","operator":"eq","value":0}], "N=0")
if rows:
    rid = rows[0]["_id"]
    req2 = urllib.request.Request(f"https://api.fireberry.com/api/record/1039/{rid}", headers=HDRS)
    r2 = urllib.request.urlopen(req2, timeout=60)
    rec = json.loads(r2.read())
    rec_data = rec.get("data", {}).get("Record", rec.get("data"))
    interesting = {k: v for k, v in rec_data.items() if v not in (None, "", []) and (k.startswith("pcf") or k in ("name","statuscode","ownerid"))}
    import sys
    print(json.dumps(interesting, ensure_ascii=False, indent=1)[:2500])
