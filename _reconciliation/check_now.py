
import urllib.request, json
HDRS = {"tokenid": "b06663c4-62df-41b7-9111-6653e6b54592", "Content-Type": "application/json"}
# Query for this specific record NOW
req = urllib.request.Request("https://api.fireberry.com/api/v3/query",
    data=json.dumps({"objectType": 4, "fields": [{"name":"name"},{"name":"statuscode"},{"name":"accountid"}],
        "pageSize": 5, "pageNumber": 1,
        "filter": [{"type":"and","conditions":[
            {"fieldName":"accountid","operator":"eq","value":"78905DBF-AA35-4406-8520-E5628DBB7C60"}]}]}).encode(), headers=HDRS)
r = urllib.request.urlopen(req, timeout=30)
d = json.loads(r.read())
rows = d.get("data", [])
print(f"אורטל קלנדרוב - תהליכי מכירה כרגע ב-API: {len(rows)}")
for x in rows:
    print(f"  {x['_id']} | {x.get('name')} | status={x.get('statuscode')}")
print()
print("d0b72253 נמצא:", any(x["_id"].lower() == "d0b72253-04ef-4cb2-9de4-b5d9ec111118" for x in rows))
