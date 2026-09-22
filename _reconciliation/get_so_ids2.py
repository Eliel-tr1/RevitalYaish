
import urllib.request, json, time
HDRS = {"tokenid": "b06663c4-62df-41b7-9111-6653e6b54592", "Content-Type": "application/json"}
final = json.load(open(r"C:\Users\sahar\Claude Code\RevitalYaish\_reconciliation\final_write_plan.json", encoding="utf-8"))
EXTS = [f["so_ext"] for f in final]
# also fuzzy SOs

id_by_ext = {}
CH = 20
for i in range(0, len(EXTS), CH):
    chunk = EXTS[i:i+CH]
    req = urllib.request.Request("https://api.fireberry.com/api/v3/query",
        data=json.dumps({"objectType": 1039, "fields": [{"name":"pcfExternalSoftwareID1"}],
            "pageSize": 50, "pageNumber": 1,
            "filter": [{"type":"and","conditions":[
                {"fieldName":"pcfExternalSoftwareID1","operator":"eq-in","value":chunk}]}]}).encode(), headers=HDRS)
    d = {"data": []}
    for attempt in range(5):
        try:
            r = urllib.request.urlopen(req, timeout=45)
            d = json.loads(r.read()); break
        except Exception as e:
            print(f"chunk {i} attempt {attempt}: {str(e)[:60]}", flush=True)
            time.sleep(5)
    for x in d.get("data", []):
        id_by_ext[str(x.get("pcfExternalSoftwareID1")).strip()] = x["_id"]
    time.sleep(1.5)
json.dump(id_by_ext, open(r"C:\Users\sahar\Claude Code\RevitalYaish\_reconciliation\so_ids_by_ext.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("SO ids resolved:", len(id_by_ext), "of", len(EXTS))
