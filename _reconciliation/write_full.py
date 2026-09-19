
import urllib.request, json, time, sys

HDRS = {"tokenid": "b06663c4-62df-41b7-9111-6653e6b54592", "Content-Type": "application/json"}
BASE = "https://api.fireberry.com"

def post(url, body):
    req = urllib.request.Request(url, data=json.dumps(body).encode(), headers=HDRS, method="POST")
    r = urllib.request.urlopen(req, timeout=60)
    return json.loads(r.read())

PLAN = json.load(open(r"C:\Users\sahar\Claude Code\RevitalYaish\_reconciliation\final_write_plan.json", encoding="utf-8"))
STATE_F = r"C:\Users\sahar\Claude Code\RevitalYaish\_reconciliation\write_state.json"
try:
    state = json.load(open(STATE_F, encoding="utf-8"))
except:
    state = {"done_sos": [], "done_docs": [], "errors": []}
done_sos = set(state["done_sos"])
done_docs = set(state["done_docs"])
METHOD_MAP = {"אשראי": 1, "Bit": 6, "ApplePay": 1, "GooglePay": 1}

for idx, entry in enumerate(PLAN):
    if entry["so_ext"] in done_sos:
        continue
    so_body = {
        "name": entry["so_name"],
        "pcfPaymentType": 7,
        "pcfNeedToPayIncludingVat": entry["amount"],
        "pcfAccountid": entry["account"],
        "pcfFirstPaymentDate": entry["first_date"] + " 00:00:00",
        "pcfExternalSoftwareID1": entry["so_ext"],
        "pcftaxincludecode": 1,
        "pcfCreatedByPersonOrSystem": 2,
    }
    try:
        r = post(BASE + "/api/record/1039", so_body)
        rec = r["data"]["Record"]
        rid = rec.get("customobject1039id") or rec.get("_id") or rec.get("id")
        entry_id = rid
        done_sos.add(entry["so_ext"])
        state["done_sos"] = list(done_sos)
    except Exception as e:
        body = getattr(e, "read", lambda: b"")()
        state["errors"].append({"so": entry["so_name"], "err": str(e)[:150], "body": body.decode("utf-8","ignore")[:200]})
        print("SO FAIL", entry["so_ext"], str(e)[:80], flush=True)
        json.dump(state, open(STATE_F, "w", encoding="utf-8"), ensure_ascii=False)
        time.sleep(1)
        continue
    # PUT N=0 (2יט gotcha: create without, update with)
    try:
        req = urllib.request.Request(f"{BASE}/api/record/1039/{entry_id}",
            data=json.dumps({"pcfNumberOfPayments": 0}).encode(), headers=HDRS, method="PUT")
        urllib.request.urlopen(req, timeout=60)
    except Exception as e:
        state["errors"].append({"so": entry["so_ext"], "err_put_n0": str(e)[:150]})
    # docs
    for ch in entry["charges"]:
        if ch["doc_ext"] in done_docs:
            continue
        doc_body = {
            "name": f'תיעוד התשלום הו"ק של {entry["customer"]} | {entry["product"]}',
            "pcfPaymentCollection": entry_id,
            "pcfAccountid": entry["account"],
            "pcfPaymetStatus": 1,
            "pcfPaymentDate": ch["date"] + " 00:00:00",
            "pcfPayedIncludingVAT": ch["amount"],
            "pcfReference": ch["ref"],
            "pcfExternalSoftwareID1": ch["doc_ext"],
            "pcfPaymentType": METHOD_MAP.get(ch["method"], 1),
            "pcftaxincludecode": 1,
            "pcfCreatedByPersonOrSystem": 2,
        }
        try:
            post(BASE + "/api/record/1018", doc_body)
            done_docs.add(ch["doc_ext"])
            state["done_docs"] = list(done_docs)
        except Exception as e:
            body = getattr(e, "read", lambda: b"")()
            state["errors"].append({"doc": ch["doc_ext"], "err": str(e)[:150], "body": body.decode("utf-8","ignore")[:200]})
            print("DOC FAIL", ch["doc_ext"], str(e)[:80], flush=True)
    if idx % 10 == 0:
        json.dump(state, open(STATE_F, "w", encoding="utf-8"), ensure_ascii=False)
        print(f"progress: {len(done_sos)} SOs, {len(done_docs)} docs, errors {len(state['errors'])}", flush=True)
    time.sleep(0.35)

json.dump(state, open(STATE_F, "w", encoding="utf-8"), ensure_ascii=False)
print("DONE:", len(done_sos), "SOs,", len(done_docs), "docs,", len(state["errors"]), "errors", flush=True)
