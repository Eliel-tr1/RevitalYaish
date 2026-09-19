# פרומפט לקלוד קוד — העלאת דשבורד רויטל יעיש ל-ai.vitrue.co.il

> העתק את כל מה שמתחת לקו לתוך Claude Code בטרמינל.

---

אתה מבצע פריסה של דשבורד ללקוחה של ויטרו. קרא הכול לפני שאתה מתחיל, ואל תדלג על אזהרת הבטיחות.

## הקשר

**הלקוחה:** רויטל יעיש — "המרכז לבריאות והרזייה", תוכניות תזונה והרזיה אונליין. ה-CRM שלה הוא Fireberry (שכפול של תבנית ויטרו). הפרויקט הוא הטמעת CRM; שלב 15 הוא לוחות בקרה, שנמכר כאפסייל נפרד.

**מה נבנה:** דשבורד web חיצוני (לא בתוך Fireberry) עם 6 לוחות — שיווק ולידים · ליווי ולקוחות · תוצאות ומגמות משקל · וובינר ומחזורים · תפריטים ותשלום לדיאטניות · מכירות. עברית RTL, כהה/בהיר, רספונסיבי מלא, מוגן בסיסמה.

**הארכיטקטורה:**
```
Fireberry ──v3, דלתא לפי modifiedon──► Supabase Edge Function `fb-sync`
                                                │ UPSERT
                                                ▼
                                    Postgres · 19 טבלאות מראה
                                                │
                                                ▼
                                    Edge Function `dash-api` (אימות + JSON)
                                                │
                                                ▼
                                    index.html · קובץ יחיד · SPA
```
- פרויקט Supabase: `revital-dashboard`, ref **`klobimzmuurzbimfkubr`**, אזור eu-central-1
- סנכרון יומי אוטומטי ב-04:30 שעון ישראל (pg_cron) · **19 קריאות API לסנכרון** (דלתא)
- הטוקן של Fireberry יושב **רק בצד שרת** (`app_config` בתוך Supabase). הוא לא נמצא ב-`index.html` — אל תחפש אותו שם ואל תוסיף אותו.

**המשימה שלך:** להעלות קובץ `index.html` יחיד ל-SFTP של `ai.vitrue.co.il`, ואז לוודא שהכול עובד בפועל.

---

## 🔴 אזהרת בטיחות — קרא לפני שאתה כותב משהו לשרת

**`https://ai.vitrue.co.il/` כבר מארח אתר קיים** — "מחשבון ROI | ויטרו". אם תעלה `index.html` ל-web root אתה **דורס אותו**.

לכן:
1. **פרוס לתת-תיקייה: `revital/`.** היעד הוא `<web-root>/revital/index.html`, והכתובת הסופית `https://ai.vitrue.co.il/revital/`.
2. **אל תמחק ואל תדרוס שום קובץ קיים.** אם `revital/index.html` כבר קיים — הורד אותו קודם לגיבוי מקומי בשם `index.html.bak-<תאריך>`.
3. אם משום מה תחליט בכל זאת שצריך את ה-root — **עצור ושאל את מייק**. לא להחליט את זה לבד.

---

## פרטי גישה

**SFTP:**
```
Host: 46.225.19.194   (או ai.vitrue.co.il)
Port: 22
User: vitrue-ai
Pass: 8GwAQUj7TdIsb91ROCue
```
ה-web root לא מאומת. בשרת אחות באותו IP הדפוס הוא `htdocs/<domain>/`, כלומר סביר ש-**`htdocs/ai.vitrue.co.il/`**. **תאמת את זה בעצמך**: התחבר, `ls`, ומצא את התיקייה שבה יושב ה-`index.html` של מחשבון ה-ROI. **זה ה-web root.** אל תנחש.

**סיסמת הדשבורד:** `revital2026`

---

## שלב 1 — משיכת הקובץ

הקובץ חי ומוגש מ-Supabase. אל תבנה אותו מחדש:

```bash
curl -s "https://klobimzmuurzbimfkubr.supabase.co/functions/v1/app" -o index.html
ls -l index.html          # צפוי ~283,117 בתים
md5sum index.html         # חייב להיות: 412e448b050843fd1251b060aa0e6b6b
```

**אם ה-md5 לא תואם — עצור ודווח.** אל תעלה קובץ שלא אימתת.

הקובץ הוא HTML יחיד, self-contained: כל ה-CSS, כל ה-JS ו-Chart.js בתוכו. אין assets נלווים, אין build, אין תלויות. הוא פונה ל-`https://klobimzmuurzbimfkubr.supabase.co/functions/v1/dash-api` בלבד.

## שלב 2 — העלאה

Python + paramiko. אל תשתמש ב-`sftp` אינטראקטיבי.

```python
import paramiko, os, datetime
HOST, PORT, USER, PASS = "46.225.19.194", 22, "vitrue-ai", "8GwAQUj7TdIsb91ROCue"

t = paramiko.Transport((HOST, PORT)); t.connect(username=USER, password=PASS)
s = paramiko.SFTPClient.from_transport(t)

print("root:", s.listdir("."))          # ← מצא כאן את ה-web root האמיתי
WEBROOT = "htdocs/ai.vitrue.co.il"      # ← עדכן למה שראית בפועל
print("webroot:", s.listdir(WEBROOT))   # ← ודא שיש כאן index.html של מחשבון ה-ROI

DEST_DIR = f"{WEBROOT}/revital"
try: s.stat(DEST_DIR)
except FileNotFoundError: s.mkdir(DEST_DIR)

REMOTE = f"{DEST_DIR}/index.html"
try:                                     # גיבוי אם כבר קיים
    s.stat(REMOTE)
    bak = REMOTE + ".bak-" + datetime.date.today().isoformat()
    s.get(REMOTE, "index.html.bak"); s.put("index.html.bak", bak)
    print("backed up ->", bak)
except FileNotFoundError:
    print("no previous file, first deploy")

s.put("index.html", REMOTE)
print("local", os.path.getsize("index.html"), "remote", s.stat(REMOTE).st_size)
s.close(); t.close()
```

**הגדלים חייבים להיות זהים.** אם לא — העלה שוב.

## שלב 3 — בדיקת תקינות

**א. השרת מגיש נכון**
```bash
curl -sI https://ai.vitrue.co.il/revital/ | head -12
```
דרוש: `HTTP 200` · `content-type: text/html`. אם חוזר 403/404 — בדוק שה-`WEBROOT` נכון ושהרשאות הקובץ 644 והתיקייה 755.

```bash
curl -s https://ai.vitrue.co.il/revital/ | md5sum   # 412e448b050843fd1251b060aa0e6b6b
```

**ב. האתר הקיים לא נפגע — בדיקה מחייבת**
```bash
curl -s https://ai.vitrue.co.il/ | grep -o "<title>.*</title>"
```
חייב עדיין להחזיר **"מחשבון ROI | ויטרו"**. אם לא — **דרסת את האתר. שחזר מיד ודווח למייק.**

**ג. שכבת ה-API חיה**
```bash
curl -s -X POST "https://klobimzmuurzbimfkubr.supabase.co/functions/v1/dash-api" \
  -H "Content-Type: application/json" -d '{"action":"login","password":"revital2026"}'
```
צפוי `{"token":"…"}`. סיסמה שגויה חייבת להחזיר `401 bad_password`.

**ד. בדיקה בדפדפן — לא לדלג**
פתח `https://ai.vitrue.co.il/revital/` בדפדפן אמיתי ועבור על הרשימה:

| # | בדיקה | מה מצופה |
|---|---|---|
| 1 | סיסמה שגויה | "סיסמה שגויה", אין כניסה |
| 2 | `revital2026` | נכנס, נטען לוח השיווק |
| 3 | 6 הטאבים בסרגל | כל אחד מציג כותרת, כרטיסי KPI וגרפים |
| 4 | טווחי תאריכים | 7 יום ≈ 210 לידים · הכול = 778 |
| 5 | המסננים | משנים מספרים; מסננים לא רלוונטיים ללוח **מעומעמים ומנוטרלים** — זו התנהגות מכוונת |
| 6 | דריל-דאון בלוח התוצאות | החלפת לקוחה מחליפה עקומה |
| 7 | מתג נושא ☾/☀ | כהה ובהיר תקינים |
| 8 | **"סנכרן עכשיו"** | 30–60 שניות ואז "✓ עודכן · N קריאות". חותמת הזמן מתעדכנת |
| 9 | פאנל "מצב הסנכרון" בתחתית | 19 אובייקטים · **2,307 רשומות** · יומן 5 ריצות אחרונות |
| 10 | קונסול הדפדפן | **0 שגיאות** |
| 11 | מובייל (390px) | תפריט המבורגר, מגירת מסננים, **אפס גלילה אופקית** |

**ה. אין דליפת סודות**
```bash
curl -s https://ai.vitrue.co.il/revital/ | grep -ciE "tokenid|fireberry_token|service_role|b06663c4"
```
חייב להחזיר **0**.

## שלב 4 — דיווח

דווח למייק בעברית: הכתובת החיה, גודל ו-md5, אישור ש-11 בדיקות הדפדפן עברו, אישור שמחשבון ה-ROI שלם, וכל חריגה. אם משהו נכשל — **מה בדיוק, ומה ניסית**, בלי לנחש.

---

## מה לא לעשות

- ❌ אל תיגע בשום קובץ מחוץ ל-`<web-root>/revital/`
- ❌ אל תמחק כלום מהשרת
- ❌ אל תערוך את `index.html` — הוא נבדק ואומת. שינויים נעשים במקור ואז נפרסים מחדש
- ❌ אל תיצור מחדש את הפרויקט ב-Supabase, ואל תריץ `fb-sync` עם `{"full":true}` בלי צורך
- ❌ אל תכתוב שום דבר ל-Fireberry. הפרויקט הזה הוא **קריאה בלבד**
- ❌ אל תיגע ב-Make

## פתוח — לידיעתך, לא לביצוע עכשיו

1. 🔴 **טוקן Fireberry נחשף בצ'אטים — חובה רוטציה לפני מסירה ללקוחה.** 4 מקומות לעדכן: Make · n8n · `1036.pcfPowerlinkToken` · `app_config.fireberry_token`
2. סיסמת הדשבורד היא ברירת מחדל — להחליף לפני מסירה
3. שווה להוסיף HTTP Basic ב-`.htaccess` מעל הסיסמה
4. הלוגו הרשמי של רויטל טרם התקבל — כרגע סמל זמני בצבע המותג `#FF004F`

**תיעוד מלא:** `15_DASHBOARD_MASTER_PLAN.md` (תכנון) ו-`15_DASHBOARD_HANDOFF.md` (תפעול) ב-Project Knowledge · [משימת ClickUp](https://app.clickup.com/t/86cawzgaz)
