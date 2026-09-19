
import urllib.request, json
HDRS = {"tokenid": "b06663c4-62df-41b7-9111-6653e6b54592", "Content-Type": "application/json"}
def q(ot, field, val, label):
    req = urllib.request.Request("https://api.fireberry.com/api/v3/query",
        data=json.dumps({"objectType": ot,
            "fields": [{"name":"name"},{"name":"pcfExternalSoftwareID1"},{"name":"pcfPaymentDate"},{"name":"pcfPayedIncludingVAT"}],
            "pageSize": 20, "pageNumber": 1,
            "filter": [{"type":"and","conditions":[
                {"fieldName":field,"operator":"eq","value":val}]}]}).encode(), headers=HDRS)
    try:
        r = urllib.request.urlopen(req, timeout=60)
        d = json.loads(r.read())
        rows = d.get("data", [])
        print(label, "->", len(rows))
        for x in rows[:3]: print("   ", json.dumps(x, ensure_ascii=False)[:180])
        return rows
    except Exception as e:
        body = getattr(e, "read", lambda: b"")()
        print(label, "FAIL", body[:150]); return []

q(1039, "pcfExternalSoftwareID1", "GROW-DD-RECO-0027F9A2-347", "SO1")
q(1018, "pcfExternalSoftwareID1", "GROW-457562960", "doc1")
q(1018, "pcfReference", "457562960", "doc by ref")
