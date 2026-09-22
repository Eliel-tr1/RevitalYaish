
import urllib.request, json
HDRS = {"tokenid": "b06663c4-62df-41b7-9111-6653e6b54592", "Content-Type": "application/json"}
def q(ot, fields, flt):
    req = urllib.request.Request("https://api.fireberry.com/api/v3/query",
        data=json.dumps({"objectType": ot, "fields": [{"name": f} for f in fields],
            "pageSize": 100, "pageNumber": 1,
            "filter": [{"type":"and","conditions":flt}]}).encode(), headers=HDRS)
    r = urllib.request.urlopen(req, timeout=45)
    return json.loads(r.read()).get("data", [])

docs = q(1018, ["name","pcfExternalSoftwareID1","pcfPaymentDate","pcfPayedIncludingVAT","pcfPaymentCollection","createdon"],
         [{"fieldName":"pcfAccountid","operator":"eq","value":"02EB8E56-3D38-43A6-9A31-A510AAE1514F"}])
print("=== כל תיעודי התשלום (1018) של אורית ===")
for x in sorted(docs, key=lambda y: str(y.get("pcfPaymentDate"))):
    parent = (x.get("pcfPaymentCollection") or "")[:8]
    print(f"  {x['_id']} | {str(x.get('pcfPaymentDate'))[:10]} | ₪{x.get('pcfPayedIncludingVAT')} | parent={parent} | ext={x.get('pcfExternalSoftwareID1')} | created={str(x.get('createdon'))[:16]} | {x.get('name','')[:40]}")
