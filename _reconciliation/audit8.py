
import urllib.request, json
HDRS = {"tokenid": "b06663c4-62df-41b7-9111-6653e6b54592", "Content-Type": "application/json"}
def q(ot, ext, fields, label):
    req = urllib.request.Request("https://api.fireberry.com/api/v3/query",
        data=json.dumps({"objectType": ot,
            "fields": [{"name": f} for f in fields],
            "pageSize": 1, "pageNumber": 1,
            "filter": [{"type":"and","conditions":[
                {"fieldName":"pcfExternalSoftwareID1","operator":"eq","value":ext}]}]}).encode(), headers=HDRS)
    try:
        r = urllib.request.urlopen(req, timeout=30)
        d = json.loads(r.read())
        print(label, "->", json.dumps(d.get("data"), ensure_ascii=False)[:300])
        return d.get("data", [])
    except Exception as e:
        body = getattr(e, "read", lambda: b"")()
        print(label, "FAIL", body[:120]); return []

q(1039, "GROW-DD-RECO-0027F9A2-347", ["pcfNeedToPayIncludingVat"], "SO amount")
q(1039, "GROW-DD-RECO-0027F9A2-347", ["pcfsystemfield100"], "SO field100")

rid = "467165A3-5FB1-4250-821C-5E49A4162C0A"
req = urllib.request.Request(f"https://api.fireberry.com/api/record/1018/{rid}",
    data=json.dumps({"pcfPayedIncludingVAT": "347"}).encode(), headers=HDRS, method="PUT")
try:
    r = urllib.request.urlopen(req, timeout=30)
    print("PUT string:", r.status, r.read()[:150])
except Exception as e:
    body = getattr(e, "read", lambda: b"")()
    print("PUT string FAIL", body[:150])
q(1018, "GROW-457562960", ["pcfPayedIncludingVAT"], "doc after")
