
import urllib.request, json, time, sys

HDRS = {"tokenid": "b06663c4-62df-41b7-9111-6653e6b54592", "Content-Type": "application/json"}
BASE = "https://api.fireberry.com"

def post(url, body):
    req = urllib.request.Request(url, data=json.dumps(body).encode(), headers=HDRS, method="POST")
    r = urllib.request.urlopen(req, timeout=60)
    return json.loads(r.read())

def put(url, body):
    req = urllib.request.Request(url, data=json.dumps(body).encode(), headers=HDRS, method="PUT")
    r = urllib.request.urlopen(req, timeout=60)
    return json.loads(r.read())

PLAN = json.load(open(r"C:\Users\sahar\Claude Code\RevitalYaish\_reconciliation\final_write_plan.json", encoding="utf-8"))
METHOD_MAP = {"אשראי": 1, "Bit": 6, "ApplePay": 1, "GooglePay": 1}

DRY = "--execute" not in sys.argv
N = int(sys.argv[sys.argv.index("--n") + 1]) if "--n" in sys.argv else 3
results = {"created_sos": 0, "created_docs": 0, "errors": []}

for entry in PLAN[:N]:
    # 1. Create SO
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
    if DRY:
        print("[DRY] SO:", entry["so_name"])
    else:
        try:
            r = post(BASE + "/api/record/1039", so_body)
            rid = r["data"]["Record"].get("customobject1039id") or r["data"]["Record"].get("_id")
            entry["_created_so_id"] = rid
            results["created_sos"] += 1
            print("SO OK", rid, flush=True)
            # PUT numberOfPayments=0 (2יט: create without, update with)
            try:
                put(f"{BASE}/api/record/1039/{rid}", {"pcfNumberOfPayments": 0})
            except Exception as e:
                print("  PUT N=0 failed:", str(e)[:80], flush=True)
        except Exception as e:
            body = getattr(e, "read", lambda: b"")()
            results["errors"].append({"so": entry["so_name"], "err": str(e), "body": body.decode("utf-8", "ignore")[:200]})
            print("SO FAIL", str(e)[:100], flush=True)
            continue
    # 2. Docs
    for ch in entry["charges"]:
        doc_body = {
            "name": f'תיעוד התשלום הו"ק של {entry["customer"]} | {entry["product"]}',
            "pcfPaymentCollection": entry.get("_created_so_id") if entry.get("_created_so_id") else None,
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
        if doc_body["pcfPaymentCollection"] is None:
            doc_body.pop("pcfPaymentCollection")
        if DRY:
            print("   [DRY] doc:", ch["date"], ch["amount"], ch["doc_ext"])
        else:
            try:
                r2 = post(BASE + "/api/record/1018", doc_body)
                results["created_docs"] += 1
            except Exception as e:
                body = getattr(e, "read", lambda: b"")()
                results["errors"].append({"doc": ch["doc_ext"], "err": str(e), "body": body.decode("utf-8", "ignore")[:200]})
                print("  DOC FAIL", ch["doc_ext"], str(e)[:100], flush=True)
    time.sleep(0.5)

json.dump(results, open(r"C:\Users\sahar\Claude Code\RevitalYaish\_reconciliation\pilot_results.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps(results, ensure_ascii=False, indent=1)[:1500])
