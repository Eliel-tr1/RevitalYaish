
import urllib.request, json
HDRS = {"tokenid": "b06663c4-62df-41b7-9111-6653e6b54592", "Content-Type": "application/json"}
def q(cond):
    req = urllib.request.Request("https://api.fireberry.com/api/v3/query",
        data=json.dumps({"objectType": 1039,
            "fields": [{"name":"name"},{"name":"pcfNumberOfPayments"}],
            "pageSize": 5, "pageNumber": 1,
            "filter": [{"type":"and","conditions":cond}]}).encode(), headers=HDRS)
    r = urllib.request.urlopen(req, timeout=60)
    d = json.loads(r.read())
    return d.get("data", [])

rows = q([{"fieldName":"pcfNumberOfPayments","operator":"eq","value":"0"}])
rid = rows[0]["_id"].upper()
try:
    req2 = urllib.request.Request(f"https://api.fireberry.com/api/record/1039/{rid}", headers=HDRS)
    r2 = urllib.request.urlopen(req2, timeout=60)
    rec = json.loads(r2.read())
    print("GET OK")
    rec_data = rec.get("data", {}).get("Record", rec.get("data"))
    interesting = {k: v for k, v in rec_data.items() if v not in (None, "", []) and (k.startswith("pcf") or k in ("name","statuscode","ownerid"))}
    out = json.dumps(interesting, ensure_ascii=False, indent=1)
    open(r"C:\Users\sahar\Claude Code\RevitalYaish\_reconciliation\so_pattern.json", "w", encoding="utf-8").write(out)
    print(out[:2200])
except Exception as e:
    body = getattr(e, "read", lambda: b"")()
    print("GET FAIL", e, body[:300])
