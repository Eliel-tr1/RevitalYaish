#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ROITAL YAISH · FIREBERRY HEALTH MONITOR
בדיקת תקינות אוטומטית · לקריאה בלבד · אפס כתיבה למערכות
"""
import json, os, re, sys, ssl, time, urllib.request, urllib.error
from datetime import datetime, timezone, timedelta
from collections import defaultdict, Counter

FB_TOKEN = os.environ.get("FB_TOKEN", "b06663c4-62df-41b7-9111-6653e6b54592")
FB_BASE  = "https://api.fireberry.com"
N8N_KEY  = os.environ.get("N8N_KEY", "")
N8N_BASE = os.environ.get("N8N_BASE", "https://n8n.srv964196.hstgr.cloud")
CC_KEY   = os.environ.get("CC_KEY", "")
CC_BASE  = "https://console.thecloud.chat/api"
MAKE_KEY = os.environ.get("MAKE_KEY", "")
MAKE_ZONE= os.environ.get("MAKE_ZONE", "eu2.make.com")
MAKE_TEAM= os.environ.get("MAKE_TEAM", "")

IL = timezone(timedelta(hours=3))
NOW = datetime.now(IL)
OUT = os.path.dirname(os.path.abspath(__file__))
ERRORS = []          # תקלות תשתית בבדיקה עצמה
MIGRATION_END = datetime(2026, 9, 11, 14, 58, tzinfo=IL)  # סוף אצוות ההגירה

# ---------------------------------------------------------------- HTTP
def _http(url, headers, method="GET", body=None, timeout=90):
    data = json.dumps(body).encode() if body is not None else None
    r = urllib.request.Request(url, data=data, headers=headers, method=method)
    last = None
    for attempt in range(4):
        try:
            with urllib.request.urlopen(r, timeout=timeout) as f:
                return json.loads(f.read().decode())
        except urllib.error.HTTPError as e:
            last = "HTTP %s %s" % (e.code, e.read()[:200])
            if e.code in (429, 500, 502, 503, 504):
                time.sleep(3 * (attempt + 1)); continue
            break
        except Exception as e:
            last = str(e); time.sleep(3 * (attempt + 1))
    raise RuntimeError("%s -> %s" % (url, last))

def fb_query(ot, fields, page=1, ps=500):
    b = {"objecttype": ot, "page_size": ps, "page_number": page, "fields": fields}
    return _http(FB_BASE + "/api/query", {"tokenid": FB_TOKEN, "Content-Type": "application/json"}, "POST", b)

def fb_all(ot, fields, cap=40000, label=""):
    rows, p = [], 1
    while True:
        try:
            d = fb_query(ot, fields, p)
        except Exception as e:
            ERRORS.append("שליפת %s (אובייקט %s) נכשלה בעמוד %s: %s" % (label or ot, ot, p, e)); break
        dd = d.get("data") or {}
        batch = dd.get("Data") or []
        rows += batch
        if dd.get("IsLastPage") or not batch or len(rows) >= cap: break
        p += 1
        if p > 200: break
    return rows

_FLD_CACHE={}
def fb_known_fields(ot):
    if ot in _FLD_CACHE: return _FLD_CACHE[ot]
    try:
        d=_http(FB_BASE+"/metadata/records/%s/fields"%ot,{"tokenid":FB_TOKEN}) or {}
        _FLD_CACHE[ot]={f.get("fieldName") for f in (d.get("data") or [])}
    except Exception as e:
        ERRORS.append("מטא-דאטה לאובייקט %s נכשל: %s"%(ot,e)); _FLD_CACHE[ot]=set()
    return _FLD_CACHE[ot]

def _probe(ot, flds):
    """True אם השאילתה עם רשימת השדות הזו מחזירה שורות"""
    try:
        dd=(fb_query(ot, ",".join(flds), 1, 50).get("data") or {})
        return bool(dd.get("Data"))
    except Exception:
        return False

def safe_fields(ot, wanted, label=""):
    """פיירברי מחזיר 0 שורות בשקט או 400 על שדה פגום. מנפים אותו במקום להחזיר דוח ריק."""
    known=fb_known_fields(ot)
    flds=[f for f in wanted.split(",") if f.strip()]
    unknown=[f for f in flds if known and f not in known]
    if unknown:
        ERRORS.append("שדות שאינם קיימים ב%s הושמטו: %s"%(label or ot, ", ".join(unknown)))
        flds=[f for f in flds if f not in unknown]
    if not flds: return ""
    if _probe(ot, flds): return ",".join(flds)
    # יש שדה פגום — מנפים בחיפוש בינארי על בסיס שדה עוגן תקין
    anchor=next((f for f in flds if _probe(ot,[f])), None)
    if anchor is None:
        ERRORS.append("אובייקט %s: אף שדה לא החזיר שורות — ייתכן שהאובייקט ריק"%(label or ot)); return ",".join(flds)
    good=[anchor]; bad=[]
    for f in flds:
        if f==anchor: continue
        if _probe(ot, good+[f]): good.append(f)
        else: bad.append(f)
    if bad: ERRORS.append("שדות פגומים ב%s הושמטו (פיירברי דוחה אותם): %s"%(label or ot, ", ".join(bad)))
    return ",".join(good)

def fb_meta_fields(ot):
    try:
        return (_http(FB_BASE + "/metadata/records/%s/fields" % ot, {"tokenid": FB_TOKEN}) or {}).get("data") or []
    except Exception as e:
        ERRORS.append("מטא-דאטה לאובייקט %s נכשל: %s" % (ot, e)); return []

def fb_meta_required(ot):
    """שדות חובה אמיתיים — מתוך Columns של השאילתה (isrequired)"""
    try:
        dd = (fb_query(ot, "", 1, 1).get("data") or {})
        return [c for c in (dd.get("Columns") or []) if c.get("isrequired")]
    except Exception:
        return []

# ---------------------------------------------------------------- utils
def dt(s):
    if not s: return None
    s = str(s).replace("Z", "").replace("T", " ").strip()
    for f in ("%Y-%m-%d %H:%M:%S.%f", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%d"):
        try: return datetime.strptime(s[:26], f).replace(tzinfo=IL)
        except Exception: pass
    return None

def blank(v):
    return v is None or str(v).strip() in ("", "None", "null", "0000-00-00")

def norm_phone(v):
    if blank(v): return ""
    d = re.sub(r"\D", "", str(v))
    if d.startswith("972"): d = "0" + d[3:]
    if len(d) == 9 and d[0] != "0": d = "0" + d
    return d

def valid_phone(v):
    d = norm_phone(v)
    return bool(re.fullmatch(r"0(5\d{8}|[2-489]\d{7})", d))

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[A-Za-z]{2,}$")
def valid_email(v): return bool(v) and bool(EMAIL_RE.match(str(v).strip()))

def looks_unnamed(n):
    if blank(n): return True
    s = str(n).strip()
    if re.fullmatch(r"[\d\-\+\s\(\)]{5,}", s): return True   # שם שהוא טלפון
    if s.lower() in ("ליד חדש","לקוח","לקוחה","test","טסט","בדיקה","unknown","null","-","new lead"): return True
    if len(s) < 2: return True
    return False

FINDINGS = []
BACKLOG = []

# ---------------------------------------------------------------- החרגות ידניות
EXC = {}
try:
    EXC = json.load(open(os.path.join(OUT, "exclusions.json")))
except Exception as e:
    ERRORS.append("exclusions.json לא נטען (%s) — הבדיקה רצה בלי החרגות ידניות" % e)
DISABLED = EXC.get("disabled_checks") or {}
SEV_OVR  = EXC.get("severity_overrides") or {}
OWN_OVR  = EXC.get("owner_overrides") or {}
NOTE_OVR = EXC.get("note_overrides") or {}
REC_EXC  = EXC.get("record_exclusions") or {}
PARKED   = EXC.get("parked_checks") or {}
OPER     = EXC.get("operational_checks") or {}
BASELINE = EXC.get("baselines") or {}
MAINT    = EXC.get("maintenance_windows") or []

def in_maintenance(d0):
    """True אם הרגע נופל בתוך חלון ריצה מאסיבית מוצהר"""
    for w in MAINT:
        a, b = dt(w.get("from")), dt(w.get("to"))
        if a and b and a <= d0 <= b: return w.get("reason") or "חלון תחזוקה מוצהר"
    return None

def excluded_ids(code):
    return set((REC_EXC.get(code) or {}).keys())

def drop_excluded(code, rows, idkey):
    """מסנן רשומות שהוחרגו ידנית, ומדווח כמה הוסרו"""
    ex = excluded_ids(code)
    if not ex: return rows
    keep = [r for r in rows if str(r.get(idkey) or "").lower() not in {e.lower() for e in ex}]
    return keep

def add(code, sev, title, count, sample=None, note="", owner="", backlog=None):
    if code in DISABLED:
        return                      # בדיקה שכובתה במפורש — לא נכנסת לדוח כלל
    sev = SEV_OVR.get(code, sev)
    owner = OWN_OVR.get(code, owner)
    note = NOTE_OVR.get(code, note)
    FINDINGS.append({"code": code, "sev": sev, "title": title, "count": int(count),
                     "sample": sample or [], "note": note, "owner": owner,
                     "backlog": (int(backlog) if backlog is not None else None)})
def addlog(title, count, note=""):
    if count: BACKLOG.append({"title": title, "count": int(count), "note": note})

def fb_link(ot, rid):
    return "https://app.fireberry.com/view?objecttype=%s&objectid=%s" % (ot, rid)

# ================================================================ FETCH
print("... שולף נתונים מפיירברי", file=sys.stderr)
ACC_F = "accountid,accountname,telephone1,telephone2,emailaddress1,createdon,modifiedon,statuscode,ownerid,pcfCloudChatId,pcfUTMSsource,pcfType,pcfWhatsAppReferans,pcfLegacyCreatedOn,pcfCreatedByPersonOrSystem,idnumber,pcfGender,billingcity,pcfChargeCompanyNumber"
accounts = fb_all(1, safe_fields(1, ACC_F, "לקוחות"), label="לקוחות")
OPP_F = "opportunityid,name,accountid,statuscode,createdon,modifiedon,pcfTelephone1,pcfemailaddress,pcfProduct,pcfCourse,pcfBoostLinked,ownerid,pcfclosedate,pcfRevenue,pcfmoneypaid1,pcfdayspast,pcfStatusUpdateTime,contacttid,pcfWhatsAppToRef,pcfSignatureStatus,pcfLastentry,pcfUTMSsource,pcfCreatedByPersonOrSystem"
opps = fb_all(4, safe_fields(4, OPP_F, "תהליכי מכירה"), label="תהליכי מכירה")
MEN_F = "customobject1051id,name,pcfaccountid,pcfSale,pcfStatus,pcfStartDate,pcfEstimatedEndDate,createdon,modifiedon,pcfBoostLinked,pcfActualGroup,pcfProduct,pcfWelcomeSent,pcfCurrentProgram,pcfWeeksNumber,ownerid,pcfcrmorderid,pcfLegacyCreatedOn,pcfCurrentWeight,pcfInitialWeight,pcfTargetWeight,pcfLastWeighDate,pcfCurrentWeek"
mentor = fb_all(1051, safe_fields(1051, MEN_F, "תהליכי ליווי"), label="תהליכי ליווי")
PAY_F = "customobject1039id,name,pcfAccountid,pcfSale,pcfStatus,pcfNeedToPayIncludingVat,pcfTotalPaidIncludingVat,pcfLeftToPayIncludingVat,createdon,modifiedon,pcfFirstPaymentDate,pcfNextPaymentDate,pcfPaymentType,pcfPaymentCategory,pcfNumberOfPayments,pcfrelatedproduct,pcfOrder,pcfDelayOnPayment,pcfLegacyCreatedOn"
pays = fb_all(1039, safe_fields(1039, PAY_F, "תשלומים"), label="תשלומים")
DOC_F = "customobject1018id,name,pcfAccountid,pcfSale,pcfPayed,pcfPayedIncludingVAT,pcfPaymentDate,createdon,pcfPaymetStatus,pcfInvoiceNumber,pcfReference,pcfPaymentCollection,pcfPaymentType"
paydocs = fb_all(1018, safe_fields(1018, DOC_F, "תיעודי תשלום"), label="תיעודי תשלום")
COH_F = "customobject1007id,name,pcfStatus,pcfStartDate,pcfEndDate,pcfStartSaleDate,pcfEndSaleDate,pcfEventLink,pcfwhatspgrouprelated,pcfRegistration,pcfRegistrationQuota,pcfOpertuintyCount,pcfBoostCount,pcfWebinarAttended,pcfWebinarRegistered,pcfProductId,createdon,pcfWebinarPulledAt"
cohorts = fb_all(1007, safe_fields(1007, COH_F, "מחזורי בוסט"), label="מחזורי בוסט")
GRP_F = "customobject1068id,name,pcfGroupLink,pcfGreenApiId,pcfGroupStatus,pcfCurrentCount,pcfCapacity,pcfAvailableSlots,pcfCurrentProgram,createdon"
groups = fb_all(1068, safe_fields(1068, GRP_F, "קבוצות וואטסאפ"), label="קבוצות וואטסאפ")
EVR_F = "customobject1030id,name,pcfAccountid,pcfSale,pcfEventId,pcfStatus,createdon,pcfProductId"
evregs = fb_all(1030, safe_fields(1030, EVR_F, "הרשמות לאירוע"), label="הרשמות לאירוע")
CON_F = "contactid,fullname,firstname,lastname,accountid,emailaddress1,telephone1,mobilephone1,createdon"
contacts = fb_all(2, safe_fields(2, CON_F, "אנשי קשר"), label="אנשי קשר")
TSK_F = "taskid,subject,pcfClient,pcfSale,statuscode,scheduledend,pcfexecutiondate,createdon,ownerid,modifiedon"
tasks = fb_all(10, safe_fields(10, TSK_F, "משימות"), label="משימות")
ACT_F = "activityid,subject,pcfClient,pcfSale,statuscode,scheduledstart,scheduledend,createdon,ownerid"
acts = fb_all(6, safe_fields(6, ACT_F, "פגישות"), label="פגישות")
SGN_F = "customobject1058id,name,createdon"
signs = fb_all(1058, safe_fields(1058, SGN_F, "מסמכים לחתימה"), label="מסמכים לחתימה")
WGH_F = "customobject1069id,name,createdon"
weigh = fb_all(1069, safe_fields(1069, WGH_F, "טפסי שקילה"), label="טפסי שקילה")

VOL = {"לקוחות": len(accounts), "תהליכי מכירה": len(opps), "תהליכי ליווי": len(mentor),
       "תשלומים": len(pays), "תיעודי תשלום": len(paydocs), "מחזורי בוסט": len(cohorts),
       "קבוצות וואטסאפ": len(groups), "הרשמות לאירוע": len(evregs), "אנשי קשר": len(contacts),
       "משימות": len(tasks), "פגישות": len(acts)}
print("... נפחים: %s" % VOL, file=sys.stderr)

def gid(r, key):
    v = r.get(key)
    return str(v).lower() if not blank(v) else ""

acc_by_id = {gid(a, "accountid"): a for a in accounts}
def aname(aid):
    a = acc_by_id.get(str(aid).lower() if aid else "")
    return (a or {}).get("accountname") or "(ללא שם)"

recent = lambda r, h=26: (dt(r.get("createdon")) or NOW - timedelta(days=999)) > NOW - timedelta(hours=h)

MIG_SIG = re.compile(r"(\|\s*סדנה בוסט|^עסקה\s*-\s)")
def is_legacy(r):
    if not blank(r.get("pcfLegacyCreatedOn")): return True
    c = dt(r.get("createdon"))
    if c and c <= MIGRATION_END: return True
    if MIG_SIG.search(str(r.get("name") or "")): return True
    return False
def organic(rows): return [r for r in rows if not is_legacy(r)]

# ================================================================ A · שלמות נתונים
# A1 לקוחות ללא שם שמיש
_all = [a for a in accounts if looks_unnamed(a.get("accountname"))]
x = organic(_all)
addlog("לקוחות מההגירה ללא שם שמיש", len(_all) - len(x), "חוב נתונים היסטורי, לא תקלה חיה")
add("A1", "critical" if any(recent(a) for a in x) else "high", "לקוחות חיות ללא שם שמיש (ריק / טלפון כשם / 'ליד חדש')", len(x),
    [{"שם": a.get("accountname"), "טלפון": a.get("telephone1"), "נוצר": a.get("createdon"), "link": fb_link(1, a.get("accountid"))} for a in x[:15]],
    "לקוחה בלי שם = אין למי לפנות, וכל הודעה אישית תצא פגומה.", "מייק", backlog=len(_all) - len(x))

# A2 אין שום דרך ליצור קשר
x = [a for a in accounts if blank(a.get("telephone1")) and blank(a.get("telephone2")) and blank(a.get("emailaddress1"))]
add("A2", "critical", "לקוחות בלי טלפון ובלי מייל — אין דרך ליצור קשר", len(x),
    [{"שם": a.get("accountname"), "נוצר": a.get("createdon"), "link": fb_link(1, a.get("accountid"))} for a in x[:15]], owner="מייק")

# A3 טלפון לא תקין
_all = [a for a in accounts if not blank(a.get("telephone1")) and not valid_phone(a.get("telephone1"))]
x = organic(_all); addlog("לקוחות מההגירה עם טלפון לא תקין", len(_all) - len(x))
add("A3", "high", "לקוחות חיות עם טלפון לא תקין", len(x),
    [{"שם": a.get("accountname"), "טלפון": a.get("telephone1"), "link": fb_link(1, a.get("accountid"))} for a in x[:15]],
    "טלפון פגום שובר גם קלאודצ'אט וגם וואטסאפ.", "מייק", backlog=len(_all) - len(x))

# A4 מייל לא תקין
_all = [a for a in accounts if not blank(a.get("emailaddress1")) and not valid_email(a.get("emailaddress1"))]
x = organic(_all); addlog("לקוחות מההגירה עם מייל לא תקין", len(_all) - len(x))
add("A4", "medium", "לקוחות חיות עם כתובת מייל לא תקינה", len(x),
    [{"שם": a.get("accountname"), "מייל": a.get("emailaddress1"), "link": fb_link(1, a.get("accountid"))} for a in x[:15]], owner="מייק")

# A5 חור ה-pcfCloudChatId (מתועד 12/09)
x = [a for a in accounts if blank(a.get("pcfCloudChatId")) and (dt(a.get("createdon")) or NOW) > MIGRATION_END]
add("A5", "critical", "לקוחות חדשות (אחרי סוף ההגירה) ללא מזהה קלאודצ'אט", len(x),
    [{"שם": a.get("accountname"), "טלפון": a.get("telephone1"), "נוצר": a.get("createdon"), "link": fb_link(1, a.get("accountid"))} for a in x[:20]],
    "החור מ-10/09: כתיבת pcfCloudChatId בזמן אמת מ-Main Leads CRM מעולם לא יושמה. כל אחת כאן חשודה גם כמי שלא קיבלה הודעת ליד חדש.", "מייק · Make")

# A6 לידים בלי מקור הגעה
_all = [a for a in accounts if blank(a.get("pcfUTMSsource")) and recent(a, 24 * 7)]
x = organic(_all); addlog("לקוחות מההגירה ללא מקור הגעה", len(_all) - len(x))
add("A6", "low", "לקוחות חיות מהשבוע ללא מקור הגעה (UTM)", len(x),
    [{"שם": a.get("accountname"), "נוצר": a.get("createdon"), "link": fb_link(1, a.get("accountid"))} for a in x[:10]],
    "בלי אטריביושן אין דשבורד שיווקי אמיתי.", "עודד")

# A7 לקוחות בלי מדריכה
x = [a for a in accounts if blank(a.get("ownerid")) and recent(a, 24 * 7)]
add("A7", "medium", "לקוחות מהשבוע האחרון ללא בעלים/מדריכה", len(x),
    [{"שם": a.get("accountname"), "link": fb_link(1, a.get("accountid"))} for a in x[:10]], owner="מייק")

# A8 תהליך מכירה מיותם
x = [o for o in opps if blank(o.get("accountid"))]
add("A8", "critical", "תהליכי מכירה ללא שיוך לקוחה (רשומות מיותמות)", len(x),
    [{"עסקה": o.get("name"), "נוצר": o.get("createdon"), "link": fb_link(4, o.get("opportunityid"))} for o in x[:15]], owner="מייק")

# A9 תהליך מכירה בלי טלפון וגם הלקוחה בלי טלפון
x = [o for o in opps if blank(o.get("pcfTelephone1")) and blank((acc_by_id.get(gid(o,"accountid")) or {}).get("telephone1"))]
x = drop_excluded("A9", x, "opportunityid")
add("A9", "high", "תהליכי מכירה בלי טלפון — גם לא ברשומת הלקוחה", len(x),
    [{"עסקה": o.get("name"), "link": fb_link(4, o.get("opportunityid"))} for o in x[:10]], owner="מייק")

# A10 ליווי חסר שיוכים
mentor_live = organic(mentor)
for f, lbl, sev in [("pcfaccountid", "לקוחה", "critical"), ("pcfBoostLinked", "מחזור בוסט", "high"),
                    ("pcfActualGroup", "קבוצת WhatsApp", "high"), ("pcfSale", "תהליך מכירה", "medium"),
                    ("pcfStartDate", "תאריך תחילת ליווי", "medium")]:
    _all = [m for m in mentor if blank(m.get(f))]
    x = [m for m in mentor_live if blank(m.get(f))]
    x = drop_excluded("A10-" + f, x, "customobject1051id")
    addlog("תהליכי ליווי מההגירה ללא %s" % lbl, len(_all) - len(x))
    add("A10-" + f, sev, "תהליכי ליווי חיים ללא %s" % lbl, len(x),
        [{"ליווי": m.get("name"), "נוצר": m.get("createdon"), "link": fb_link(1051, m.get("customobject1051id"))} for m in x[:12]],
        "הבאג של 27 הלקוחות התקועות (12/09) חזר אם המספר עולה." if f in ("pcfBoostLinked", "pcfActualGroup") else "", "מייק",
        backlog=len(_all) - len(x))

# A11 תשלום בלי סכום / בלי לקוחה / סכום לא חיובי
_all = [p for p in pays if blank(p.get("pcfAccountid"))]
x = organic([p for p in _all if "רטרו" not in str(p.get("name") or "")])
addlog("תשלומי רטרו/הגירה ללא שיוך לקוחה", len(_all) - len(x), "רשומות '[רטרו — לאיחוד במעבר]' — חוב ידוע")
add("A11a", "critical", "תשלומים חיים ללא שיוך לקוחה", len(x),
    [{"תשלום": p.get("name"), "נוצר": p.get("createdon"), "link": fb_link(1039, p.get("customobject1039id"))} for p in x[:12]],
    owner="מייק", backlog=len(_all) - len(x))
def num(v):
    try: return float(str(v).replace(",", ""))
    except Exception: return None
_all = [p for p in pays if (num(p.get("pcfNeedToPayIncludingVat")) or 0) <= 0]
x = organic(_all); addlog("תשלומים מההגירה בסכום 0 או שלילי", len(_all) - len(x))
add("A11b", "high", "תשלומים חיים בסכום 0 או שלילי", len(x),
    [{"תשלום": p.get("name"), "סכום": p.get("pcfNeedToPayIncludingVat"), "link": fb_link(1039, p.get("customobject1039id"))} for p in x[:12]],
    owner="מייק", backlog=len(_all) - len(x))

# A12 מחזור בוסט בלי תאריך / בלי לינק קבוצה
x = [c for c in cohorts if blank(c.get("pcfStartDate"))]
add("A12a", "high", "מחזורי בוסט ללא תאריך תחילה", len(x),
    [{"מחזור": c.get("name"), "link": fb_link(1007, c.get("customobject1007id"))} for c in x[:12]], owner="מייק")
_all = [c for c in cohorts if blank(c.get("pcfEventLink")) and blank(c.get("pcfwhatspgrouprelated"))]
x = [c for c in _all if (dt(c.get("pcfStartDate")) or NOW + timedelta(days=999)) < NOW + timedelta(days=21)]
x = drop_excluded("A12b", x, "customobject1007id")
addlog("מחזורי בוסט עתידיים (מעל 3 שבועות) בלי קבוצה", len(_all) - len(x), "לא דחוף — יוקם לקראת המחזור")
add("A12b", "high", "מחזורי בוסט שמתחילים בתוך 3 שבועות בלי קבוצת וואטסאפ", len(x),
    [{"מחזור": c.get("name"), "link": fb_link(1007, c.get("customobject1007id"))} for c in x[:12]],
    "חוסם את שיוך הלקוחות לקבוצה בהמשך המסע.", "מייק", backlog=len(_all) - len(x))

# A13 קבוצת וואטסאפ בלי מזהה GreenAPI / בלי לינק
x = [g for g in groups if blank(g.get("pcfGreenApiId"))]
add("A13", "medium", "קבוצות וואטסאפ ללא מזהה GreenAPI", len(x),
    [{"קבוצה": g.get("name"), "link": fb_link(1068, g.get("customobject1068id"))} for g in x[:12]],
    "בלי מזהה אין הוספה אוטומטית לקבוצה.", "מייק")

# A14 שדות חובה לפי המטא-דאטה שריקים בפועל (סריקה גנרית)
REQ_SCAN = [(1, accounts, "accountid", "לקוח"), (4, opps, "opportunityid", "תהליך מכירה"),
            (1051, mentor, "customobject1051id", "תהליך ליווי"), (1039, pays, "customobject1039id", "תשלום"),
            (1007, cohorts, "customobject1007id", "מחזור בוסט")]
req_hits = []
for ot, rows, pk, lbl in REQ_SCAN:
    for c in fb_meta_required(ot):
        fn = c.get("fieldname")
        if fn in (pk, "accountname", "name"): continue
        miss = [r for r in rows if fn in r and blank(r.get(fn))]
        if miss:
            req_hits.append({"אובייקט": lbl, "שדה": "%s (%s)" % (c.get("name"), fn), "רשומות ריקות": len(miss)})
add("A14", "medium", "שדות המסומנים 'חובה' במטא-דאטה ובפועל ריקים", len(req_hits), req_hits[:20],
    "פיירברי לא אוכף חובה על כתיבת API — לכן זה נשמר שקט.", "מייק")

# ================================================================ B · כפילויות
def dupes(rows, keyfn, pk, ot, min_n=2):
    g = defaultdict(list)
    for r in rows:
        k = keyfn(r)
        if k: g[k].append(r)
    return {k: v for k, v in g.items() if len(v) >= min_n}

d = dupes(accounts, lambda a: norm_phone(a.get("telephone1")) or None, "accountid", 1)
add("B1", "critical" if d else "ok", "לקוחות כפולות לפי טלפון", sum(len(v) - 1 for v in d.values()),
    [{"טלפון": k, "כמה": len(v), "שמות": " | ".join(str(r.get("accountname"))[:25] for r in v[:4]),
      "link": fb_link(1, v[0].get("accountid"))} for k, v in list(d.items())[:15]],
    "כפילות טלפון = הודעות כפולות ללקוחה ופיצול היסטוריה.", "מייק")

d = dupes(accounts, lambda a: (str(a.get("emailaddress1")).strip().lower() if valid_email(a.get("emailaddress1")) else None), "accountid", 1)
add("B2", "high", "לקוחות כפולות לפי מייל", sum(len(v) - 1 for v in d.values()),
    [{"מייל": k, "כמה": len(v), "שמות": " | ".join(str(r.get("accountname"))[:25] for r in v[:4]),
      "link": fb_link(1, v[0].get("accountid"))} for k, v in list(d.items())[:12]], owner="מייק")

d = dupes(accounts, lambda a: (None if looks_unnamed(a.get("accountname")) else re.sub(r"\s+", " ", str(a.get("accountname")).strip().lower())), "accountid", 1)
d = {k: v for k, v in d.items() if len({norm_phone(r.get("telephone1")) for r in v}) > 1}
_tot = len(d); d = {k: v for k, v in d.items() if any(not is_legacy(r) for r in v)}
addlog("קבוצות שם זהה שכולן מההגירה", _tot - len(d))
add("B3", "medium", "לקוחות עם שם זהה וטלפונים שונים (חשד לכפילות או לשם גנרי)", len(d),
    [{"שם": k, "כמה": len(v), "link": fb_link(1, v[0].get("accountid"))} for k, v in list(d.items())[:12]], owner="מייק")

# B4 תהליכי מכירה כפולים לאותה לקוחה + אותו מוצר (באג 319)
d = dupes(opps, lambda o: (gid(o, "accountid") + "|" + str(o.get("pcfProduct") or "")) if not blank(o.get("accountid")) else None, "opportunityid", 4)
_tot = sum(len(v) - 1 for v in d.values())
d = {k: v for k, v in d.items() if any(not is_legacy(r) for r in v)}
_live = sum(len(v) - 1 for v in d.values())
addlog("זוגות תהליכי מכירה כפולים שכולם מההגירה", _tot - _live, "ניקוי היסטורי, ממתין לאישור פרוטוקול המיזוג")
add("B4", "critical" if d else "ok", "תהליכי מכירה כפולים שנוגעים ברשומה חיה — אותה לקוחה, אותו מוצר", _live,
    [{"לקוחה": aname(v[0].get("accountid")), "כמה": len(v),
      "שמות עסקאות": " | ".join(str(r.get("name"))[:32] for r in v[:3]),
      "link": fb_link(1, v[0].get("accountid"))} for k, v in list(d.items())[:15]],
    "זו החתימה של 319 החשבונות (12/09). מוצגים רק זוגות שנוגעים ברשומה חיה. מספר שעולה = הדליפה חזרה.", "מייק", backlog=_tot - _live)

# B5 תהליכי ליווי כפולים
d = dupes(mentor, lambda m: (gid(m, "pcfaccountid") + "|" + str(m.get("pcfProduct") or "")) if not blank(m.get("pcfaccountid")) else None, "customobject1051id", 1051)
_tot = sum(len(v) - 1 for v in d.values())
d = {k: v for k, v in d.items() if any(not is_legacy(r) for r in v)}
_b5ex = {e.lower() for e in excluded_ids("B5")}
d = {k: v for k, v in d.items()
     if not any(str(r.get("customobject1051id") or "").lower() in _b5ex for r in v)}
_live = sum(len(v) - 1 for v in d.values())
addlog("תהליכי ליווי כפולים שכולם מההגירה", _tot - _live)
add("B5", "high", "תהליכי ליווי כפולים הנוגעים לרשומה חיה — אותה לקוחה, אותו מוצר", _live,
    [{"לקוחה": aname(v[0].get("pcfaccountid")), "כמה": len(v),
      "link": fb_link(1051, v[0].get("customobject1051id"))} for k, v in list(d.items())[:12]], owner="מייק")

# B6 תשלומים כפולים — אותה לקוחה, אותו סכום, פחות מ-15 דק'
g = defaultdict(list)
for p in pays:
    if blank(p.get("pcfAccountid")): continue
    g[(gid(p, "pcfAccountid"), str(p.get("pcfNeedToPayIncludingVat")))].append(p)
b6 = []
for k, v in g.items():
    if len(v) < 2: continue
    v2 = sorted(v, key=lambda r: dt(r.get("createdon")) or NOW)
    for i in range(1, len(v2)):
        t0, t1 = dt(v2[i-1].get("createdon")), dt(v2[i].get("createdon"))
        if t0 and t1 and (t1 - t0) < timedelta(minutes=15):
            b6.append({"לקוחה": aname(k[0]), "סכום": k[1], "הפרש_דק": round((t1 - t0).total_seconds() / 60, 1),
                       "link": fb_link(1039, v2[i].get("customobject1039id")),
                       "_live": not (is_legacy(v2[i]) and is_legacy(v2[i - 1]))})
_tot6 = len(b6); b6 = [r for r in b6 if r.pop("_live", True)]
addlog("זוגות תשלומים כפולים שכולם מההגירה", _tot6 - len(b6))
add("B6", "critical" if b6 else "ok", "תשלומים כפולים חיים — אותה לקוחה ואותו סכום בפער של פחות מ-15 דקות", len(b6), b6[:12],
    "חשד לחיוב כפול. בודקים מול הסליקה לפני כל מסקנה.", "מייק · עודד")

# B7 דליפת הגירה חוזרת
CLEAN_PREFIX = re.compile(r"^\s*\[(כפילות מוגרת|רטרו|להשלמה)")
x = [o for o in opps if MIG_SIG.search(str(o.get("name") or ""))
     and not CLEAN_PREFIX.match(str(o.get("name") or ""))
     and (dt(o.get("createdon")) or datetime(2000, 1, 1, tzinfo=IL)) > NOW - timedelta(hours=13)]
add("B7", "critical" if x else "ok", "רשומות בחתימת הגירה שנוצרו ב-13 השעות האחרונות — דליפה חוזרת", len(x),
    [{"עסקה": o.get("name"), "נוצר": o.get("createdon"), "link": fb_link(4, o.get("opportunityid"))} for o in x[:15]],
    "רשומות שסומנו '[כפילות מוגרת]' / '[רטרו]' הוחרגו — אלה פעולות הניקוי שלך. אם זה לא אפס, תרחיש Make או מנוע ההגירה התעורר שוב. עוצרים מיד.", "מייק")

# B8 אנשי קשר כפולים
d = dupes(contacts, lambda c: norm_phone(c.get("telephone1") or c.get("mobilephone1")) or None, "contactid", 2)
add("B8", "medium", "אנשי קשר כפולים לפי טלפון", sum(len(v) - 1 for v in d.values()),
    [{"טלפון": k, "כמה": len(v), "link": fb_link(2, v[0].get("contactid"))} for k, v in list(d.items())[:10]], owner="מייק")

# B9 הרשמות כפולות לאותו אירוע
d = dupes(evregs, lambda e: (gid(e, "pcfAccountid") + "|" + str(e.get("pcfEventId") or "")) if not blank(e.get("pcfAccountid")) else None, "customobject1030id", 1030)
add("B9", "medium", "הרשמות כפולות לאותו אירוע/וובינר", sum(len(v) - 1 for v in d.values()),
    [{"לקוחה": aname(v[0].get("pcfAccountid")), "כמה": len(v), "link": fb_link(1030, v[0].get("customobject1030id"))} for k, v in list(d.items())[:10]],
    "כפילות הרשמה = הזמנה ותזכורות כפולות לוובינר.", "מייק")

# B10 תיעודי תשלום כפולים לפי אסמכתא
d = dupes(paydocs, lambda p: (str(p.get("pcfReference")).strip() if not blank(p.get("pcfReference")) else None), "customobject1018id", 1018)
_tot = sum(len(v) - 1 for v in d.values())
d = {k: v for k, v in d.items() if any(not is_legacy(r) for r in v)}
_live = sum(len(v) - 1 for v in d.values())
addlog("תיעודי תשלום כפולים מההגירה", _tot - _live)
add("B10", "high", "תיעודי תשלום כפולים לפי אסמכתא הנוגעים לרשומה חיה", _live,
    [{"אסמכתא": k, "כמה": len(v), "link": fb_link(1018, v[0].get("customobject1018id"))} for k, v in list(d.items())[:10]],
    "לפני מסקנה — לוודא שמספר האסמכתא בגרואו הוא בכלל ייחודי. אם לא, זו לא כפילות אלא שדה שאינו מזהה.", "מייק",
    backlog=_tot - _live)

# ================================================================ C · שרשראות שבורות
opp_by_acc = defaultdict(list)
for o in opps: opp_by_acc[gid(o, "accountid")].append(o)
men_by_acc = defaultdict(list)
for m in mentor: men_by_acc[gid(m, "pcfaccountid")].append(m)
pay_by_acc = defaultdict(list)
for p in pays: pay_by_acc[gid(p, "pcfAccountid")].append(p)
pay_by_sale = defaultdict(list)
for p in pays: pay_by_sale[gid(p, "pcfSale")].append(p)
doc_by_pay = defaultdict(list)
for p in paydocs: doc_by_pay[gid(p, "pcfPaymentCollection")].append(p)
evr_by_acc = defaultdict(list)
for e in evregs: evr_by_acc[gid(e, "pcfAccountid")].append(e)
men_by_sale = defaultdict(list)
for m in mentor: men_by_sale[gid(m, "pcfSale")].append(m)

# C1 לקוחה חדשה בלי תהליך מכירה
x = [a for a in accounts if recent(a, 26) and not opp_by_acc.get(gid(a, "accountid"))]
add("C1", "critical", "לקוחות שנוצרו ב-26 השעות האחרונות ואין להן תהליך מכירה", len(x),
    [{"שם": a.get("accountname"), "טלפון": a.get("telephone1"), "נוצר": a.get("createdon"), "link": fb_link(1, a.get("accountid"))} for a in x[:15]],
    "הליד נכנס אבל לא נפתח לו תהליך — הוא לא יופיע בשום פייפליין ואף אחד לא יטפל בו.", "מייק")

# C2 עסקה סגורה בהצלחה בלי תשלום
CLOSED_WORDS = ("נסגרה בהצלחה", "נסגר בהצלחה", "won", "שולם")
def is_won(o): return any(w in str(o.get("statuscode") or "") for w in CLOSED_WORDS)
_all = [o for o in opps if is_won(o) and not pay_by_sale.get(gid(o, "opportunityid"))]
x = organic(_all)
addlog("עסקאות הגירה שנסגרו בהצלחה ללא רשומת תשלום", len(_all) - len(x),
       "כפילויות הגירה שהתשלום שלהן נותב לעסקה השורדת בעבודת הדדופ — מועמדות למחיקה, לא לחקירה")
add("C2", "critical", "עסקאות חיות שנסגרו בהצלחה וללא רשומת תשלום", len(x),
    [{"עסקה": o.get("name"), "לקוחה": aname(o.get("accountid")), "נסגר": o.get("pcfclosedate"), "link": fb_link(4, o.get("opportunityid"))} for o in x[:15]],
    "או שהכסף לא תועד, או שהסטטוס עודכן ידנית בלי סליקה. שתי האפשרויות מחייבות בדיקה. רשומות הגירה הוצאו לחוב ההגירה.", "מייק",
    backlog=len(_all) - len(x))

# C3 יש תשלום ואין ליווי
x = []
for p in pays:
    acc = gid(p, "pcfAccountid")
    if not acc: continue
    if not men_by_acc.get(acc) and (num(p.get("pcfTotalPaidIncludingVat")) or 0) > 0:
        x.append(p)
_allc3 = x; x = organic(x)
addlog("תשלומים מההגירה ללא תהליך ליווי", len(_allc3) - len(x))
add("C3", "high", "לקוחות ששילמו בפעילות חיה ואין להן תהליך ליווי", len(x),
    [{"לקוחה": aname(p.get("pcfAccountid")), "שולם": p.get("pcfTotalPaidIncludingVat"), "link": fb_link(1039, p.get("customobject1039id"))} for p in x[:15]],
    "לקוחה שילמה ולא נפתח לה ליווי = היא לא מקבלת שירות בפועל.", "מייק")

# C4 ליווי בלי welcome
_all = [m for m in mentor if blank(m.get("pcfWelcomeSent")) and (dt(m.get("createdon")) or NOW) > NOW - timedelta(days=14)]
x = organic(_all)
addlog("תהליכי ליווי מההגירה בלי סימון Welcome", len(_all) - len(x), "לקוחות היסטוריות, לא אמורות לקבל וולקאם")
add("C4", "high", "תהליכי ליווי חיים בלי סימון שליחת Welcome", len(x),
    [{"ליווי": m.get("name"), "נוצר": m.get("createdon"), "link": fb_link(1051, m.get("customobject1051id"))} for m in x[:15]],
    "הבאג של הוולקאם (12/09) — לבדוק אם השדה לא נכתב או שההודעה באמת לא יצאה.", "מייק", backlog=len(_all) - len(x))

# C5 תשלום בלי תיעוד תשלום
x = [p for p in pays if (num(p.get("pcfTotalPaidIncludingVat")) or 0) > 0 and not doc_by_pay.get(gid(p, "customobject1039id"))]
add("C5", "medium", "תשלומים עם כסף שנכנס וללא תיעוד תשלום/חשבונית", len(x),
    [{"תשלום": p.get("name"), "לקוחה": aname(p.get("pcfAccountid")), "שולם": p.get("pcfTotalPaidIncludingVat"),
      "link": fb_link(1039, p.get("customobject1039id"))} for p in x[:12]], owner="מייק · עודד")

# C6 ליווי בלי לקוחה שמקושרת חזרה לקבוצה
_all = [a for a in accounts if men_by_acc.get(gid(a, "accountid")) and blank(a.get("pcfWhatsAppReferans"))]
x = organic(_all)
addlog("לקוחות מההגירה עם ליווי וללא שיוך קבוצה", len(_all) - len(x))
add("C6", "medium", "לקוחות חיות עם ליווי וללא שיוך קבוצת וואטסאפ ברשומת הלקוחה", len(x),
    [{"שם": a.get("accountname"), "link": fb_link(1, a.get("accountid"))} for a in x[:12]], owner="מייק",
    backlog=len(_all) - len(x))

# C7 קנתה בוסט ואין הרשמה לאירוע
boost_opps = [o for o in opps if "בוסט" in str(o.get("name") or "") or not blank(o.get("pcfCourse"))]
_all = [o for o in boost_opps if is_won(o) and not evr_by_acc.get(gid(o, "accountid"))]
x = organic(_all)
addlog("רכישות בוסט מההגירה ללא הרשמה לאירוע", len(_all) - len(x), "הוובינרים שלהן כבר עברו")
add("C7", "high", "רכשו בוסט בפעילות חיה ואין להן הרשמה לאירוע/וובינר", len(x),
    [{"עסקה": o.get("name"), "לקוחה": aname(o.get("accountid")), "link": fb_link(4, o.get("opportunityid"))} for o in x[:12]],
    "בלי הרשמה לאירוע הן לא יקבלו הזמנה ותזכורות לוובינר.", "מייק", backlog=len(_all) - len(x))

# C8 לקוחה עם עסקה ואין איש קשר
con_by_acc = defaultdict(list)
for c in contacts: con_by_acc[gid(c, "accountid")].append(c)
_all = [a for a in accounts if opp_by_acc.get(gid(a, "accountid")) and not con_by_acc.get(gid(a, "accountid")) and recent(a, 24 * 7)]
x = organic(_all)
addlog("לקוחות מההגירה ללא איש קשר", len(_all) - len(x), "אובייקט איש קשר כמעט לא בשימוש בחשבון")
add("C8", "low", "לקוחות חיות עם תהליך מכירה וללא איש קשר", len(x),
    [{"שם": a.get("accountname"), "link": fb_link(1, a.get("accountid"))} for a in x[:10]], owner="מייק")

# ================================================================ D · אנומליות זרימה וסטטוס
# D1 תקועים ב"ליד חדש"
_all = [o for o in opps if "ליד חדש" in str(o.get("statuscode") or "") and (dt(o.get("createdon")) or NOW) < NOW - timedelta(days=7)]
x = organic(_all)
addlog("עסקאות מההגירה שנשארו ב'ליד חדש'", len(_all) - len(x))
add("D1", "medium", "תהליכי מכירה תקועים ב'ליד חדש' מעל 7 ימים", len(x),
    [{"עסקה": o.get("name"), "לקוחה": aname(o.get("accountid")), "נוצר": o.get("createdon"), "link": fb_link(4, o.get("opportunityid"))} for o in x[:10]],
    "בפייפליין בריא זה לא אמור להצטבר. מספר שעולה משבוע לשבוע = אף אחד לא עובד על הפייפליין.", "רויטל")

# D2 כסף נכנס אבל הסטטוס עוד 'ליד חדש'
_all = [o for o in opps if pay_by_sale.get(gid(o, "opportunityid")) and "ליד חדש" in str(o.get("statuscode") or "")]
x = organic(_all); addlog("עסקאות מההגירה עם תשלום שנשארו ב'ליד חדש'", len(_all) - len(x))
add("D2", "high", "עסקאות חיות עם תשלום מקושר שהסטטוס שלהן עדיין 'ליד חדש'", len(x),
    [{"עסקה": o.get("name"), "לקוחה": aname(o.get("accountid")), "link": fb_link(4, o.get("opportunityid"))} for o in x[:12]],
    "או שהאוטומציה שמקדמת סטטוס לא רצה, או שהתשלום שויך לעסקה הלא נכונה.", "מייק", backlog=len(_all) - len(x))

# D3 מחזור בוסט עם תאריך שחלף וסטטוס לא סגור
x = []
for c in cohorts:
    d0 = dt(c.get("pcfEndDate")) or dt(c.get("pcfStartDate"))
    st = str(c.get("pcfStatus") or "")
    if d0 and d0 < NOW - timedelta(days=2) and any(w in st for w in ("פתוח", "עתידי", "בהרשמה", "פעיל")):
        x.append({"מחזור": c.get("name"), "תאריך": c.get("pcfStartDate"), "סטטוס": st, "link": fb_link(1007, c.get("customobject1007id"))})
add("D3", "medium", "מחזורי בוסט שהתאריך שלהם חלף והסטטוס עוד פתוח/עתידי", len(x), x[:12],
    "סטטוסים הפוכים במחזורים תועדו כבר. זה מרעיל כל שיוך אוטומטי לפי 'המחזור הפעיל'.", "מייק")

# D4 תאריך יצירה בעתיד
x = []
for lbl, rows, pk, ot in [("לקוח", accounts, "accountid", 1), ("תהליך מכירה", opps, "opportunityid", 4),
                          ("ליווי", mentor, "customobject1051id", 1051), ("תשלום", pays, "customobject1039id", 1039)]:
    for r in rows:
        d0 = dt(r.get("createdon"))
        if d0 and d0 > NOW + timedelta(hours=2):
            x.append({"אובייקט": lbl, "רשומה": r.get("name") or r.get("accountname"), "נוצר": r.get("createdon"), "link": fb_link(ot, r.get(pk))})
add("D4", "medium", "רשומות עם תאריך יצירה בעתיד", len(x), x[:10],
    "בדרך כלל סימן לאזור זמן שגוי באוטומציה שכותבת.", "מייק")

# D5 משימות שעבר להן התאריך
OPEN_TASK = ("פתוח", "חדש", "בטיפול", "ממתין")
x = [t for t in tasks if (dt(t.get("scheduledend")) or dt(t.get("pcfexecutiondate")) or NOW + timedelta(days=999)) < NOW - timedelta(days=1)
     and any(w in str(t.get("statuscode") or "") for w in OPEN_TASK)]
_all = x; x = organic(_all)
addlog("משימות בקרה מההגירה שעבר תאריך היעד", len(_all) - len(x), "נוצרו אוטומטית בחלון ההגירה")
add("D5", "medium", "משימות חיות פתוחות שתאריך היעד שלהן חלף", len(x),
    [{"משימה": t.get("subject"), "יעד": t.get("scheduledend") or t.get("pcfexecutiondate"), "link": fb_link(10, t.get("taskid"))} for t in x[:12]],
    owner="רויטל", backlog=len(_all) - len(x))

# D6 פגישות בעבר שנשארו מתוכננות
x = [a for a in acts if (dt(a.get("scheduledstart")) or NOW + timedelta(days=999)) < NOW - timedelta(days=1)
     and any(w in str(a.get("statuscode") or "") for w in ("מתוכננ", "נקבע", "פתוח"))]
add("D6", "low", "פגישות בעבר שנשארו בסטטוס 'מתוכננת'", len(x),
    [{"פגישה": a.get("subject"), "מתי": a.get("scheduledstart"), "link": fb_link(6, a.get("activityid"))} for a in x[:10]], owner="רויטל")

# D7 עסקאות ללא נציג
x = [o for o in opps if blank(o.get("ownerid")) and recent(o, 24 * 7)]
add("D7", "medium", "תהליכי מכירה מהשבוע ללא נציג/בעלים", len(x),
    [{"עסקה": o.get("name"), "link": fb_link(4, o.get("opportunityid"))} for o in x[:10]], owner="מייק")

# D8 יתרת תשלום שלילית / שולם יותר מהנדרש
x = []
for p in pays:
    need, paid = num(p.get("pcfNeedToPayIncludingVat")), num(p.get("pcfTotalPaidIncludingVat"))
    if need is not None and paid is not None and paid > need + 1:
        x.append({"תשלום": p.get("name"), "לקוחה": aname(p.get("pcfAccountid")), "נדרש": need, "שולם": paid,
                  "link": fb_link(1039, p.get("customobject1039id"))})
add("D8", "high", "תשלומים שבהם שולם יותר מהסכום הנדרש", len(x), x[:12],
    "חיוב עודף — לבדוק מול הסליקה.", "מייק · עודד")

# D9 מאחרים בתשלום
x = [p for p in pays if str(p.get("pcfDelayOnPayment") or "").strip() not in ("", "None", "לא", "0", "False")]
add("D9", "medium", "תשלומים המסומנים כמאחרים בתשלום", len(x),
    [{"לקוחה": aname(p.get("pcfAccountid")), "יתרה": p.get("pcfLeftToPayIncludingVat"), "link": fb_link(1039, p.get("customobject1039id"))} for p in x[:12]], owner="רויטל")

# D10 קבוצות מעל קיבולת
x = []
for g_ in groups:
    cur, cap = num(g_.get("pcfCurrentCount")), num(g_.get("pcfCapacity"))
    if cur is not None and cap and cur > cap:
        x.append({"קבוצה": g_.get("name"), "בקבוצה": cur, "קיבולת": cap, "link": fb_link(1068, g_.get("customobject1068id"))})
add("D10", "medium", "קבוצות וואטסאפ מעל הקיבולת המוגדרת", len(x), x[:10], owner="מייק")

# D11 ליווי שהמשקלים לא מתעדכנים
x = [m for m in mentor if not blank(m.get("pcfStartDate")) and (dt(m.get("pcfStartDate")) or NOW) < NOW - timedelta(days=10)
     and ((dt(m.get("pcfLastWeighDate")) or datetime(2000,1,1,tzinfo=IL)) < NOW - timedelta(days=14))
     and "פעיל" in str(m.get("pcfStatus") or "")]
add("D11", "medium", "ליווי פעיל ללא שקילה מעל 14 יום", len(x),
    [{"ליווי": m.get("name"), "שקילה אחרונה": m.get("pcfLastWeighDate"), "link": fb_link(1051, m.get("customobject1051id"))} for m in x[:12]],
    "או שהלקוחה נשרה או שטופס השקילה לא נכתב חזרה.", "רויטל")

# D12 עדכון מאסיבי — חשד לריצה סורגת
for lbl, rows, ot in [("לקוחות", accounts, 1), ("תהליכי מכירה", opps, 4), ("ליווי", mentor, 1051)]:
    c = Counter()
    for r in rows:
        d0 = dt(r.get("modifiedon"))
        if d0 and d0 > NOW - timedelta(hours=12):
            c[d0.strftime("%Y-%m-%d %H:%M")] += 1
    # דקות צמודות הן ריצה אחת, לא N תקלות. מקבצים לאירועים ומדווחים אירועים.
    hot = sorted([(dt(k), v) for k, v in c.items() if v >= 25 and dt(k)])
    events, planned = [], 0
    for d0, v in hot:
        if events and (d0 - events[-1]["_end"]) <= timedelta(minutes=3):
            e = events[-1]; e["_end"] = d0; e["דקות"] += 1; e["סך רשומות"] += v; e["שיא לדקה"] = max(e["שיא לדקה"], v)
        else:
            events.append({"_start": d0, "_end": d0, "דקות": 1, "סך רשומות": v, "שיא לדקה": v})
    rows = []
    for e in events:
        why = in_maintenance(e["_start"]) or in_maintenance(e["_end"])
        if why:
            planned += e["סך רשומות"]; continue
        rows.append({"מתי": "%s–%s" % (e.pop("_start").strftime("%d/%m %H:%M"), e.pop("_end").strftime("%H:%M")),
                     "דקות": e["דקות"], "שיא לדקה": e["שיא לדקה"], "סך רשומות": e["סך רשומות"]})
    if planned:
        addlog("עדכונים ב-%s בתוך חלון ריצה מוצהר" % lbl, planned, "ריצה מאסיבית מתוכננת — לא לופ")
    if rows:
        add("D12-%s" % ot, "high", "אירועי עדכון מאסיבי ב-%s (חשד לריצה סורגת/לופ)" % lbl, len(rows), rows[:5],
            "25+ רשומות בדקה זה כמעט תמיד סקריפט או לופ, לא אנשים. דקות צמודות נספרות כאירוע אחד. "
            "ריצה מתוכננת שמוצהרת ב-maintenance_windows יוצאת מהספירה.", "מייק")

# ================================================================ E · n8n
n8n_ok = False
if N8N_KEY:
    H = {"X-N8N-API-KEY": N8N_KEY, "Accept": "application/json"}
    try:
        wfs, cur = [], None
        while True:
            u = N8N_BASE + "/api/v1/workflows?limit=250&excludePinnedData=true" + ("&cursor=" + cur if cur else "")
            d = _http(u, H)
            wfs += d.get("data") or []
            cur = d.get("nextCursor")
            if not cur: break
        wf_name = {w["id"]: w.get("name") for w in wfs}
        ROITAL_RE = re.compile(r"(רויטל|revital|^WF-?\d+)", re.I)
        ROITAL_IDS = {w["id"] for w in wfs if ROITAL_RE.search(str(w.get("name") or ""))}
        def mine(e): return e.get("workflowId") in ROITAL_IDS
        n8n_ok = True
        # E1 כשלונות בחלון
        WIN = NOW - timedelta(hours=13)
        fails, cur = [], None
        while True:
            u = N8N_BASE + "/api/v1/executions?status=error&limit=250&includeData=false" + ("&cursor=" + cur if cur else "")
            d = _http(u, H)
            batch = d.get("data") or []
            stop = False
            for e in batch:
                t = dt(e.get("startedAt"))
                if t and t < WIN: stop = True; continue
                fails.append(e)
            cur = d.get("nextCursor")
            if stop or not cur: break
        other = [e for e in fails if not mine(e)]
        fails = [e for e in fails if mine(e)]
        if other:
            ERRORS.append("n8n: %d כשלונות נוספים בתהליכים של לקוחות אחרים על אותו שרת — לא נכללו בדוח" % len(other))
        # קיבוץ לפי אירוע שורש: כשלונות באותה דקה הם כמעט תמיד תקלה אחת (למשל הצפת 429 של פיירברי),
        # ולא N תקלות נפרדות. סופרים אירועים, לא הרצות — אחרת מספר הקריטיים מנופח פי שלושה.
        ev = defaultdict(list)
        for e in fails:
            t = dt(e.get("startedAt"))
            ev[t.strftime("%d/%m %H:%M") if t else "לא ידוע"].append(e)
        ev_rows = []
        for k in sorted(ev.keys(), reverse=True):
            wfs_in = sorted({wf_name.get(e.get("workflowId"), e.get("workflowId")) for e in ev[k]})
            ev_rows.append({"מתי": k, "הרצות שנפלו": len(ev[k]), "תהליכים": " · ".join(str(w)[:34] for w in wfs_in[:4])})
        add("E1", "critical" if ev else "ok", "אירועי כשל ב-n8n ב-13 השעות האחרונות", len(ev), ev_rows[:15],
            "כל כשל כאן הוא הודעה, תשלום או רשומה שלא נוצרו. כשלונות באותה דקה נספרים כאירוע אחד — %d הרצות ב-%d אירועים."
            % (len(fails), len(ev)), "מייק")
        # E2 תקועים
        stuck = []
        for st in ("waiting",):
            try: d = _http(N8N_BASE + "/api/v1/executions?status=%s&limit=100" % st, H)
            except Exception: continue
            for e in d.get("data") or []:
                t = dt(e.get("startedAt")); w = dt(e.get("waitTill"))
                if t and t < NOW - timedelta(hours=36) and not w and e.get("workflowId") in ROITAL_IDS:
                    stuck.append({"workflow": wf_name.get(e.get("workflowId"), e.get("workflowId")), "התחיל": e.get("startedAt"), "id": e.get("id")})
        add("E2", "high", "הרצות n8n שממתינות מעל 36 שעות בלי מועד המשך", len(stuck), stuck[:10], owner="מייק")
        # E3 workflows כבויים
        off = [{"workflow": w.get("name"), "עודכן": w.get("updatedAt")} for w in wfs
               if not w.get("active") and not w.get("isArchived") and re.match(r"^WF-?\d+", str(w.get("name") or ""))]
        add("E3", "high", "תהליכי WF ב-n8n שאינם פעילים (active=false)", len(off), off[:20],
            "כל WF כבוי הוא שלב במסע הלקוחה שלא קורה.", "מייק")
        # E4 DRY_RUN
        # ⚠️ תוקן 16/09/2026: הרגקס הקודם תפס הערות, notes והשוואות (`cfg.DRY_RUN === true`)
        # והפיק 10 ממצאי שווא מתוך 10. עכשיו נבדקת *השמה* בפועל בגוף הקונפיג בלבד,
        # אחרי ניקוי הערות ושדות notes/description.
        # רק צורת ההשמה האמיתית בקונפיג: DRY_RUN: true
        # צורת `DRY_RUN=true` בקוד הזה מופיעה אך ורק בפרוזה (הערות ומחרוזות הסבר) ולכן אינה נספרת.
        ASSIGN_TRUE = re.compile(r"(?<!\\\")[\"']?\bDRY_RUN[\"']?\s*:\s*true\b", re.I)
        def _strip_noise(nodes):
            clean = []
            for n in nodes:
                n = {k: v for k, v in n.items() if k not in ("notes", "notesInFlow", "description")}
                s = json.dumps(n, ensure_ascii=False)
                s = s.replace("\\n", "\n").replace("\\t", " ")   # פורסים שורות אמיתיות קודם
                s = re.sub(r"//.*?$", " ", s, flags=re.M)        # הערות שורה בקוד
                s = re.sub(r"/\*.*?\*/", " ", s, flags=re.S)     # הערות בלוק
                s = re.sub(r"DRY_RUN\s*===", "DRY_RUN ==EQ==", s)  # השוואה, לא השמה
                s = re.sub(r"if\s*\([^)]*\)\s*cfg\.DRY_RUN\s*=\s*true", " ", s)  # השמה מותנית לבדיקות
                clean.append(s)
            return "\n".join(clean)
        dry = []
        for w in wfs:
            if not w.get("active") or w["id"] not in ROITAL_IDS: continue
            try:
                full = _http(N8N_BASE + "/api/v1/workflows/" + w["id"], H)
            except Exception: continue
            nodes = full.get("nodes") or []
            if ASSIGN_TRUE.search(_strip_noise(nodes)):
                dry.append({"workflow": w.get("name"), "סיבה": "DRY_RUN מושם ל-true בקונפיג"})
            dis = [n.get("name") for n in (full.get("nodes") or []) if n.get("disabled")]
            _ok_disabled = (EXC.get("intentional_disabled_nodes") or {})
            if dis and re.match(r"^WF-?\d+", str(w.get("name") or "")) \
               and str(w.get("name")) not in _ok_disabled:
                dry.append({"workflow": w.get("name"), "צמתים מנוטרלים": ", ".join(dis[:6])})
        add("E4", "high", "תהליכים פעילים שעדיין ב-DRY_RUN או עם צמתים מנוטרלים", len(dry), dry[:20],
            "פעיל אבל מנוטרל = נראה ירוק בלוח ולא עושה כלום.", "מייק")
        # E5 לופ
        allex, cur = [], None
        d = _http(N8N_BASE + "/api/v1/executions?limit=250&includeData=false", H)
        for e in d.get("data") or []:
            t = dt(e.get("startedAt"))
            if t and t > NOW - timedelta(hours=13) and mine(e): allex.append(e)
        per = Counter(wf_name.get(e.get("workflowId"), e.get("workflowId")) for e in allex)
        loops = [{"workflow": k, "הרצות ב-13 שעות": v} for k, v in per.most_common(5) if v >= 120]
        add("E5", "high", "תהליכי n8n עם מספר הרצות חריג (חשד לופ)", len(loops), loops, owner="מייק")
    except Exception as e:
        ERRORS.append("n8n: %s" % e)
else:
    ERRORS.append("n8n: לא הוגדר מפתח API — בדיקות E לא רצו")

# ================================================================ F · Make
if MAKE_KEY:
    try:
        # ⚠️ גוצ'ה מתועדת: Make/Cloudflare מחזיר 403 code 1010 בלי User-Agent של דפדפן.
        H = {"Authorization": "Token " + MAKE_KEY, "Accept": "application/json",
             "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                           "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"}
        base = "https://%s/api/v2" % MAKE_ZONE
        teams = _http(base + "/teams" + ("?organizationId=%s" % MAKE_TEAM if MAKE_TEAM else ""), H)
        tids = [t["id"] for t in (teams.get("teams") or [])] or ([MAKE_TEAM] if MAKE_TEAM else [])
        rows = []
        for tid in tids:
            scen = _http(base + "/scenarios?teamId=%s&pg[limit]=200" % tid, H).get("scenarios") or []
            for s in scen:
                if not s.get("isActive"): continue
                try:
                    logs = _http(base + "/scenarios/%s/logs?pg[limit]=25" % s["id"], H).get("scenarioLogs") or []
                except Exception: continue
                bad = [l for l in logs if str(l.get("status")) in ("2", "3", "error", "warning")
                       and (dt(l.get("timestamp")) or NOW) > NOW - timedelta(hours=13)]
                if bad:
                    rows.append({"תרחיש": s.get("name"), "כשלונות ב-13 שעות": len(bad), "אחרון": bad[0].get("timestamp")})
        add("F1", "critical" if rows else "ok", "תרחישי Make שנכשלו ב-13 השעות האחרונות", len(rows), rows[:20],
            "קריאה בלבד — אפס נגיעה בתרחישים.", "מייק")
    except Exception as e:
        ERRORS.append("Make: %s" % e)
else:
    ERRORS.append("Make: לא הוגדר מפתח API — בדיקות F לא רצו. זו נקודת העיוורון הגדולה בבדיקה.")

# ================================================================ G · CloudChat
if CC_KEY:
    try:
        H = {"Authorization": "Bearer " + CC_KEY, "Accept": "application/json",
             "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/127 Safari/537.36"}
        newacc = [a for a in organic(accounts) if recent(a, 26) and valid_phone(a.get("telephone1"))]
        missing, checked = [], 0
        for a in newacc[:120]:
            ph = norm_phone(a.get("telephone1"))
            uid = "972" + ph[1:]
            checked += 1
            try:
                d = _http(CC_BASE + "/subscriber/get-info-by-user-id?user_id=" + uid, H, timeout=30)
                if d and d.get("data"): continue
            except Exception as ex:
                if "400" not in str(ex):        # 400 = subscriber not found; כל שאר השגיאות אינן מסקנה
                    ERRORS.append("קלאודצ'אט: בדיקת %s נכשלה (%s)" % (ph, str(ex)[:60])); continue
            missing.append({"שם": a.get("accountname"), "טלפון": ph, "נוצר": a.get("createdon"),
                            "link": fb_link(1, a.get("accountid"))})
        add("G1", "critical" if missing else "ok", "לקוחות חדשות (26 שעות) שאינן קיימות כלל בקלאודצ'אט", len(missing), missing[:20],
            "מתוך %d לקוחות חיות שנבדקו. אלה לא קיבלו הודעת ליד חדש — תקלת שירות ללקוחה, לא תקלת נתונים." % checked,
            "מייק · Make")
    except Exception as e:
        ERRORS.append("CloudChat: %s" % e)
else:
    ERRORS.append("CloudChat: לא הוגדר מפתח — בדיקת G לא רצה")

# ================================================================ H · דלתא מול ההרצה הקודמת
prev = {}
pp = os.path.join(OUT, "state_prev.json")
if os.path.exists(pp):
    try: prev = json.load(open(pp)).get("counts") or {}
    except Exception: pass
counts = {f["code"]: f["count"] for f in FINDINGS}
delta = {}
for k, v in counts.items():
    p = prev.get(k)
    if p is None: delta[k] = None
    else: delta[k] = v - p
for f in FINDINGS:
    f["delta"] = delta.get(f["code"])

# ---- סיווג לדליים: פעיל / ידוע ומטופל / תפעולי ----
# ממצא "ידוע" הוא ממצא אמיתי שכבר הוכרע וממתין לתיקון שורש. הוא לא נספר כפעיל,
# אבל הוא לא מושתק: אם הוא עולה מעל הרמה המאושרת הוא חוזר להיות פעיל בחומרה המקורית.
for f in FINDINGS:
    code, cnt = f["code"], f["count"]
    f["bucket"], f["why"], f["doc"], f["escalated"] = "active", "", "", ""
    base = BASELINE.get(code)
    if code in OPER:
        f["bucket"], f["why"] = "operational", OPER[code]
        continue
    if code in PARKED:
        p = PARKED[code]
        pb = p.get("baseline", base)
        f["why"], f["doc"] = p.get("reason", ""), p.get("doc", "")
        if pb is not None and cnt > pb:
            f["escalated"] = "עלה מעל הרמה המאושרת (%d) — חזר להיות ממצא פעיל" % pb
        else:
            f["bucket"] = "known"
        continue
    if base is not None and cnt <= base:
        f["bucket"], f["why"] = "known", "מתחת או שווה לרמה המאושרת (%d)" % base

json.dump({"ran_at": NOW.isoformat(), "counts": counts, "volumes": VOL, "errors": ERRORS,
           "buckets": {f["code"]: f["bucket"] for f in FINDINGS}},
          open(os.path.join(OUT, "state_new.json"), "w"), ensure_ascii=False, indent=1)

# ---- הפרדה בין פער אמיתי בבדיקה לבין הערה צפויה ומאושרת ----
# "אובייקט X ריק" כשידוע שהוא יצא משימוש הוא לא פער בבדיקה. זה רעש שמסתיר פערים אמיתיים.
EXPECT = EXC.get("expected_notes") or []
GAPS, NOTES = [], []
for _e in ERRORS:
    _hit = next((x for x in EXPECT if x.get("match") and x["match"] in _e), None)
    (NOTES.append({"text": _e, "reason": _hit.get("reason", "")}) if _hit else GAPS.append(_e))

# ================================================================ RENDER
SEV_ORDER = {"critical": 0, "high": 1, "medium": 2, "low": 3, "ok": 9}
SEV_HE = {"critical": "קריטי", "high": "גבוה", "medium": "בינוני", "low": "נמוך", "ok": "תקין"}
SEV_COL = {"critical": "#b3261e", "high": "#d97706", "medium": "#0369a1", "low": "#4b5563", "ok": "#15803d"}
_srt = lambda L: sorted(L, key=lambda f: (SEV_ORDER[f["sev"]], -f["count"]))
active = _srt([f for f in FINDINGS if f["count"] > 0 and f["bucket"] == "active"])
known  = _srt([f for f in FINDINGS if f["count"] > 0 and f["bucket"] == "known"])
oper   = _srt([f for f in FINDINGS if f["count"] > 0 and f["bucket"] == "operational"])
clean = [f for f in FINDINGS if f["count"] == 0]
nc = sum(1 for f in active if f["sev"] == "critical")
nh = sum(1 for f in active if f["sev"] == "high")

def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))

verdict = ("נמצאו תקלות קריטיות" if nc else ("נמצאו תקלות בעדיפות גבוהה" if nh else ("נמצאו תקלות מינוריות" if active else
           ("אין ממצא פעיל — רק פריטים ידועים ומטופלים" if (known or oper) else "לא נמצאו תקלות"))))
vcol = "#b3261e" if nc else ("#d97706" if nh else ("#0369a1" if active else "#15803d"))
MAX_SAMPLE = 10
def build(limit):
 H = []
 H.append('<div dir="rtl" style="font-family:Arial,Helvetica,sans-serif;background:#f4f5f7;padding:18px;margin:0">')
 H.append('<div style="max-width:860px;margin:0 auto;background:#ffffff;border-radius:10px;overflow:hidden;border:1px solid #e3e5e8">')
 H.append('<div style="background:#111827;color:#ffffff;padding:20px 24px">'
          '<div style="font-size:19px;font-weight:bold">בדיקת תקינות · פיירברי רויטל יעיש</div>'
          '<div style="font-size:13px;color:#c7cbd1;padding-top:5px">%s · הרצה אוטומטית · קריאה בלבד</div></div>'
          % NOW.strftime("%d/%m/%Y %H:%M"))
 H.append('<div style="padding:16px 24px;background:%s;color:#fff;font-size:16px;font-weight:bold">%s · %d ממצאים פעילים · %d קריטיים · %d גבוהים</div>'
          % (vcol, verdict, len(active), nc, nh))

 H.append('<div style="padding:18px 24px 4px 24px"><table cellpadding="0" cellspacing="0" style="width:100%;border-collapse:collapse"><tr>')
 for lbl, val, col in [("קריטי", nc, "#b3261e"), ("גבוה", nh, "#d97706"),
                       ("בינוני", sum(1 for f in active if f["sev"] == "medium"), "#0369a1"),
                       ("ידוע ומטופל", len(known), "#6b7280"),
                       ("תפעולי", len(oper), "#7c3aed"),
                       ("עברו נקי", len(clean), "#15803d")]:
     H.append('<td style="width:16%%;text-align:center;padding:10px 4px;border:1px solid #e6e8eb;background:#fafbfc">'
              '<div style="font-size:24px;font-weight:bold;color:%s">%d</div>'
              '<div style="font-size:11px;color:#6b7280;padding-top:2px">%s</div></td>' % (col, val, lbl))
 H.append('</tr></table></div>')

 H.append('<div style="padding:12px 24px;font-size:12px;color:#4b5563">נפחים שנסרקו: ' +
          " · ".join("%s <b>%d</b>" % (k, v) for k, v in VOL.items()) + '</div>')

 if not active:
     H.append('<div style="padding:24px;font-size:15px;color:#15803d;font-weight:bold">כל %d הבדיקות עברו. אין ממצא פעיל.</div>' % len(FINDINGS))

 for f in active:
     col = SEV_COL[f["sev"]]
     d = f.get("delta")
     if d is None: dtxt = '<span style="color:#6b7280">חדש בבדיקה</span>'
     elif d > 0:   dtxt = '<span style="color:#b3261e;font-weight:bold">▲ %+d מההרצה הקודמת</span>' % d
     elif d < 0:   dtxt = '<span style="color:#15803d;font-weight:bold">▼ %d מההרצה הקודמת</span>' % d
     else:         dtxt = '<span style="color:#6b7280">ללא שינוי</span>'
     if f.get("backlog"): dtxt += ' · <span style="color:#6b7280">ועוד %s בחוב ההגירה</span>' % "{:,}".format(f["backlog"])
     H.append('<div style="margin:14px 24px;border:1px solid #e6e8eb;border-right:5px solid %s;border-radius:6px">' % col)
     H.append('<div style="padding:12px 14px;background:#fafbfc">'
              '<span style="background:%s;color:#fff;font-size:11px;padding:2px 8px;border-radius:9px">%s</span> '
              '<span style="font-size:15px;font-weight:bold;color:#111827">%s</span> '
              '<span style="font-size:15px;font-weight:bold;color:%s">· %d</span>'
              '<div style="font-size:11px;color:#6b7280;padding-top:5px">קוד %s · %s%s</div>'
              % (col, SEV_HE[f["sev"]], esc(f["title"]), col, f["count"], f["code"], dtxt,
                 (" · באחריות " + esc(f["owner"])) if f["owner"] else ""))
     if f["note"]:
         H.append('<div style="font-size:12px;color:#374151;padding-top:7px;line-height:1.5">%s</div>' % esc(f["note"]))
     if f.get("escalated"):
         H.append('<div style="margin-top:8px;padding:6px 9px;background:#fff1f0;border:1px solid #f3c9c6;border-radius:4px;font-size:11px;color:#b3261e;font-weight:bold">%s</div>' % esc(f["escalated"]))
     H.append('</div>')
     if f["sample"]:
         keys = [k for k in f["sample"][0].keys() if k != "link"]
         H.append('<table cellpadding="6" cellspacing="0" style="width:100%;border-collapse:collapse;font-size:12px">')
         H.append('<tr style="background:#f1f3f5">' + "".join('<th align="right" style="border-top:1px solid #e6e8eb;color:#374151">%s</th>' % esc(k) for k in keys) +
                  ('<th align="right" style="border-top:1px solid #e6e8eb"></th>' if "link" in f["sample"][0] else "") + '</tr>')
         for row in f["sample"][:limit]:
             H.append('<tr>' + "".join('<td align="right" style="border-top:1px solid #eef0f2;color:#111827">%s</td>' % esc(row.get(k, "")) for k in keys) +
                      ('<td align="right" style="border-top:1px solid #eef0f2"><a href="%s" style="color:#1d4ed8">רשומה</a></td>' % row["link"] if "link" in row else "") + '</tr>')
         H.append('</table>')
         if f["count"] > len(f["sample"][:limit]):
             H.append('<div style="font-size:11px;color:#6b7280;padding:7px 14px">מוצגות %d מתוך %d. הרשימה המלאה זמינה לפי בקשה.</div>' % (len(f["sample"][:limit]), f["count"]))
     H.append('</div>')

 for grp, ttl, sub, bg, bd, fg in [
     (known, "ידוע ומטופל — לא נספר כממצא פעיל", "ממצאים אמיתיים שכבר הוכרעו וממתינים לתיקון שורש או להחלטה. אם המספר עולה מעל הרמה המאושרת הם חוזרים אוטומטית לרשימת הפעילים.", "#f8f9fa", "#dde1e6", "#374151"),
     (oper, "תפעולי — באחריות הצוות של רויטל", "עומס עבודה שוטף, לא תקלת מערכת. מוצג כדי שיהיה גלוי, לא כדי שייחשב תקלה.", "#faf8ff", "#e2d9f5", "#5b21b6")]:
  if not grp: continue
  H.append('<div style="margin:16px 24px;padding:12px 14px;border:1px solid %s;background:%s;border-radius:6px">'
           '<div style="font-size:13px;font-weight:bold;color:%s">%s (%d)</div>'
           '<div style="font-size:11px;color:#6b7280;padding-top:4px;line-height:1.5">%s</div>' % (bd, bg, fg, ttl, len(grp), sub))
  H.append('<table cellpadding="5" cellspacing="0" style="width:100%;border-collapse:collapse;font-size:12px;margin-top:8px">')
  for f in grp:
      d = f.get("delta")
      dtx = "חדש" if d is None else ("%+d" % d if d else "ללא שינוי")
      H.append('<tr><td align="right" style="border-top:1px solid #e6e8eb;color:#111827">%s'
               '<div style="font-size:10px;color:#9ca3af">קוד %s · %s%s</div>'
               '<div style="font-size:11px;color:#4b5563;padding-top:3px;line-height:1.5">%s</div></td>'
               '<td align="right" style="border-top:1px solid #e6e8eb;font-weight:bold;color:%s;width:60px">%s</td></tr>'
               % (esc(f["title"]), f["code"], dtx,
                  (" · מסמך: " + esc(f["doc"])) if f.get("doc") else "",
                  esc(f.get("why") or ""), fg, "{:,}".format(f["count"])))
  H.append('</table></div>')

 if BACKLOG:
  B = sorted(BACKLOG, key=lambda b: -b["count"])
  H.append('<div style="margin:16px 24px;padding:12px 14px;border:1px solid #dde1e6;background:#f8f9fa;border-radius:6px">'
           '<div style="font-size:13px;font-weight:bold;color:#374151">חוב הגירה — לא תקלה חיה (%d סעיפים)</div>'
           '<div style="font-size:11px;color:#6b7280;padding-top:4px">רשומות שנולדו בהגירה. הן לא נספרות בממצאים למעלה, כדי שהדוח יישאר תפעולי.</div>' % len(B))
  H.append('<table cellpadding="5" cellspacing="0" style="width:100%;border-collapse:collapse;font-size:12px;margin-top:8px">')
  for b in B[:22]:
      H.append('<tr><td align="right" style="border-top:1px solid #e6e8eb;color:#111827">%s</td>'
               '<td align="right" style="border-top:1px solid #e6e8eb;font-weight:bold;color:#374151;width:80px">%s</td>'
               '<td align="right" style="border-top:1px solid #e6e8eb;color:#6b7280">%s</td></tr>'
               % (esc(b["title"]), "{:,}".format(b["count"]), esc(b["note"])))
  H.append('</table></div>')

 if clean:
     H.append('<div style="margin:16px 24px;padding:12px 14px;border:1px solid #d7ecd9;background:#f3faf4;border-radius:6px">'
              '<div style="font-size:13px;font-weight:bold;color:#15803d">בדיקות שעברו נקי (%d)</div>'
              '<div style="font-size:12px;color:#374151;padding-top:6px;line-height:1.7">%s</div></div>'
              % (len(clean), " · ".join(esc(f["title"]) for f in clean)))

 if GAPS:
     H.append('<div style="margin:16px 24px;padding:12px 14px;border:1px solid #f0d9a8;background:#fffbf0;border-radius:6px">'
              '<div style="font-size:13px;font-weight:bold;color:#a16207">מה לא נבדק בהרצה הזו — פער אמיתי</div>'
              '<div style="font-size:12px;color:#374151;padding-top:6px;line-height:1.7">%s</div></div>'
              % "<br>".join(esc(e) for e in GAPS))
 if NOTES:
     H.append('<div style="margin:16px 24px;padding:10px 14px;border:1px solid #e6e8eb;background:#fafbfc;border-radius:6px">'
              '<div style="font-size:12px;font-weight:bold;color:#6b7280">הערות צפויות — לא פער</div>'
              '<div style="font-size:11px;color:#6b7280;padding-top:5px;line-height:1.7">%s</div></div>'
              % "<br>".join("%s <span style=\"color:#9ca3af\">— %s</span>" % (esc(n["text"]), esc(n["reason"])) for n in NOTES))

 H.append('<div style="padding:16px 24px;background:#f6f7f8;border-top:1px solid #e6e8eb;font-size:11px;color:#6b7280;line-height:1.6">'
          'הבדיקה היא קריאה בלבד. לא נוצרה, לא עודכנה ולא נמחקה שום רשומה בפיירברי, ב-n8n או ב-Make.<br>'
          'ויטרו · ניטור אוטומטי · פעמיים ביום בשעות 08:00 ו-16:00</div>')
 H.append('</div></div>')
 ated_html = "".join(H)
 return ated_html

html = build(MAX_SAMPLE)
for lim in (8, 6, 4, 3, 2):
    if len(html.encode()) <= 92000: break
    html = build(lim)
open(os.path.join(OUT, "report.html"), "w").write(html)
json.dump({"ran_at": NOW.isoformat(), "verdict": verdict, "critical": nc, "high": nh,
           "volumes": VOL, "errors": GAPS, "notes": NOTES, "findings": FINDINGS, "backlog": BACKLOG},
          open(os.path.join(OUT, "report.json"), "w"), ensure_ascii=False, indent=1)
print("VERDICT=%s | active=%d critical=%d high=%d | html=%dKB" % (verdict, len(active), nc, nh, len(html.encode()) // 1024))


# ================================================================ EMAIL (compact)
import subprocess
try:
    open(os.path.join(OUT, "email.html"), "w").write(__import__("mkemail").render(json.load(open(os.path.join(OUT, "report.json")))))
    print("email.html written")
except Exception as e:
    print("mkemail failed: %s" % e)
