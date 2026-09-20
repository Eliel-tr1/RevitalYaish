
import urllib.request, json
HDRS = {"tokenid": "b06663c4-62df-41b7-9111-6653e6b54592", "Content-Type": "application/json"}
# find any 1039 with pcfNumberOfPayments=0 and an amount (live SO) - e.g. from pilot verification earlier: SO name 'הוראת הקבע של גלית ישראלי'
req = urllib.request.Request("https://api.fireberry.com/api/v3/query",
    data=json.dumps({"objectType": 1039, "fields": [{"name":"name"}],
        "pageSize": 5, "pageNumber": 1,
        "filter": [{"type":"and","conditions":[
            {"fieldName":"name","operator":"eq-in","value":["הוראת הקבע של גלית ישראלי | תוכנית ליווי 22 שבועות | 917 ₪ | חיוב חודשי"]}]}]}).encode(), headers=HDRS)
r = urllib.request.urlopen(req, timeout=30)
rows = json.loads(r.read()).get("data", [])
print("found:", len(rows))
if rows:
    rid = rows[0]["_id"]
    req2 = urllib.request.Request(f"https://api.fireberry.com/api/record/1039/{rid}", headers=HDRS)
    r2 = urllib.request.urlopen(req2, timeout=30)
    rec2 = json.loads(r2.read())
    data2 = rec2.get("data", {}).get("Record", rec2.get("data"))
    money2 = {k: v for k, v in data2.items() if v not in (None, "") and ("pay" in k.lower() or "amount" in k.lower() or "sum" in k.lower() or "vat" in k.lower() or "numb" in k.lower())}
    print("live SO:", json.dumps(money2, ensure_ascii=False, indent=1))
    print("ext:", data2.get("pcfExternalSoftwareID1"), "| pcfID:", data2.get("pcfID"))
