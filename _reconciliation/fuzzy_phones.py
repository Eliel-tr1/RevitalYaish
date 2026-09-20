
import urllib.request, json
HDRS = {"tokenid": "b06663c4-62df-41b7-9111-6653e6b54592", "Content-Type": "application/json"}
def q(val):
    req = urllib.request.Request("https://api.fireberry.com/api/v3/query",
        data=json.dumps({"objectType": 1,
            "fields": [{"name":"accountname"},{"name":"telephone1"}],
            "pageSize": 5, "pageNumber": 1,
            "filter": [{"type":"or","conditions":[
                {"fieldName":"telephone1","operator":"eq","value":val},
                {"fieldName":"telephone2","operator":"eq","value":val}]}]}).encode(), headers=HDRS)
    try:
        r = urllib.request.urlopen(req, timeout=30)
        d = json.loads(r.read())
        return d.get("data", [])
    except:
        return []

def variants(p):
    out = set()
    for i in range(len(p)):
        for d in "0123456789":
            if d != p[i]:
                out.add(p[:i] + d + p[i+1:])
    return out

PHONES = ["0508680115", "0524153323", "0538249625", "0547887909"]
for p in PHONES:
    vs = variants(p)
    found = None
    for v in vs:
        rows = q(v)
        if rows:
            found = (v, rows[0].get("accountname"), rows[0].get("_id"))
            break
    print(p, "->", found)
