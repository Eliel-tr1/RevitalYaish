
import urllib.request, json, time

HDRS = {"tokenid": "092ce1fa-833a-499b-a021-5edbecd753a0", "Content-Type": "application/json"}
URL = "https://api.fireberry.com/api/v3/query"

def fetch_all(object_type, fields, name):
    all_rows, page = [], 1
    while True:
        req = urllib.request.Request(URL,
            data=json.dumps({"objectType": object_type,
                             "fields": [{"name": f} for f in fields],
                             "pageSize": 500, "pageNumber": page}).encode(), headers=HDRS)
        for attempt in range(3):
            try:
                r = urllib.request.urlopen(req, timeout=60)
                d = json.loads(r.read()); break
            except Exception:
                if attempt == 2: raise
                time.sleep(2)
        rows = d.get("data", [])
        all_rows.extend(rows)
        if d.get("isLastPage") or not rows: break
        page += 1
        time.sleep(0.7)
    print(f"{name}: {len(all_rows)} rows, {page} pages", flush=True)
    return all_rows

out = {}
out["old_1004_leads"] = fetch_all(1004, ["name", "createdon", "pcfsystemfield101", "pcfsystemfield100", "pcfNewSystemId"], "1004 רישום שיווקי")
time.sleep(1)
out["old_1003_payments"] = fetch_all(1003, ["name", "createdon", "pcfsystemfield109", "pcfsystemfield108", "pcfsystemfield106", "pcfsystemfield107", "pcfsystemfield110", "pcfsystemfield111", "pcfsystemfield112", "pcfsystemfield113", "pcfsystemfield114", "pcfsystemfield115", "pcfNewSystemId"], "1003 תשלום")

with open(r"C:\Users\sahar\Claude Code\RevitalYaish\_reconciliation\old_crm_extract.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False)
print("saved", flush=True)
