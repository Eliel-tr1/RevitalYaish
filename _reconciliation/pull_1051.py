import json, urllib.request, time
HDRS = {"tokenid": "b06663c4-62df-41b7-9111-6653e6b54592", "Content-Type": "application/json"}
FIELDS = [{"name":f} for f in ["name","pcfStatus","createdon","pcfStartDate","pcfEstimatedEndDate","pcfStatusUpdateTime","pcfaccountid","pcfaccountid_accountname","pcfProduct","pcfProductname","pcfSale"]]
allrows = []
for p in range(1, 30):
    d = json.loads(urllib.request.urlopen(urllib.request.Request("https://api.fireberry.com/api/v3/query",
      data=json.dumps({"objectType":"1051","fields":FIELDS,"pageSize":200,"pageNumber":p}).encode(), headers=HDRS), timeout=30).read().decode())
    rows = d.get("data", [])
    allrows.extend(rows)
    print("page", p, "cum", len(allrows), flush=True)
    if d.get("isLastPage") or not rows: break
    time.sleep(0.75)
json.dump(allrows, open("obj1051_all.json","w",encoding="utf-8"), ensure_ascii=False)
print("TOTAL:", len(allrows))
