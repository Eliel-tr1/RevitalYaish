
import urllib.request, json
HDRS = {"tokenid": "b06663c4-62df-41b7-9111-6653e6b54592", "Content-Type": "application/json"}
def q(fields, flt=None, n=5):
    body = {"objectType": 4, "fields": [{"name": f} for f in fields], "pageSize": n, "pageNumber": 1}
    if flt: body["filter"] = flt
    req = urllib.request.Request("https://api.fireberry.com/api/v3/query", data=json.dumps(body).encode(), headers=HDRS)
    r = urllib.request.urlopen(req, timeout=30)
    return json.loads(r.read()).get("data", [])

# Sample: name + statuscode + product + close date for a few recent
rows = q(["name","statuscode","pcfProduct","pcfclosedate","pcfincomingcashflow","createdon"])
print("sample type 4 records:")
for x in rows[:5]:
    print("  ", json.dumps(x, ensure_ascii=False)[:220])
# statuscode distribution over sample
from collections import Counter
rows2 = q(["statuscode"], n=500)
print("statuscode sample 500:", Counter(str(x.get("statuscode")) for x in rows2))
