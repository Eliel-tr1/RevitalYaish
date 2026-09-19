
import urllib.request, json
HDRS = {"tokenid": "b06663c4-62df-41b7-9111-6653e6b54592", "Content-Type": "application/json"}
def q(ot, field, val):
    req = urllib.request.Request("https://api.fireberry.com/api/v3/query",
        data=json.dumps({"objectType": ot,
            "fields": [{"name":"name"},{"name":"pcfExternalSoftwareID1"}],
            "pageSize": 5, "pageNumber": 1,
            "filter": [{"type":"and","conditions":[
                {"fieldName":field,"operator":"eq","value":val}]}]}).encode(), headers=HDRS)
    r = urllib.request.urlopen(req, timeout=60)
    return json.loads(r.read()).get("data", [])
SO_EXT = "GROW-DD-RECO-EBC47B86-649"
rows = q(1039, "pcfExternalSoftwareID1", SO_EXT)
print("SO:", len(rows), rows[0]["_id"] if rows else None)
if rows:
    doc_body = {
        "name": "\u05ea\u05d9\u05e2\u05d5\u05d3 \u05d4\u05ea\u05e9\u05dc\u05d5\u05dd \u05d4\u05d5\"\u05e7 \u05e9\u05dc \u05e9\u05e4\u05e8\u05d4 \u05d3\u05d1\u05d5\u05e8\u05e7\u05d9\u05df | \u05dc\u05d9\u05d5\u05d5\u05d9 \u05ea\u05d6\u05d5\u05e0\u05d4 \u05d0\u05d5\u05e0\u05dc\u05d9\u05d9\u05df - \u05de\u05e0\u05d8\u05d5\u05e8\u05d9\u05ea \u05d0\u05d9\u05e9\u05d9\u05ea",
        "pcfPaymentCollection": rows[0]["_id"],
        "pcfAccountid": "EBC47B86-B9FB-420C-9B18-829159289347",
        "pcfPaymetStatus": 1,
        "pcfPaymentDate": "2026-03-11 00:00:00",
        "pcfPayedIncludingVAT": 649.0,
        "pcfReference": "470288811",
        "pcfExternalSoftwareID1": "GROW-470288811",
        "pcfPaymentType": 1,
        "pcftaxincludecode": 1,
        "pcfCreatedByPersonOrSystem": 2,
    }
    req2 = urllib.request.Request("https://api.fireberry.com/api/record/1018",
        data=json.dumps(doc_body).encode(), headers=HDRS, method="POST")
    r2 = urllib.request.urlopen(req2, timeout=60)
    print("DOC CREATED OK")
# verify
rows2 = q(1018, "pcfExternalSoftwareID1", "GROW-470288811")
print("verified:", len(rows2), json.dumps(rows2[0], ensure_ascii=False)[:200] if rows2 else "")
