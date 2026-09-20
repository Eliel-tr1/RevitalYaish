
import urllib.request, json
HDRS = {"tokenid": "b06663c4-62df-41b7-9111-6653e6b54592", "Content-Type": "application/json"}
SAMPLE = ["GROW-509518460", "GROW-500941422", "GROW-480091780", "GROW-495690702", "GROW-490389457", "GROW-482117751", "GROW-459651149", "GROW-478553474", "GROW-465599973", "GROW-484330981", "GROW-501268166", "GROW-485496419", "GROW-484109432", "GROW-499799775", "GROW-500980765", "GROW-493465701"]
out = {}
for ext in SAMPLE:
    req = urllib.request.Request("https://api.fireberry.com/api/v3/query",
        data=json.dumps({"objectType": 1018,
            "fields": [{"name":"pcfExternalSoftwareID1"},{"name":"pcfPayedIncludingVAT"},{"name":"pcfPaymentDate"},{"name":"pcfReference"}],
            "pageSize": 2, "pageNumber": 1,
            "filter": [{"type":"and","conditions":[
                {"fieldName":"pcfExternalSoftwareID1","operator":"eq","value":ext}]}]}).encode(), headers=HDRS)
    r = urllib.request.urlopen(req, timeout=30)
    d = json.loads(r.read())
    rows = d.get("data", [])
    if rows:
        out[ext] = {"amount": rows[0].get("pcfPayedIncludingVAT"), "date": str(rows[0].get("pcfPaymentDate"))[:10], "ref": rows[0].get("pcfReference")}
import json as J
J.dump(out, open(r"C:\Users\sahar\Claude Code\RevitalYaish\_reconciliation\amount_audit.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("audited", len(out))
