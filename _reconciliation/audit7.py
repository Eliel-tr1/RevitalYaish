
import urllib.request, json
HDRS = {"tokenid": "b06663c4-62df-41b7-9111-6653e6b54592", "Content-Type": "application/json"}
def q(ot, ext, fields):
    req = urllib.request.Request("https://api.fireberry.com/api/v3/query",
        data=json.dumps({"objectType": ot,
            "fields": [{"name": f} for f in fields],
            "pageSize": 1, "pageNumber": 1,
            "filter": [{"type":"and","conditions":[
                {"fieldName":"pcfExternalSoftwareID1","operator":"eq","value":ext}]}]}).encode(), headers=HDRS)
    r = urllib.request.urlopen(req, timeout=30)
    return json.loads(r.read()).get("data", [])
rows = q(1039, "GROW-DD-RECO-0027F9A2-347", ["pcfExternalSoftwareID1","pcfNeedToPayIncludingVat","pcfsystemfield100"])
print("SO amount:", json.dumps(rows, ensure_ascii=False))
# Try doc PUT with string value
rid = "467165A3-5FB1-4250-821C-5E49A4162C0A"
for val in ["347", 347.0, "347.00"]:
    req = urllib.request.Request(f"https://api.fireberry.com/api/record/1018/{rid}",
        data=json.dumps({"pcfPayedIncludingVAT": val}).encode(), headers=HDRS, method="PUT")
    r = urllib.request.urlopen(req, timeout=30)
    rows = q(1018, "GROW-457562960", ["pcfPayedIncludingVAT"])
    print(f"PUT val={val!r} -> {json.dumps(rows, ensure_ascii=False)}")
