
import urllib.request, json
HDRS = {"tokenid": "b06663c4-62df-41b7-9111-6653e6b54592", "Content-Type": "application/json"}
ACCT = "02EB8E56-3D38-43A6-9A31-A510AAE1514F"
def q(ot, fields, flt):
    req = urllib.request.Request("https://api.fireberry.com/api/v3/query",
        data=json.dumps({"objectType": ot, "fields": [{"name": f} for f in fields],
            "pageSize": 100, "pageNumber": 1,
            "filter": [{"type":"and","conditions":flt}]}).encode(), headers=HDRS)
    r = urllib.request.urlopen(req, timeout=45)
    return json.loads(r.read()).get("data", [])

# All her 1039s
pays = q(1039, ["name","pcfExternalSoftwareID1","pcfPaymentType","pcfNeedToPayIncludingVat","pcfNumberOfPayments","pcfFirstPaymentDate","createdon","pcfID"],
         [{"fieldName":"pcfAccountid","operator":"eq","value":ACCT}])
print("=== כל התשלומים (1039) של אורית אלמליח ===")
for p in pays:
    print(f"  {p['_id']} | {p.get('name','')[:55]} | type={p.get('pcfPaymentType')} | N={p.get('pcfNumberOfPayments')} | first={str(p.get('pcfFirstPaymentDate'))[:10]} | ext={p.get('pcfExternalSoftwareID1')} | created={str(p.get('createdon'))[:16]}")
