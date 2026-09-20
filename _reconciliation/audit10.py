
import urllib.request, json
HDRS = {"tokenid": "b06663c4-62df-41b7-9111-6653e6b54592", "Content-Type": "application/json"}
def post(url, body):
    req = urllib.request.Request(url, data=json.dumps(body).encode(), headers=HDRS, method="POST")
    return json.loads(urllib.request.urlopen(req, timeout=30).read())

# create a throwaway doc with amount as string, then delete it
body = {"name": "TEST-AMOUNT-FIELD", "pcfAccountid": "21148f16-cad5-4ae8-b39f-4938615432a0",
        "pcfPaymetStatus": 1, "pcfPaymentDate": "2026-06-19 00:00:00",
        "pcfPayedIncludingVAT": "349", "pcfExternalSoftwareID1": "TEST-AMOUNT-DEL1",
        "pcftaxincludecode": 1, "pcfCreatedByPersonOrSystem": 2}
r = post("https://api.fireberry.com/api/record/1018", body)
rec = r["data"]["Record"]
rid = rec.get("customobject1018id") or rec.get("_id")
print("created", rid)
for k in ("pcfPayedIncludingVAT", "pcfPayed"):
    print("  ", k, "=", rec.get(k))
# delete
req = urllib.request.Request(f"https://api.fireberry.com/api/record/1018/{rid}", headers=HDRS, method="DELETE")
urllib.request.urlopen(req, timeout=30)
print("deleted")
