
import urllib.request, json
HDRS = {"tokenid": "b06663c4-62df-41b7-9111-6653e6b54592", "Content-Type": "application/json"}
req = urllib.request.Request("https://api.fireberry.com/api/v3/query",
    data=json.dumps({"objectType": 1039, "fields": [{"name":"pcfExternalSoftwareID1"}],
        "pageSize": 20, "pageNumber": 1,
        "filter": [{"type":"and","conditions":[
            {"fieldName":"pcfExternalSoftwareID1","operator":"eq-in","value":["GROW-DD-RECO-0027F9A2-347","GROW-DD-RECO-8933B1BF-917"]}]}]}).encode(), headers=HDRS)
try:
    r = urllib.request.urlopen(req, timeout=30)
    d = json.loads(r.read())
    print("rows:", len(d.get("data", [])))
    for x in d.get("data", []): print("  ", json.dumps(x, ensure_ascii=False))
except Exception as e:
    body = getattr(e, "read", lambda: b"")()
    print("FAIL", body[:150])
