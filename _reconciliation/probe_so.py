
import urllib.request, json
HDRS = {"tokenid": "b06663c4-62df-41b7-9111-6653e6b54592", "Content-Type": "application/json"}
# find one live SO by ext id from the sample: GROW-DD-50996664
req = urllib.request.Request("https://api.fireberry.com/api/v3/query",
    data=json.dumps({"objectType": 1039,
        "fields": [{"name":"name"},{"name":"pcfExternalSoftwareID1"},{"name":"pcfNumberOfPayments"},{"name":"pcfFirstPaymentDate"},{"name":"pcfStatus"},{"name":"pcfPaymentType"}],
        "pageSize": 3, "pageNumber": 1,
        "filter": [{"type":"and","conditions":[
            {"fieldName":"pcfExternalSoftwareID1","operator":"eq","value":"GROW-DD-50996664"}]}]}).encode(), headers=HDRS)
r = urllib.request.urlopen(req, timeout=60)
d = json.loads(r.read())
rows = d.get("data", [])
if rows:
    rid = rows[0]["_id"]
    # GET full record
    req2 = urllib.request.Request(f"https://api.fireberry.com/api/record/1039/{rid}", headers=HDRS)
    r2 = urllib.request.urlopen(req2, timeout=60)
    rec = json.loads(r2.read())
    rec_data = rec.get("data", {}).get("Record", rec.get("data"))
    # print only non-null interesting fields
    interesting = {k: v for k, v in rec_data.items() if v not in (None, "", []) and (k.startswith("pcf") or k in ("name","statuscode","ownerid"))}
    print(json.dumps(interesting, ensure_ascii=False, indent=1))
