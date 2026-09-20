
import urllib.request, json
HDRS = {"tokenid": "b06663c4-62df-41b7-9111-6653e6b54592", "Content-Type": "application/json"}
# pilot doc: GROW-457562960 (נופר, 347)
def q(ext, fields):
    req = urllib.request.Request("https://api.fireberry.com/api/v3/query",
        data=json.dumps({"objectType": 1018,
            "fields": [{"name": f} for f in fields],
            "pageSize": 1, "pageNumber": 1,
            "filter": [{"type":"and","conditions":[
                {"fieldName":"pcfExternalSoftwareID1","operator":"eq","value":ext}]}]}).encode(), headers=HDRS)
    r = urllib.request.urlopen(req, timeout=30)
    return json.loads(r.read()).get("data", [])
rows = q("GROW-457562960", ["pcfExternalSoftwareID1","pcfPayedIncludingVAT","pcfPayed"])
print("pilot doc:", json.dumps(rows, ensure_ascii=False))
# live WF-20 doc for comparison: GROW-517044601 (גלית, 917)
rows2 = q("GROW-517044601", ["pcfExternalSoftwareID1","pcfPayedIncludingVAT","pcfPayed"])
print("live doc:", json.dumps(rows2, ensure_ascii=False))
