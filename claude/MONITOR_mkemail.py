#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""בונה את גוף המייל הקומפקטי מתוך report.json"""
import json, sys, os
from datetime import datetime
SEV_HE = {"critical": "קריטי", "high": "גבוה", "medium": "בינוני", "low": "נמוך"}
SEV_COL = {"critical": "#b3261e", "high": "#d97706", "medium": "#0369a1", "low": "#4b5563"}
SEV_ORDER = {"critical": 0, "high": 1, "medium": 2, "low": 3}
def esc(s): return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def render(D):
    FINDINGS = D["findings"]; BACKLOG = D.get("backlog") or []; ERRORS = D.get("errors") or []
    VOL = D["volumes"]
    _b = lambda f: f.get("bucket") or "active"
    _srt = lambda L: sorted(L, key=lambda f: (SEV_ORDER[f["sev"]], -f["count"]))
    active = _srt([f for f in FINDINGS if f["count"] and _b(f) == "active"])
    known = _srt([f for f in FINDINGS if f["count"] and _b(f) == "known"])
    oper = _srt([f for f in FINDINGS if f["count"] and _b(f) == "operational"])
    clean = [f for f in FINDINGS if not f["count"]]
    nc = sum(1 for f in active if f["sev"] == "critical"); nh = sum(1 for f in active if f["sev"] == "high")
    verdict = D.get("verdict") or ""
    vcol = "#b3261e" if nc else ("#d97706" if nh else ("#0369a1" if active else "#15803d"))
    NOW = datetime.fromisoformat(D["ran_at"])
    E = []
    E.append('<div dir="rtl" style="font-family:Arial,Helvetica,sans-serif;background:#f4f5f7;padding:14px;margin:0">')
    E.append('<div style="max-width:760px;margin:0 auto;background:#fff;border:1px solid #e3e5e8;border-radius:10px;overflow:hidden">')
    E.append('<div style="background:#111827;color:#fff;padding:18px 20px"><div style="font-size:18px;font-weight:bold">'
             'בדיקת תקינות · פיירברי רויטל יעיש</div><div style="font-size:12px;color:#c7cbd1;padding-top:4px">%s · הרצה אוטומטית · קריאה בלבד</div></div>'
             % NOW.strftime("%d/%m/%Y %H:%M"))
    E.append('<div style="padding:14px 20px;background:%s;color:#fff;font-size:15px;font-weight:bold">%s · %d ממצאים פעילים · %d קריטיים · %d גבוהים</div>'
             % (vcol, verdict, len(active), nc, nh))
    E.append('<div style="padding:9px 20px;background:#f1f3f5;font-size:11px;color:#4b5563;border-bottom:1px solid #e6e8eb">'
             'בנוסף: <b>%d</b> ידועים ומטופלים · <b>%d</b> תפעוליים באחריות הצוות · <b>%d</b> בדיקות עברו נקי. '
             'פריט ידוע חוזר להיות פעיל אוטומטית אם הוא עולה מעל הרמה המאושרת.</div>' % (len(known), len(oper), len(clean)))
    E.append('<div style="padding:12px 20px;font-size:11px;color:#4b5563">נסרקו: ' +
             " · ".join("%s %s" % (k, "{:,}".format(v)) for k, v in VOL.items()) + '</div>')
    if not active:
        E.append('<div style="padding:20px;font-size:15px;color:#15803d;font-weight:bold">אין ממצא פעיל בהרצה הזו.</div>')
    else:
        E.append('<table cellpadding="7" cellspacing="0" style="width:100%;border-collapse:collapse;font-size:12px">')
        E.append('<tr style="background:#f1f3f5"><th align="right">חומרה</th><th align="right">ממצא</th><th align="right">כמות</th>'
                 '<th align="right">שינוי</th><th align="right">חוב הגירה</th><th align="right">אחראי</th></tr>')
        for f in active:
            d = f.get("delta")
            dtx = "חדש" if d is None else ("%+d" % d if d else "—")
            dcol = "#b3261e" if (d or 0) > 0 else ("#15803d" if (d or 0) < 0 else "#6b7280")
            E.append('<tr><td align="right" style="border-top:1px solid #eef0f2"><span style="background:%s;color:#fff;font-size:10px;padding:2px 7px;border-radius:9px">%s</span></td>'
                     '<td align="right" style="border-top:1px solid #eef0f2;color:#111827">%s<div style="font-size:10px;color:#9ca3af">%s</div></td>'
                     '<td align="right" style="border-top:1px solid #eef0f2;font-weight:bold;color:%s">%s</td>'
                     '<td align="right" style="border-top:1px solid #eef0f2;color:%s">%s</td>'
                     '<td align="right" style="border-top:1px solid #eef0f2;color:#6b7280">%s</td>'
                     '<td align="right" style="border-top:1px solid #eef0f2;color:#6b7280">%s</td></tr>'
                     % (SEV_COL[f["sev"]], SEV_HE[f["sev"]], esc(f["title"]), f["code"],
                        SEV_COL[f["sev"]], "{:,}".format(f["count"]), dcol, dtx,
                        ("{:,}".format(f["backlog"]) if f.get("backlog") else "—"), esc(f["owner"] or "—")))
            if f.get("escalated"):
                E.append('<tr><td colspan="6" align="right" style="background:#fff1f0;color:#b3261e;font-size:11px;font-weight:bold;padding:4px 7px">%s · %s</td></tr>'
                         % (esc(f["code"]), esc(f["escalated"])))
        E.append('</table>')
        top = [f for f in active if f["sev"] in ("critical", "high")][:6]
        if top:
            E.append('<div style="padding:14px 20px 4px 20px;font-size:13px;font-weight:bold;color:#111827">דוגמאות מהממצאים הדחופים</div>')
        for f in top:
            E.append('<div style="margin:8px 20px;border:1px solid #e6e8eb;border-right:4px solid %s;border-radius:5px;padding:9px 11px">'
                     '<div style="font-size:12px;font-weight:bold;color:#111827">%s · %s</div>' % (SEV_COL[f["sev"]], esc(f["title"]), "{:,}".format(f["count"])))
            if f["note"]: E.append('<div style="font-size:11px;color:#374151;padding-top:4px;line-height:1.5">%s</div>' % esc(f["note"]))
            for row in f["sample"][:3]:
                txt = " · ".join("%s: %s" % (k, esc(v)) for k, v in row.items() if k != "link")
                lnk = (' <a href="%s" style="color:#1d4ed8">רשומה</a>' % row["link"]) if row.get("link") else ""
                E.append('<div style="font-size:11px;color:#4b5563;padding-top:3px">• %s%s</div>' % (txt, lnk))
            E.append('</div>')
    for grp, ttl, sub, bg, bd, fg in [
        (known, "ידוע ומטופל — לא נספר כממצא פעיל",
         "ממצאים אמיתיים שכבר הוכרעו וממתינים לתיקון שורש או להחלטה. עולים מעל הרמה המאושרת — חוזרים אוטומטית לפעילים.",
         "#f8f9fa", "#dde1e6", "#374151"),
        (oper, "תפעולי — באחריות הצוות של רויטל",
         "עומס עבודה שוטף, לא תקלת מערכת.", "#faf8ff", "#e2d9f5", "#5b21b6")]:
        if not grp: continue
        E.append('<div style="margin:14px 20px;padding:10px 12px;background:%s;border:1px solid %s;border-radius:5px">'
                 '<div style="font-size:12px;font-weight:bold;color:%s">%s (%d)</div>'
                 '<div style="font-size:11px;color:#6b7280;padding-top:3px;line-height:1.5">%s</div>' % (bg, bd, fg, ttl, len(grp), sub))
        E.append('<table cellpadding="5" cellspacing="0" style="width:100%;border-collapse:collapse;font-size:11px;margin-top:7px">')
        for f in grp:
            d = f.get("delta")
            dtx = "חדש" if d is None else ("%+d" % d if d else "ללא שינוי")
            E.append('<tr><td align="right" style="border-top:1px solid #e6e8eb;color:#111827">%s'
                     '<div style="font-size:10px;color:#9ca3af">קוד %s · %s%s</div>'
                     '<div style="font-size:11px;color:#4b5563;padding-top:2px;line-height:1.5">%s</div></td>'
                     '<td align="right" style="border-top:1px solid #e6e8eb;font-weight:bold;color:%s;width:55px">%s</td></tr>'
                     % (esc(f["title"]), f["code"], dtx,
                        (" · מסמך: " + esc(f["doc"])) if f.get("doc") else "",
                        esc(f.get("why") or ""), fg, "{:,}".format(f["count"])))
        E.append('</table></div>')
    if BACKLOG:
        E.append('<div style="margin:14px 20px;padding:10px 12px;background:#f8f9fa;border:1px solid #dde1e6;border-radius:5px;font-size:11px;color:#4b5563">'
                 '<b style="color:#374151">חוב הגירה (לא תקלה חיה): %s רשומות ב-%d סעיפים.</b> '
                 'הגדולים: %s' % ("{:,}".format(sum(b["count"] for b in BACKLOG)), len(BACKLOG),
                                  " · ".join("%s (%s)" % (esc(b["title"]), "{:,}".format(b["count"]))
                                             for b in sorted(BACKLOG, key=lambda b: -b["count"])[:5])) + '</div>')
    if ERRORS:
        E.append('<div style="margin:14px 20px;padding:10px 12px;background:#fffbf0;border:1px solid #f0d9a8;border-radius:5px">'
                 '<div style="font-size:12px;font-weight:bold;color:#a16207">מה לא נבדק בהרצה הזו — פער אמיתי</div>'
                 '<div style="font-size:11px;color:#374151;padding-top:5px;line-height:1.6">%s</div></div>'
                 % "<br>".join(esc(e) for e in ERRORS))
    NOTES = D.get("notes") or []
    if NOTES:
        E.append('<div style="margin:14px 20px;padding:9px 12px;background:#fafbfc;border:1px solid #e6e8eb;border-radius:5px">'
                 '<div style="font-size:11px;font-weight:bold;color:#6b7280">הערות צפויות — לא פער</div>'
                 '<div style="font-size:11px;color:#6b7280;padding-top:4px;line-height:1.6">%s</div></div>'
                 % "<br>".join('%s <span style="color:#9ca3af">— %s</span>' % (esc(n["text"]), esc(n.get("reason", ""))) for n in NOTES))
    E.append('<div style="padding:14px 20px;background:#f6f7f8;border-top:1px solid #e6e8eb;font-size:10px;color:#6b7280;line-height:1.6">'
             'קריאה בלבד — לא נוצרה, עודכנה או נמחקה שום רשומה בפיירברי, ב-n8n או ב-Make.<br>'
             'הדוח המלא עם כל הרשומות נשמר בידע הפרויקט בקלוד: <b>claude/MONITOR_report_latest.html</b><br>'
             'ויטרו · ניטור אוטומטי · 08:00 ו-16:00</div></div></div>')
    return "".join(E)


if __name__ == "__main__":
    d = json.load(open(sys.argv[1] if len(sys.argv) > 1 else "report.json"))
    out = sys.argv[2] if len(sys.argv) > 2 else "email.html"
    open(out, "w").write(render(d))
    print("%s · %dKB" % (out, len(render(d).encode()) // 1024))
