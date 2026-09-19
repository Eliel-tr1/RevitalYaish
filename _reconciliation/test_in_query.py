
import urllib.request, json
HDRS = {"tokenid": "b06663c4-62df-41b7-9111-6653e6b54592", "Content-Type": "application/json"}
vals = ["0503777229", "+972505322537", "0503707090", "972544250476", "+972506988922", "972504245328", "0505583478", "+972527734568", "0544866125", "0529202692", "0505521006", "0507723774", "0544945992", "0547565258", "+972523316862", "+972522482370", "+972508329219", "0526344722", "+972542584103", "+972503707090"]
req = urllib.request.Request("https://api.fireberry.com/api/v3/query",
    data=json.dumps({"objectType": 1,
        "fields": [{"name":"telephone1"},{"name":"telephone2"}],
        "pageSize": 50, "pageNumber": 1,
        "filter": [{"type":"or","conditions":[
            {"fieldName":"telephone1","operator":"in","value":vals},
            {"fieldName":"telephone2","operator":"in","value":vals}]}]}).encode(), headers=HDRS)
try:
    r = urllib.request.urlopen(req, timeout=60)
    d = json.loads(r.read())
    rows = d.get("data", [])
    print("matched accounts:", len(rows))
    for x in rows[:5]: print("  ", json.dumps(x, ensure_ascii=False))
except Exception as e:
    body = getattr(e, "read", lambda: b"")()
    print("FAIL", e, body[:200])
