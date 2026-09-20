
import urllib.request, json
HDRS = {"tokenid": "b06663c4-62df-41b7-9111-6653e6b54592", "Content-Type": "application/json"}
req = urllib.request.Request("https://api.fireberry.com/api/v3/query",
    data=json.dumps({"objectType": 1018,
        "fields": [{"name":"pcfReference"},{"name":"pcfPayed"},{"name":"pcfPayedIncludingVAT"},{"name":"pcfExternalSoftwareID1"},{"name":"pcfPaymentDate"}],
        "pageSize": 1, "pageNumber": 1,
        "filter": [{"type":"and","conditions":[
            {"fieldName":"pcfReference","operator":"eq","value":"502067152"}]}]}).encode(), headers=HDRS)
r = urllib.request.urlopen(req, timeout=30)
print(json.dumps(r.read().decode(), ensure_ascii=False)[:400])
