
import urllib.request, json, time
HDRS = {"tokenid": "b06663c4-62df-41b7-9111-6653e6b54592", "Content-Type": "application/json"}
for ext in ["GROW-495429507", "GROW-478196752"]:
    # find id
    req = urllib.request.Request("https://api.fireberry.com/api/v3/query",
        data=json.dumps({"objectType": 1018, "fields": [{"name":"pcfExternalSoftwareID1"}],
            "pageSize": 2, "pageNumber": 1,
            "filter": [{"type":"and","conditions":[
                {"fieldName":"pcfExternalSoftwareID1","operator":"eq","value": ext}]}]}).encode(), headers=HDRS)
    r = urllib.request.urlopen(req, timeout=30)
    rows = json.loads(r.read()).get("data", [])
    if not rows:
        print(ext, "already gone"); continue
    rid = rows[0]["_id"]
    req2 = urllib.request.Request(f"https://api.fireberry.com/api/record/1018/{rid}", headers=HDRS, method="DELETE")
    try:
        r2 = urllib.request.urlopen(req2, timeout=30)
        print(ext, "deleted", r2.status)
    except Exception as e:
        body = getattr(e, "read", lambda: b"")()
        print(ext, "FAIL", e, body[:150])
    time.sleep(1.5)
