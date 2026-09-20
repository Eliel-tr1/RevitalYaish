
import urllib.request, json
HDRS = {"tokenid": "b06663c4-62df-41b7-9111-6653e6b54592", "Content-Type": "application/json"}
def q(fields):
    req = urllib.request.Request("https://api.fireberry.com/api/v3/query",
        data=json.dumps({"objectType": 1018,
            "fields": [{"name": f} for f in fields],
            "pageSize": 1, "pageNumber": 1,
            "filter": [{"type":"and","conditions":[
                {"fieldName":"pcfExternalSoftwareID1","operator":"eq","value":"GROW-493465701"}]}]}).encode(), headers=HDRS)
    try:
        r = urllib.request.urlopen(req, timeout=30)
        d = json.loads(r.read())
        return d.get("data", [])
    except Exception as e:
        body = getattr(e, "read", lambda: b"")()
        print("FAIL", body[:100]); return []

rows = q(["pcfExternalSoftwareID1","pcfPayedIncludingVAT","pcfPayed","pcfReference","pcfPaymentDate"])
print(json.dumps(rows, ensure_ascii=False, indent=1))
