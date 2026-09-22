
import urllib.request, json
HDRS = {"tokenid": "b06663c4-62df-41b7-9111-6653e6b54592", "Content-Type": "application/json"}
# Query all opps for account 78905DBF (אורטל קלנדרוב)
req = urllib.request.Request("https://api.fireberry.com/api/v3/query",
    data=json.dumps({"objectType": 4, "fields": [{"name":"name"},{"name":"statuscode"},{"name":"createdon"}],
        "pageSize": 20, "pageNumber": 1,
        "filter": [{"type":"and","conditions":[
            {"fieldName":"accountid","operator":"eq","value":"78905DBF-AA35-4406-8520-E5628DBB7C60"}]}]}).encode(), headers=HDRS)
r = urllib.request.urlopen(req, timeout=30)
d = json.loads(r.read())
print(f"תהליכי מכירה לאורטל קלנדרוב: {len(d.get('data', []))}")
for x in d.get("data", []):
    print(f"  {x['_id']} | {x.get('name')} | {x.get('statuscode')} | {str(x.get('createdon'))[:16]}")
