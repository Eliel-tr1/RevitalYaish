# v4 - תיקון היסט של עמודות (הנתונים היו 10 עמודות מתחת לכותרת של 11),
# מילוי קישור לכרטיס לקוח אמיתי (נשלף מפיירברי), קישור בעמודת תהליך מכירה לשיוך,
# וסימון צהוב לשדות שצריך למלא (החלטה + תהליך מכירה חסר).

import json, sys, csv, time, re
sys.path.insert(0, r"C:\Users\sahar\AppData\Local\hermes\skills\productivity\google-workspace\scripts")
from google_api import get_credentials
from googleapiclient.discovery import build
import urllib.request

FB_TOKEN = "b06663c4-62df-41b7-9111-6653e6b54592"
FB_HDRS = {"tokenid": FB_TOKEN, "Content-Type": "application/json"}
SHEET_ID = "1WRvZpzsQyEbCe1HyMXO4zxQaP-_uUE0yDA35mtZc8Jc"
CSV_PATH = r"C:\Users\sahar\Claude Code\RevitalYaish\לקוחה_להחלטה_רויטל_v3.csv"

# ---------- 1. קריאת ה-CSV ----------
with open(CSV_PATH, encoding="utf-8-sig") as f:
    reader = list(csv.reader(f))
header = reader[0]
data_rows = [r for r in reader[1:] if any(x.strip() for x in r)]
print(f"header cols: {len(header)}, data rows: {len(data_rows)}")

# ---------- 2. שליפת accountid לכל תיעוד תשלום (1018) ----------
def fb_q(fields, conds, page_size=20, max_pages=1):
    body = {"objectType": 1018, "fields": [{"name": f} for f in fields],
            "pageSize": page_size, "pageNumber": 1}
    if conds:
        body["filter"] = [{"type": "and", "conditions": conds}]
    req = urllib.request.Request("https://api.fireberry.com/api/v3/query",
        data=json.dumps(body).encode(), headers=FB_HDRS)
    try:
        d = json.loads(urllib.request.urlopen(req, timeout=30).read())
        return d.get("data") or []
    except urllib.error.HTTPError as e:
        print("FB FAIL:", e.read().decode()[:200]); return []

# מציאת ה-PK של 1018
req = urllib.request.Request("https://api.fireberry.com/api/query",
    data=json.dumps({"objecttype": 1018, "pageSize": 1}).encode(), headers=FB_HDRS)
meta = json.loads(urllib.request.urlopen(req, timeout=30).read()).get("data") or {}
PK = meta.get("PrimaryKey")
print("1018 PK:", PK)

# ה-GUIDs של התיעודים מתוך הקישורים בעמודה 2 (קישור לתיעוד תשלום)
doc_ids = []
for r in data_rows:
    m = re.search(r"/record/1018/([0-9a-fA-F-]{36})", r[1])
    if m:
        doc_ids.append(m.group(1).lower())
print("doc ids found:", len(doc_ids))

doc_to_acct = {}
for i in range(0, len(doc_ids), 20):
    chunk = doc_ids[i:i+20]
    conds = [{"fieldName": PK, "operator": "eq", "value": d} for d in chunk]
    body = {"objectType": 1018, "fields": [{"name": "pcfAccountid"}],
            "pageSize": 20, "pageNumber": 1,
            "filter": [{"type": "or", "conditions": conds}]}
    req = urllib.request.Request("https://api.fireberry.com/api/v3/query",
        data=json.dumps(body).encode(), headers=FB_HDRS)
    try:
        d = json.loads(urllib.request.urlopen(req, timeout=30).read())
        rows = d.get("data") or []
        for row in rows:
            rid = (row.get("_id") or "").lower()
            acct = row.get("pcfAccountid")
            if rid and acct:
                doc_to_acct[rid] = acct
    except urllib.error.HTTPError as e:
        print("FB FAIL:", e.read().decode()[:200])
    time.sleep(0.8)
print("accountids resolved:", len(doc_to_acct))

# ---------- 3. בניית השורות במיקומי העמודות הנכונים ----------
# header: [0]שם הלקוחה [1]קישור לכרטיס לקוח [2]קישור לתיעוד תשלום [3]קישור לתהליך מכירה לשיוך
#          [4]שם תהליך מכירה [5]סכום [6]תאריך [7]תיאור מגרואו [8]אסמכתא [9]פתרון במילים שלי [10]החלטה (מלא)
# ב-CSV הקיים הנתונים היו במיקום שגוי (אחרי שם הלקוחה היה קישור 1018, אחר-כך קישור 4,
# אחר-כך שם התהליך, אחר-כך סכום, תאריך, תיאור, אסמכתא, פתרון) - כלומר היה חסר עמודת כרטיס לקוח.
out = [header]
yellow_cells = []  # (row_idx, col_idx) 1-based for Sheets API

for i, r in enumerate(data_rows):
    # r היסטורי: [0]=שם [1]=קישור 1018 [2]=קישור 4 (או ריק) [3]=שם תהליך (או ריק)
    #             [4]=סכום [5]=תאריך [6]=תיאור [7]=אסמכתא [8]=פתרון [9]=החלטה(ריק)
    name      = r[0]
    link_doc  = r[1] if len(r) > 1 else ""
    link_opp  = r[2] if len(r) > 2 else ""
    opp_name  = r[3] if len(r) > 3 else ""
    amount    = r[4] if len(r) > 4 else ""
    date      = r[5] if len(r) > 5 else ""
    desc      = r[6] if len(r) > 6 else ""
    asmachta  = r[7] if len(r) > 7 else ""
    solution  = r[8] if len(r) > 8 else ""

    # כרטיס לקוח: מה-GUID של התיעוד -> accountid -> קישור אובייקט 1
    m = re.search(r"/record/1018/([0-9a-fA-F-]{36})", link_doc or "")
    acct_link = ""
    if m:
        acct = doc_to_acct.get(m.group(1).lower())
        if acct:
            acct_link = f"https://app.fireberry.com/app/record/1/{acct.lower()}"

    # קישור לתהליך מכירה לשיוך: אם יש קישור 4 זה המקור; אם רק שם תהליך קיים בלי קישור - נשים קישור על השם בעמודה זו
    opp_cell = link_opp or (opp_name if opp_name else "")

    row = [name, acct_link, link_doc, opp_cell, opp_name, amount, date, desc, asmachta, solution, ""]
    out.append(row)

    # צהוב: עמודת החלטה (10) תמיד צריכה מילוי; תהליך מכירה (3/4) כשריק
    yellow_cells.append((i + 2, 11))           # עמודת החלטה (מלא)
    if not link_opp:
        yellow_cells.append((i + 2, 4))        # קישור לתהליך מכירה לשיוך

print("rows built:", len(out) - 1, "yellow cells:", len(yellow_cells))

# ---------- 4. כתיבה לגוגל שיטס ----------
creds = get_credentials()
service = build("sheets", "v4", credentials=creds)

service.spreadsheets().values().clear(spreadsheetId=SHEET_ID, range="Sheet1").execute()
time.sleep(2)

body = {"values": out}
result = service.spreadsheets().values().update(
    spreadsheetId=SHEET_ID, range="Sheet1!A1", valueInputOption="RAW", body=body).execute()
print(f"Updated: {result.get('updatedCells')} cells, {result.get('updatedRows')} rows")

# ---------- 5. צביעה צהובה ----------
requests = []
for row, col in yellow_cells:
    requests.append({
        "repeatCell": {
            "range": {"sheetId": 0, "startRowIndex": row - 1, "endRowIndex": row,
                      "startColumnIndex": col - 1, "endColumnIndex": col},
            "cell": {"userEnteredFormat": {
                "backgroundColor": {"red": 1.0, "green": 0.918, "blue": 0.235},
                "horizontalAlignment": "RIGHT"}},
            "fields": "userEnteredFormat.backgroundColor,userEnteredFormat.horizontalAlignment"
        }
    })
if requests:
    service.spreadsheets().batchUpdate(spreadsheetId=SHEET_ID, body={"requests": requests}).execute()
    print(f"Yellow-painted {len(requests)} cells")