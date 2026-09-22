
import urllib.request, json
HDRS = {"tokenid": "b06663c4-62df-41b7-9111-6653e6b54592", "Content-Type": "application/json"}
IDS = ["1C3B1868-147C-48E2-B156-1A232A389081", "45C995F8-570A-4FC5-94C0-DE9B7C297811", "6782FB9F-2010-4CA7-8F58-8190DDFD5F4D", "6936C16C-B500-4D74-BBBD-41A97FFA009E", "7D684B1D-D138-4F70-815C-B239312C9A95", "7E0B4F2A-19E9-4F20-B312-44E8AB5E5871", "84978719-E890-477F-8FDD-BD1A193507F2", "85AE7F76-5E7C-427B-92C9-205A2B06167F", "AEB5CCC9-4622-4942-A1CC-68034D8D93F2", "DEF4481A-8664-47EE-8C81-054F47A952A0"]
out = {}
for rid in IDS:
    req = urllib.request.Request("https://api.fireberry.com/api/v3/query",
        data=json.dumps({"objectType": 1039, "fields": [{"name":"name"},{"name":"pcfExternalSoftwareID1"}],
            "pageSize": 1, "pageNumber": 1,
            "filter": [{"type":"and","conditions":[
                {"fieldName":"customobject1039id","operator":"eq","value":rid}]}]}).encode(), headers=HDRS)
    try:
        r = urllib.request.urlopen(req, timeout=30)
        d = json.loads(r.read())
        rows = d.get("data", [])
        if rows:
            out[rid] = {"name": rows[0].get("name"), "ext": rows[0].get("pcfExternalSoftwareID1")}
    except Exception as e:
        print("fail", rid[:8], str(e)[:60])
import json as J
J.dump(out, open(r"C:\Users\sahar\Claude Code\RevitalYaish\_reconciliation\target_names.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("got", len(out), "of", len(IDS))
