
import urllib.request, json, random, time
HDRS = {"tokenid": "b06663c4-62df-41b7-9111-6653e6b54592", "Content-Type": "application/json"}
plan = json.load(open(r"C:\Users\sahar\Claude Code\RevitalYaish\_reconciliation\final_write_plan.json", encoding="utf-8"))
random.seed(42)
sample = []
for f in random.sample(plan, 10):
    for ch in random.sample(f["charges"], min(2, len(f["charges"]))):
        sample.append((ch["ref"], ch["amount"]))
grow = json.load(open(r"C:\Users\sahar\Claude Code\RevitalYaish\_reconciliation\grow_transactions_full.json", encoding="utf-8"))
gmap = {t["ref_grow"]: t for t in grow if t["status"] == "חוייב"}

bad = 0
for ref, expected in sample:
    req = urllib.request.Request("https://api.fireberry.com/api/v3/query",
        data=json.dumps({"objectType": 1018,
            "fields": [{"name":"pcfPayedIncludingVAT"},{"name":"pcfPayed"}],
            "pageSize": 1, "pageNumber": 1,
            "filter": [{"type":"and","conditions":[
                {"fieldName":"pcfReference","operator":"eq","value":ref}]}]}).encode(), headers=HDRS)
    r = urllib.request.urlopen(req, timeout=30)
    rows = json.loads(r.read()).get("data", [])
    got = rows[0].get("pcfPayedIncludingVAT") if rows else None
    t = gmap.get(ref)
    if t is None or got is None or abs(got - (t["amount_paid"] or 0)) > 0.05:
        print("BAD", ref, "expected", t["amount_paid"] if t else "?", "got", got)
        bad += 1
    time.sleep(0.3)
print(f"AUDIT: {len(sample)} sampled, {bad} bad")
