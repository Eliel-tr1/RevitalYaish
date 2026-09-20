
import urllib.request, json, time
HDRS = {"tokenid": "b06663c4-62df-41b7-9111-6653e6b54592", "Content-Type": "application/json"}
PAIRS = json.load(open(r"C:\Users\sahar\Claude Code\RevitalYaish\_reconciliation\all_amount_pairs.json", encoding="utf-8"))
AMT = dict((str(r), float(a)) for r, a in PAIRS)
REFS = [str(r) for r, a in PAIRS]
bad = []
ok = 0
CH = 20
for i in range(0, len(REFS), CH):
    chunk = REFS[i:i+CH]
    req = urllib.request.Request("https://api.fireberry.com/api/v3/query",
        data=json.dumps({"objectType": 1018,
            "fields": [{"name":"pcfReference"},{"name":"pcfPayedIncludingVAT"}],
            "pageSize": 50, "pageNumber": 1,
            "filter": [{"type":"and","conditions":[
                {"fieldName":"pcfReference","operator":"eq-in","value":chunk}]}]}).encode(), headers=HDRS)
    for attempt in range(3):
        try:
            r = urllib.request.urlopen(req, timeout=45)
            d = json.loads(r.read()); break
        except Exception:
            if attempt == 2: d = {"data": []}; break
            time.sleep(5)
    for x in d.get("data", []):
        ref = str(x.get("pcfReference") or "").strip()
        got = x.get("pcfPayedIncludingVAT")
        exp = AMT.get(ref)
        if got is None or exp is None or abs(got - exp) > 0.05:
            bad.append({"ref": ref, "expected": exp, "got": got})
        else:
            ok += 1
    if (i//CH) % 15 == 0:
        print(f"checked {i+len(chunk)}/{len(REFS)} ok={ok} bad={len(bad)}", flush=True)
    time.sleep(0.8)
json.dump(bad, open(r"C:\Users\sahar\Claude Code\RevitalYaish\_reconciliation\final_amount_audit.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"FINAL AMOUNT AUDIT: ok={ok} bad={len(bad)}", flush=True)
