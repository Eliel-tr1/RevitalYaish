
import urllib.request, json
HDRS = {"tokenid": "092ce1fa-833a-499b-a021-5edbecd753a0", "Content-Type": "application/json"}
# old account phone format: telephone1
def q(phone):
    req = urllib.request.Request("https://api.fireberry.com/api/v3/query",
        data=json.dumps({"objectType": 1,
            "fields": [{"name":"telephone1"}],  # account has no name field in old!
            "pageSize": 5, "pageNumber": 1,
            "filter": [{"type":"or","conditions":[
                {"fieldName":"telephone1","operator":"eq","value":phone},
                {"fieldName":"telephone2","operator":"eq","value":phone}]}]}).encode(), headers=HDRS)
    try:
        r = urllib.request.urlopen(req, timeout=30)
        return json.loads(r.read()).get("data", [])
    except Exception as e:
        body = getattr(e, "read", lambda: b"")()
        print("FAIL", body[:100]); return []

rows = q("0524153323")
print("old CRM 0524153323:", len(rows))
if rows:
    # get full record
    rid = rows[0]["accountid"]
    req = urllib.request.Request(f"https://api.fireberry.com/api/v3/query",
        data=json.dumps({"objectType": 1, "fields": [{"name":"telephone1"}], "pageSize": 1, "pageNumber": 1,
            "filter": [{"type":"and","conditions":[{"fieldName":"accountid","operator":"eq","value":rid}]}]}).encode(), headers=HDRS)
    print("found in OLD CRM - needs migration or manual handling")
