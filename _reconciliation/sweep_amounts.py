# -*- coding: utf-8 -*-
# Sweeper: find reco docs with null pcfPayed and PUT the correct amount, verify each, until clean.
import urllib.request, json, time, os

HDRS = {"tokenid": "b06663c4-62df-41b7-9111-6653e6b54592", "Content-Type": "application/json"}
BASE = "https://api.fireberry.com"
QURL = BASE + "/api/v3/query"

def post_json(url, body, method="POST"):
    req = urllib.request.Request(url, data=json.dumps(body).encode(), headers=HDRS, method=method)
    return json.loads(urllib.request.urlopen(req, timeout=45).read())

PAIRS = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "all_amount_pairs.json"), encoding="utf-8"))
AMT = dict((str(r), float(a)) for r, a in PAIRS)
REFS = [str(r) for r, a in PAIRS]

STATE_F = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sweep_state.json")
state = {"round": 0, "fixed_total": 0}
if os.path.exists(STATE_F):
    state = json.load(open(STATE_F, encoding="utf-8"))

CH = 20
for rnd in range(state.get("round", 0), 10):
    print(f"=== ROUND {rnd} ===", flush=True)
    nulls = []
    for i in range(0, len(REFS), CH):
        chunk = REFS[i:i+CH]
        try:
            d = post_json(QURL, {"objectType": 1018, "fields": [{"name":"pcfReference"},{"name":"pcfPayed"}],
                                 "pageSize": 50, "pageNumber": 1,
                                 "filter": [{"type":"and","conditions":[
                                     {"fieldName":"pcfReference","operator":"eq-in","value":chunk}]}]})
        except Exception as e:
            print("query fail", str(e)[:60], flush=True)
            time.sleep(5); continue
        for x in d.get("data", []):
            if x.get("pcfPayed") is None:
                ref = str(x.get("pcfReference") or "").strip()
                if ref in AMT:
                    nulls.append((ref, x["_id"]))
        time.sleep(0.8)
    print(f"nulls found: {len(nulls)}", flush=True)
    if not nulls:
        print("CLEAN", flush=True)
        state["round"] = rnd + 1
        json.dump(state, open(STATE_F, "w", encoding="utf-8"), ensure_ascii=False)
        break
    fixed = 0
    for ref, rid in nulls:
        payed = round(AMT[ref] / 1.18, 4)
        try:
            post_json(f"{BASE}/api/record/1018/{rid}", {"pcfPayed": payed}, method="PUT")
            fixed += 1
        except Exception as e:
            print("PUT fail", ref, str(e)[:60], flush=True)
        time.sleep(2.0)
    state["fixed_total"] += fixed
    state["round"] = rnd + 1
    json.dump(state, open(STATE_F, "w", encoding="utf-8"), ensure_ascii=False)
    print(f"fixed this round: {fixed} (total {state['fixed_total']})", flush=True)
    time.sleep(20)
print("SWEEP DONE", flush=True)
