
import urllib.request, json
HDRS = {"tokenid": "b06663c4-62df-41b7-9111-6653e6b54592", "Content-Type": "application/json"}
# probe: query object 1 returning _id and try eq on a known account guid
import sys
sys.path.insert(0, r"C:\Users\sahar\Claude Code\RevitalYaish\_reconciliation")
plan = json.load(open(r"C:\Users\sahar\Claude Code\RevitalYaish\_reconciliation\write_plan.json", encoding="utf-8"))
a0 = plan["accounts"][0]
req = urllib.request.Request("https://api.fireberry.com/api/v3/query",
    data=json.dumps({"objectType": 1,
        "fields": [{"name":"name"}],
        "pageSize": 5, "pageNumber": 1,
        "filter": [{"type":"and","conditions":[
            {"fieldName":"_id","operator":"eq","value":a0}]}]}).encode(), headers=HDRS)
try:
    r = urllib.request.urlopen(req, timeout=60)
    d = json.loads(r.read())
    print("eq _id:", len(d.get("data", [])), d.get("data", [{}])[0] if d.get("data") else "")
except Exception as e:
    body = getattr(e, "read", lambda: b"")()
    print("eq _id FAIL", body[:150])
# try 'accountid'
req = urllib.request.Request("https://api.fireberry.com/api/v3/query",
    data=json.dumps({"objectType": 1,
        "fields": [{"name":"name"}],
        "pageSize": 5, "pageNumber": 1,
        "filter": [{"type":"and","conditions":[
            {"fieldName":"accountid","operator":"eq","value":a0}]}]}).encode(), headers=HDRS)
try:
    r = urllib.request.urlopen(req, timeout=60)
    d = json.loads(r.read())
    print("eq accountid:", len(d.get("data", [])))
except Exception as e:
    body = getattr(e, "read", lambda: b"")()
    print("eq accountid FAIL", body[:150])
