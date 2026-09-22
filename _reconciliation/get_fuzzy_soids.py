
import urllib.request, json
HDRS = {"tokenid": "b06663c4-62df-41b7-9111-6653e6b54592", "Content-Type": "application/json"}
EXTS = ["GROW-DD-RECO-5B8578DA-425", "GROW-DD-RECO-5B8578DA-425", "GROW-DD-RECO-5B8578DA-425", "GROW-DD-RECO-5B8578DA-425", "GROW-DD-RECO-5B8578DA-425", "GROW-DD-RECO-5B8578DA-425", "GROW-DD-RECO-5B8578DA-425", "GROW-DD-RECO-5B8578DA-425", "GROW-DD-RECO-CCFBDCF8-566", "GROW-DD-RECO-CCFBDCF8-566", "GROW-DD-RECO-CCFBDCF8-566", "GROW-DD-RECO-CCFBDCF8-566", "GROW-DD-RECO-CCFBDCF8-566", "GROW-DD-RECO-CCFBDCF8-566", "GROW-DD-RECO-CCFBDCF8-566", "GROW-DD-RECO-CCFBDCF8-566", "GROW-DD-RECO-228683DF-349", "GROW-DD-RECO-228683DF-349"]
out = {}
for ext in EXTS:
    req = urllib.request.Request("https://api.fireberry.com/api/v3/query",
        data=json.dumps({"objectType": 1039, "fields": [{"name":"pcfExternalSoftwareID1"}],
            "pageSize": 2, "pageNumber": 1,
            "filter": [{"type":"and","conditions":[
                {"fieldName":"pcfExternalSoftwareID1","operator":"eq","value":ext}]}]}).encode(), headers=HDRS)
    r = urllib.request.urlopen(req, timeout=30)
    rows = json.loads(r.read()).get("data", [])
    if rows: out[ext] = rows[0]["_id"]
    else: out[ext] = None
    print(ext, "->", out[ext], flush=True)
import json as J
J.dump(out, open(r"C:\Users\sahar\Claude Code\RevitalYaish\_reconciliation\fuzzy_so_ids.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
