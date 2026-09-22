
import urllib.request, json
HDRS = {"tokenid": "b06663c4-62df-41b7-9111-6653e6b54592", "Content-Type": "application/json"}
rid = "467165A3-5FB1-4250-821C-5E49A4162C0A"
# verify exists
req = urllib.request.Request("https://api.fireberry.com/api/v3/query",
    data=json.dumps({"objectType": 1018, "fields": [{"name":"pcfExternalSoftwareID1"}],
        "pageSize": 1, "pageNumber": 1,
        "filter": [{"type":"and","conditions":[
            {"fieldName":"pcfExternalSoftwareID1","operator":"eq","value":"GROW-457562960"}]}]}).encode(), headers=HDRS)
r = urllib.request.urlopen(req, timeout=30)
print("exists:", len(json.loads(r.read()).get("data", [])))
# try single DELETE to see error
req2 = urllib.request.Request(f"https://api.fireberry.com/api/record/1018/{rid}", headers=HDRS, method="DELETE")
try:
    r2 = urllib.request.urlopen(req2, timeout=30)
    print("single delete:", r2.status)
except Exception as e:
    body = getattr(e, "read", lambda: b"")()
    print("single delete FAIL:", e, body[:300])
