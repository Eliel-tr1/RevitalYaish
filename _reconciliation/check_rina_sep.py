
import urllib.request, json
HDRS = {"tokenid": "b06663c4-62df-41b7-9111-6653e6b54592", "Content-Type": "application/json"}
def q(ext):
    req = urllib.request.Request("https://api.fireberry.com/api/v3/query",
        data=json.dumps({"objectType": 1018,
            "fields": [{"name":"name"},{"name":"pcfExternalSoftwareID1"},{"name":"pcfPaymentDate"},{"name":"pcfPayedIncludingVAT"}],
            "pageSize": 5, "pageNumber": 1,
            "filter": [{"type":"and","conditions":[
                {"fieldName":"pcfExternalSoftwareID1","operator":"eq","value":ext}]}]}).encode(), headers=HDRS)
    r = urllib.request.urlopen(req, timeout=30)
    return json.loads(r.read()).get("data", [])
rows = q("GROW-514261210")
print("GROW-514261210 (רינה Sep):", len(rows), json.dumps(rows[0], ensure_ascii=False)[:200] if rows else "MISSING")
