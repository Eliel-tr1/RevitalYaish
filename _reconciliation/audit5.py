
import urllib.request, json
HDRS = {"tokenid": "b06663c4-62df-41b7-9111-6653e6b54592", "Content-Type": "application/json"}
rid = "467165A3-5FB1-4250-821C-5E49A4162C0A"
req = urllib.request.Request(f"https://api.fireberry.com/api/record/1018/{rid}",
    data=json.dumps({"pcfPayedIncludingVAT": 347}).encode(), headers=HDRS, method="PUT")
r = urllib.request.urlopen(req, timeout=30)
print("PUT:", r.status)
# verify
req2 = urllib.request.Request("https://api.fireberry.com/api/v3/query",
    data=json.dumps({"objectType": 1018,
        "fields": [{"name":"pcfPayedIncludingVAT"}],
        "pageSize": 1, "pageNumber": 1,
        "filter": [{"type":"and","conditions":[
            {"fieldName":"pcfExternalSoftwareID1","operator":"eq","value":"GROW-457562960"}]}]}).encode(), headers=HDRS)
r2 = urllib.request.urlopen(req2, timeout=30)
d = json.loads(r2.read())
print("after PUT:", json.dumps(d.get("data"), ensure_ascii=False))
