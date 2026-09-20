
import urllib.request, json
HDRS = {"tokenid": "b06663c4-62df-41b7-9111-6653e6b54592", "Content-Type": "application/json"}
def post(url, body):
    req = urllib.request.Request(url, data=json.dumps(body).encode(), headers=HDRS, method="POST")
    return json.loads(urllib.request.urlopen(req, timeout=30).read())
def cleanup(rid):
    req = urllib.request.Request(f"https://api.fireberry.com/api/record/1018/{rid}", headers=HDRS, method="DELETE")
    urllib.request.urlopen(req, timeout=30)

# Test A: pcfPayed only (before VAT)
r = post("https://api.fireberry.com/api/record/1018", {"name": "TEST-A", "pcfAccountid": "21148f16-cad5-4ae8-b39f-4938615432a0",
    "pcfPaymetStatus": 1, "pcfPaymentDate": "2026-06-19 00:00:00", "pcfPayed": 297.46,
    "pcfExternalSoftwareID1": "TEST-AMT-A", "pcftaxincludecode": 1, "pcfCreatedByPersonOrSystem": 2})
rec = r["data"]["Record"]; rid = rec.get("customobject1018id") or rec.get("_id")
print("A pcfPayed:", rec.get("pcfPayed"), "incl:", rec.get("pcfPayedIncludingVAT"))
cleanup(rid)

# Test B: pcfPayedIncludingVAT only with taxinclude=1
r = post("https://api.fireberry.com/api/record/1018", {"name": "TEST-B", "pcfAccountid": "21148f16-cad5-4ae8-b39f-4938615432a0",
    "pcfPaymetStatus": 1, "pcfPaymentDate": "2026-06-19 00:00:00", "pcfPayedIncludingVAT": 349,
    "pcfExternalSoftwareID1": "TEST-AMT-B", "pcftaxincludecode": 1, "pcfCreatedByPersonOrSystem": 2})
rec = r["data"]["Record"]; rid = rec.get("customobject1018id") or rec.get("_id")
print("B incl:", rec.get("pcfPayedIncludingVAT"), "payed:", rec.get("pcfPayed"))
cleanup(rid)
