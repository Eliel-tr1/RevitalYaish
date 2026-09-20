
import urllib.request, json
HDRS = {"tokenid": "b06663c4-62df-41b7-9111-6653e6b54592", "Content-Type": "application/json"}
def fullrec(ot, ext, label):
    req = urllib.request.Request("https://api.fireberry.com/api/v3/query",
        data=json.dumps({"objectType": ot, "fields": [{"name":"pcfExternalSoftwareID1"}],
            "pageSize": 1, "pageNumber": 1,
            "filter": [{"type":"and","conditions":[
                {"fieldName":"pcfExternalSoftwareID1","operator":"eq","value":ext}]}]}).encode(), headers=HDRS)
    try:
        r = urllib.request.urlopen(req, timeout=30)
        rows = json.loads(r.read()).get("data", [])
        if not rows:
            print(label, "NOT FOUND"); return
        rid = rows[0]["_id"]
        req2 = urllib.request.Request(f"https://api.fireberry.com/api/record/{ot}/{rid}", headers=HDRS)
        r2 = urllib.request.urlopen(req2, timeout=30)
        rec2 = json.loads(r2.read())
        data2 = rec2.get("data", {}).get("Record", rec2.get("data"))
        money2 = {k: v for k, v in data2.items() if v not in (None, "") and ("pay" in k.lower() or "amount" in k.lower() or "sum" in k.lower() or "vat" in k.lower() or "numb" in k.lower())}
        print(label, ":", json.dumps(money2, ensure_ascii=False, indent=1))
    except Exception as e:
        body = getattr(e, "read", lambda: b"")()
        print(label, "FAIL", body[:120])

fullrec(1039, "GROW-DD-RECO-0027F9A2-347", "our reco SO")
fullrec(1039, "GROW-DD-515886638", "live SO (מורן רודניקי)")
