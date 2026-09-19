
import urllib.request, json
HDRS = {"tokenid": "b06663c4-62df-41b7-9111-6653e6b54592", "Content-Type": "application/json"}
req = urllib.request.Request("https://api.fireberry.com/api/v3/query",
    data=json.dumps({"objectType": 1039,
        "fields": [{"name":"name"},{"name":"pcfExternalSoftwareID1"}],
        "pageSize": 5, "pageNumber": 1,
        "filter": [{"type":"and","conditions":[
            {"fieldName":"pcfAccountid","operator":"ne","value":"00000000-0000-0000-0000-000000000000"},
            {"fieldName":"pcfNumberOfPayments","operator":"eq","value":0}]}]}).encode(), headers=HDRS)
r = urllib.request.urlopen(req, timeout=60)
d = json.loads(r.read())
rows = d.get("data", [])
print("SO-like rows:", len(rows))
for x in rows[:5]: print("  ", json.dumps(x, ensure_ascii=False))
