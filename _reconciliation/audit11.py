
import urllib.request, json
HDRS = {"tokenid": "b06663c4-62df-41b7-9111-6653e6b54592", "Content-Type": "application/json"}
def post(url, body):
    req = urllib.request.Request(url, data=json.dumps(body).encode(), headers=HDRS, method="POST")
    return json.loads(urllib.request.urlopen(req, timeout=30).read())

body = {"name": "TEST-AMOUNT-FIELD2", "pcfAccountid": "21148f16-cad5-4ae8-b39f-4938615432a0",
        "pcfPaymetStatus": 1, "pcfPaymentDate": "2026-06-19 00:00:00",
        "pcfPayedIncludingVAT": 349, "pcfPayed": 297.46, "pcfsystemfield100": 349,
        "pcfExternalSoftwareID1": "TEST-AMOUNT-DEL2", "pcftaxincludecode": 1, "pcfCreatedByPersonOrSystem": 2}
try:
    r = post("https://api.fireberry.com/api/record/1018", body)
    rec = r["data"]["Record"]
    rid = rec.get("customobject1018id") or rec.get("_id")
    for k in ("pcfPayedIncludingVAT", "pcfPayed", "pcfsystemfield100"):
        print("  ", k, "=", rec.get(k))
    req = urllib.request.Request(f"https://api.fireberry.com/api/record/1018/{rid}", headers=HDRS, method="DELETE")
    urllib.request.urlopen(req, timeout=30)
    print("deleted")
except Exception as e:
    body = getattr(e, "read", lambda: b"")()
    print("FAIL", body[:300])
