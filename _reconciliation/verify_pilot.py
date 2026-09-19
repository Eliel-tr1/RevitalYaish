
import urllib.request, json
HDRS = {"tokenid": "b06663c4-62df-41b7-9111-6653e6b54592", "Content-Type": "application/json"}
def q(ext_prefix, ot):
    req = urllib.request.Request("https://api.fireberry.com/api/v3/query",
        data=json.dumps({"objectType": ot,
            "fields": [{"name":"name"},{"name":"pcfExternalSoftwareID1"},{"name":"pcfPaymentDate"},{"name":"pcfPayedIncludingVAT"},{"name":"pcfPaymetStatus"},{"name":"pcfNumberOfPayments"},{"name":"pcfPaymentType"}],
            "pageSize": 50, "pageNumber": 1,
            "filter": [{"type":"and","conditions":[
                {"fieldName":"pcfExternalSoftwareID1","operator":"eq","value":ext_prefix}]}]}).encode(), headers=HDRS)
    r = urllib.request.urlopen(req, timeout=60)
    return json.loads(r.read()).get("data", [])

# Verify SO 1
so1 = q("GROW-DD-RECO-0027F9A2-347", 1039)
print("SO1:", json.dumps(so1, ensure_ascii=False, indent=1)[:600] if so1 else "NOT FOUND")
# Verify docs of ref 457562960
docs = q("GROW-457562960", 1018)
print("doc 457562960:", json.dumps(docs, ensure_ascii=False, indent=1)[:600] if docs else "NOT FOUND")
