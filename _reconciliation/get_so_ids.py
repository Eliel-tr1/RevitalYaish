
import urllib.request, json, time
HDRS = {"tokenid": "b06663c4-62df-41b7-9111-6653e6b54592", "Content-Type": "application/json"}
final = json.load(open(r"C:\Users\sahar\Claude Code\RevitalYaish\_reconciliation\final_write_plan.json", encoding="utf-8"))
EXTS = [f["so_ext"] for f in final]
# also fuzzy SOs
fuzzy_sos = ["GROW-DD-RECO-" + a[:8].upper() + "-" + str(int(amt)) for a, amt in [(566.0,566),(425.0,425),(349.0,349)]]
id_by_ext = {}
CH = 20
for i in range(0, len(EXTS), CH):
    chunk = EXTS[i:i+CH]
    req = urllib.request.Request("https://api.fireberry.com/api/v3/query",
        data=json.dumps({"objectType": 1039, "fields": [{"name":"pcfExternalSoftwareID1"}],
            "pageSize": 50, "pageNumber": 1,
            "filter": [{"type":"and","conditions":[
                {"fieldName":"pcfExternalSoftwareID1","operator":"eq-in","value":chunk}]}]}).encode(), headers=HDRS)
    for attempt in range(3):
        try:
            r = urllib.request.urlopen(req, timeout=45)
            d = json.loads(r.read()); break
        except Exception:
            if attempt == 2: d = {"data": []}; break
            time.sleep(3)
    for x in d.get("data", []):
        id_by_ext[str(x.get("pcfExternalSoftwareID1")).strip()] = x["_id"]
    time.sleep(0.8)
json.dump(id_by_ext, open(r"C:\Users\sahar\Claude Code\RevitalYaish\_reconciliation\so_ids_by_ext.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("SO ids resolved:", len(id_by_ext), "of", len(EXTS))
