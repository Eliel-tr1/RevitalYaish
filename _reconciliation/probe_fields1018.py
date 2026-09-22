
import urllib.request, json
HDRS = {"tokenid": "b06663c4-62df-41b7-9111-6653e6b54592", "Content-Type": "application/json"}
def probe(field):
    req = urllib.request.Request("https://api.fireberry.com/api/v3/query",
        data=json.dumps({"objectType": 1018, "fields": [{"name": field}],
            "pageSize": 1, "pageNumber": 1}).encode(), headers=HDRS)
    try:
        r = urllib.request.urlopen(req, timeout=30)
        return f"OK: {json.loads(r.read()).get('data',[{}])[0].get(field)}"
    except Exception as e:
        body = getattr(e, "read", lambda: b"")()
        return f"FAIL {body[:80]}"
for f in ["pcfSale", "pcfPaymentCollection", "pcfProduct", "pcfExternalSoftwareID1"]:
    print(f, probe(f))
