
import urllib.request, json
HDRS = {"tokenid": "b06663c4-62df-41b7-9111-6653e6b54592", "Content-Type": "application/json"}
req = urllib.request.Request("https://api.fireberry.com/api/v3/query",
    data=json.dumps({"objectType": 1039,
        "fields": [{"name":"name"},{"name":"pcfExternalSoftwareID1"},{"name":"pcfPayedIncludingVAT"},{"name":"pcfNumberOfPayments"},{"name":"pcfPaymentType"},{"name":"pcfStatus"}],
        "pageSize": 20, "pageNumber": 1,
        "filter": [{"type":"and","conditions":[
            {"fieldName":"pcfExternalSoftwareID1","operator":"eq","value":"GROW-DD-RECO-0027F9A2-347"}]}]}).encode(), headers=HDRS)
r = urllib.request.urlopen(req, timeout=60)
d = json.loads(r.read())
rows = d.get("data", [])
print("SO1 ->", len(rows))
for x in rows: print("   ", json.dumps(x, ensure_ascii=False))
