
import urllib.request, json
HDRS = {"tokenid": "b06663c4-62df-41b7-9111-6653e6b54592", "Content-Type": "application/json"}
# live doc GROW-517044601 -> find _id
req = urllib.request.Request("https://api.fireberry.com/api/v3/query",
    data=json.dumps({"objectType": 1018, "fields": [{"name":"pcfExternalSoftwareID1"}],
        "pageSize": 1, "pageNumber": 1,
        "filter": [{"type":"and","conditions":[
            {"fieldName":"pcfExternalSoftwareID1","operator":"eq","value":"GROW-517044601"}]}]}).encode(), headers=HDRS)
r = urllib.request.urlopen(req, timeout=30)
rid = json.loads(r.read())["data"][0]["_id"]
req2 = urllib.request.Request(f"https://api.fireberry.com/api/record/1018/{rid}", headers=HDRS)
r2 = urllib.request.urlopen(req2, timeout=30)
rec = json.loads(r2.read())
data = rec.get("data", {}).get("Record", rec.get("data"))
money = {k: v for k, v in data.items() if v not in (None, "") and ("pay" in k.lower() or "amount" in k.lower() or "sum" in k.lower() or "vat" in k.lower())}
print("live doc money fields:", json.dumps(money, ensure_ascii=False, indent=1))
# Same for one live SO 1039:
req = urllib.request.Request("https://api.fireberry.com/api/v3/query",
    data=json.dumps({"objectType": 1039, "fields": [{"name":"pcfExternalSoftwareID1"}],
        "pageSize": 1, "pageNumber": 1,
        "filter": [{"type":"and","conditions":[
            {"fieldName":"pcfExternalSoftwareID1","operator":"eq","value":"GROW-DD-47749864"}]}]}).encode(), headers=HDRS)
r = urllib.request.urlopen(req, timeout=30)
rows = json.loads(r.read()).get("data", [])
if rows:
    rid2 = rows[0]["_id"]
    req2 = urllib.request.Request(f"https://api.fireberry.com/api/record/1039/{rid2}", headers=HDRS)
    r2 = urllib.request.urlopen(req2, timeout=30)
    rec2 = json.loads(r2.read())
    data2 = rec2.get("data", {}).get("Record", rec2.get("data"))
    money2 = {k: v for k, v in data2.items() if v not in (None, "") and ("pay" in k.lower() or "amount" in k.lower() or "sum" in k.lower() or "vat" in k.lower())}
    print("live SO money fields:", json.dumps(money2, ensure_ascii=False, indent=1))
