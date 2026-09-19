# HANDOFF — Roital Yaish Implementation · Boost Cycles & Coaching Model

> **עודכן 03/08/2026 — סקירת 26 שיחות הפרויקט.**

| # | מה שונה | מקור |
|---|---|---|
| 1 | מספר מחזורי הבוסט: **74 מחזורים אומתו חי ב-02/08/2026** מול 22 שתועדו קודם — ⚠️ סתירה פתוחה, בעלים מייק | chat_03 · אימות API 02/08/2026 |
| 2 | 🔴 **גורל אובייקט ההרשמה `1005` — שלוש עמדות סותרות.** כל בנייה שנשענת על 1005 **מוקפאת**. `4.pcfBoostLinked` = זומבי | chat_20 · chat_25 · chat_27 |
| 3 | נוסף פרק מלא: **WF-17 — מכירת ליווי לאחר בוסט** (n8n `e30cNECSoBNJDQcf`, 19 צמתים, מושבת, `DRY_RUN=true`) | chat_03 |
| 4 | תוקן: **"מסלול ליווי 12 חודשים" לא קיים** — המוצר הוא **תוכנית ליווי 12 שבועות**, GUID `d9e842a7-f284-4596-bb61-4d2a350eebb5`, 3,601.69 ₪ לפני מע"מ | chat_03 |
| 5 | נוסף **פרק ניתוח תמחור מסחרי** — חיווט בוסט→12 שבועות הופך את 12 שבועות למוצר ברירת המחדל; 4,250 ₪ מול 3,850 ₪ ל-8 שבועות | chat_03 · chat_08 |
| 6 | **WF-16 (מסלול מת) עודכן לעקביות** — לקוחה עם תהליך מכירה פתוח שמצביע על עסקת בוסט כבר לא מסומנת "לא המירה" | chat_03 |
| 7 | תוקן: **שיוך לקבוצה — הנציג בוחר קבוצה לפני התשלום**, השיוך נורה אוטומטית ברגע התשלום. קבוצה↔מנטורית = 1:1. אין קשר בין אורך מסלול לקבוצה | chat_03 · chat_20 |
| 8 | נוסף **מצב הדאטה החי 02/08/2026**: 176 תהליכי מכירה · 175 בסטטוס "ליד חדש" · 2 משויכים למחזור · 0 ב"עסקה נסגרה בהצלחה" → WF-17 מחזיר אפס = תקין | chat_03 |
| 9 | 🔴 נוסף סיכון: מילוי רטרואקטיבי של `pcfCourse` ללא פילטר תשלום יפתח **175 תהליכי מכירה בבת אחת** | chat_03 |
| 10 | 🐛 נוסף באג דאטה: מחזור **"בוסט · אוגוסט 02"** נושא תאריך התחלה **09.08** וכופל את "בוסט · אוגוסט 09" (מסומן "התבטל") | chat_03 |
| 11 | נוסף: **תפריטי הבוסט ממופים ל"סטנדרטי" ב-`pcfMenuType`** שיש בו 2 ערכים בלבד — בוסט אינו מסלול נפרד במישור התפריטים | chat_14 |
| 12 | ⚠️ סתירה פתוחה: **עסקה אחת או שתיים?** המסמך תיאר עסקת פרימיום שנפתחת אוטומטית; מייק: "תהליך מכירה, יש תמיד אחד, לא 2" | chat_08 מול chat_27 |
| 13 | תוקן: **תזמון הוובינר = יום 3 מתחילת המחזור** (רביעי), לא 4 ימים ולא מהרכישה; ההזמנה יוצאת בבוקר יום הוובינר | chat_17 |
| 14 | נוסף **מודל 4 החלונות** של סטטוס המחזור + האינווריאנט "בכל רגע בדיוק אחד פתוח ובדיוק אחד פעיל" | chat_21 |
| 15 | נוסף: מנגנון קישור **`1032.pcfExternalSoftwareID1` = מזהה המחזור** (אין lookup); 1030 ו-1032 ריקים; הם **הוובינר**, לא מודל מתחרה | chat_17 · chat_26 |
| 16 | נוסף חוסם דאטה: **רק מחזור אחד מתוך 22 עם `pcfEventLink` מלא** | chat_19 |
| 17 | נוסף: **1007↔1068 lookup** + כתיבה אוטומטית של `4.pcfCourse` ו-`1051.pcfBoostLinked` בעת הצירוף לקבוצה | chat_20 |
| 18 | נוסף פרק **"נקודת יציאה לא מנוצלת"** — `1051.pcfStatus=8`, 50–120 נשים בשבוע, אפס רימרקטינג | chat_23 |
| 19 | נוסף: **נפח המחזור מתועד בשני טווחים** — 50–60 מול 50–120 | chat_27 מול chat_23 |
| 20 | נוסף: **רילייבל "מחזור בוסט"→"מחזור" לא הוכרע**; גורר 5 תוויות | chat_25 |
| 21 | נוסף לציר הזמן: `pcfEndSaleDate = pcfStartDate`; **הקבוצה נפתחת ~4 שבועות לפני תחילת המכירה** | chat_15 |
| 22 | נוסף פרק תלויות: **תרחיש התשלום של הבוסט מוקפא** (משולם) — WF-16 ו-WF-17 יושבים במורד הזרם שלו | chat_16 · chat_27 |
| 23 | נוסף: **טבלת קטגוריה→מסלול→חובת חתימה** (`categorycode` 101/102); 102 פתוח להכרעה | chat_11 · chat_12 |
| 24 | נוסף פרק **סודות לרוטציה** — 5 מפתחות, ⚠️ נחשף בצ'אט — לרוטציה. **ערכים לעולם לא נרשמים במסמך** | chat_20–27 |
| 25 | נוסף: **22 המחזורים ייגמרו והמערכת תיעצר בשקט** — בעלים עודד | chat_22 |
| 26 | נוסף: האוטומציה הפנימית היומית 00:01 **מיועדת לכיבוי** לטובת workflow ב-n8n | chat_27 |

---

> **Audience: Claude only.** This is a Claude-to-Claude knowledge transfer. A future chat should be able to read this cold and fully understand how the Boost program, the coaching process, the sales flow, and the payment webhook are architected — including *why* each decision was made. Written in English per the Claude-to-Claude convention; all Fireberry object/field names kept in their real (Hebrew/system) form so you can act on the live system.
>
> **הערה 03/08/2026:** כל התוספות והתיקונים מסבב הסקירה נכתבים **בעברית**, בתוך הסעיפים הרלוונטיים. הגוף האנגלי המקורי נשמר כלשונו למעט תיקונים מסומנים.

---

## 0. Orientation — who and what

**Client:** Roital Yaish (רויטל יעיש) — online women's wellness & weight-loss coaching business.
**Implementer:** Vitrue consultancy. **Mike (מיכאל)** builds the CRM/Make/automations and manages all processes. **Tal (טל)** owns the AI bot that sends all customer-facing messages. **Eliel** is the reviewer who reads Hebrew change-logs. **עודד** — בעלים של חוסמי דאטה (לינקי קבוצות, טבלת מחזורים).
**Stack:** Fireberry CRM (eu2) · Make.com (eu2) · Grow (payments) · Tofsy (e-signatures) · Tally (forms) · GreenAPI (WhatsApp) · **n8n (פיתוח חדש)** · **CloudChat (שליחת הודעות)**.
**Ground truth:** `template_snapshot.json` holds the structural template (objects, fields, wiring). Field validation rules (mandatory/readonly/default) are NOT in it — ask Mike.

**Mike's working style:** Hebrew only, direct, no fluff, push back when he's wrong, add value beyond the literal ask. He does not read code. Default execution surface = Fireberry UI or Make (manual). Claude Code only for bulk data ops. One mission per chat.

**כלל פלטפורמה מחייב (מאושרר 03/08/2026):** פיתוח חדש = **n8n**. תחזוקת קיים = **Make, ידנית, ע"י מייק בלבד**. קלוד **לעולם** לא כותב ל-Make דרך API. לוגיקת מסך בפיירברי = client-side JS, לא n8n.

---

## 1. Business model — the shape of the thing

The business runs on a **weekly Boost cohort** that converts into premium coaching. There are **no traditional courses** — only Boost + continuous coaching. This matters: any object modeling "lessons/attendance" is dead weight here.

**עיקרון-על (chat_27):** **הבוסט אינו מוצר אמיתי — הוא שער לליווי.** הוא מנוע ההמרה של העסק. כל החלטה במודל צריכה להימדד בשאלה "האם זה משפר את ההמרה בוסט→ליווי".

### The four products (this is the spine of the whole model)

| Product | Price | Mentor | WhatsApp group | Duration | Role |
|---|---|---|---|---|---|
| **בוסט** (Boost) | one-time | — | weekly Boost group | 1 week | intro / generic menu / conversion engine |
| **פרימיום** (Premium) | per product (X weeks) | personal | mentor's group | X weeks + bonus | full 1:1 coaching |
| **מתקדמים** (Advanced) | 349 ₪/month | one fixed mentor for all | one shared group (all advanced together) | ongoing | cheap, general, group |
| **המשך** (Continuation) | 649 ₪/month | same mentor, same format | mentor's group | open-ended | 1:1 continuation of Premium |

Continuation & Advanced both require **one month advance notice** to cancel. "המשך" is a provisional name (Roital said "for now").

### מוצרי הליווי בפועל — עודכן 03/08/2026

| מוצר | GUID | מחיר לפני מע"מ | מחיר כולל | הערה |
|---|---|---|---|---|
| **תוכנית ליווי 12 שבועות** | `d9e842a7-f284-4596-bb61-4d2a350eebb5` | **3,601.69 ₪** | 4,250 ₪ | המוצר שנבחר ל-WF-17 |
| תוכנית ליווי 8 שבועות | — | — | 3,850 ₪ | ראה §1.1 ניתוח תמחור |

~~מסלול ליווי 12 חודשים~~ ⛔ מיושן (הוחלף 03/08/2026) — **המוצר הזה לא קיים בחשבון.** המודל נסגר על **12 שבועות**. כל התייחסות ל"12 חודשים" בכל מסמך היא שגויה.

### 1.1 ניתוח תמחור — החלטה עסקית, לא טכנית 🟡

חיווט אוטומטי של בוסט→**תוכנית ליווי 12 שבועות** (WF-17) **הופך את 12 שבועות למוצר ברירת המחדל של העסק.** זו לא החלטה טכנית — זו החלטה מסחרית שצריכה אישור של **רויטל**.

- 12 שבועות = **4,250 ₪** → 354 ₪ לשבוע
- 8 שבועות = **3,850 ₪** → 481 ₪ לשבוע
- **הפער: 4 שבועות נוספים תמורת 400 ₪.**

**המסקנה (chat_08):** נציג מכירות רציונלי לא ימכור 8 שבועות. המוצר של 8 שבועות גונב מכירות ממוצר רווחי יותר ובפועל הוא **מוצר מת**. אם רויטל רוצה לשמר את 8 השבועות כמוצר חי — צריך לתקן את התמחור, לא את האוטומציה.

**בעלים להכרעה: רויטל.** עד להכרעה — WF-17 מושבת בכל מקרה.

### The weekly cycle mechanics
- A Boost cohort runs **Sunday → Sunday** (7 days). **7 ימי מחזור מתוכם 5 ימי תוכן** (chat_26).
- You can register until **end of Saturday** for the cohort starting the coming Sunday. You cannot join a cohort already running.
- Therefore a cohort's **sales window = the previous week** (while the prior cohort runs), closing the day it starts. **`pcfEndSaleDate = pcfStartDate`** (chat_15).
- **קבוצת ה-WhatsApp של המחזור נפתחת ~4 שבועות לפני תחילת המכירה** של אותו מחזור (chat_15).
- Cohorts are opened **manually** by an admin (holiday/scheduling awareness), not by automation.
- ~50–60 women per cohort. **⚠️ נפח מתועד בשני טווחים:** 50–60 (chat_27) מול **50–120** (chat_23). שני הטווחים נשמרים עד מדידה בפועל. בעלים: מייק.

### ציר הזמן של המחזור — נקודות ציון

```
T-4 שבועות מתחילת המכירה → נפתחת קבוצת WhatsApp למחזור
pcfStartSaleDate         → סטטוס 6 (ממתין לפתיחה) → 1 (פתוח להרשמה)
pcfEndSaleDate = pcfStartDate → חלון המכירה נסגר; סטטוס 3 (קורס פעיל)
יום 1 (ראשון)            → תחילת המחזור
יום 3 (רביעי)            → Zoom מוקלט; ההזמנה יוצאת בבוקר אותו יום
סוף המחזור               → שאלון אבחון ב-Tally → נכתב על עסקת הפרימיום
pcfEndDate (ראשון)       → סטטוס 4 (הסתיים)
```

**תיקון תזמון הוובינר:** ~~4 ימים / ספירה מהרכישה~~ ⛔ מיושן (הוחלף 03/08/2026). התזמון הוא **3 ימים מתחילת המחזור** — לא מהרכישה. מחזור שנפתח ביום ראשון ⇒ יום 3 = **יום רביעי**, כלומר **ההזמנה יוצאת בבוקר יום הוובינר עצמו**. יש להתאים את הקופי בהתאם (chat_17).

---

## 2. The customer journey (end-to-end)

```
Lead (any source) → Make "Main Lead CRM" scenario
   → creates Account + Opportunity(Boost) + lead-source records
   → Bot (Tal) opens conversation, runs conversion
        │
   Buys Boost via bot → Grow webhook #1 fires:
   → payment card · Welcome msg (Tal) · link Boost cohort · WhatsApp group (GreenAPI)
   → opens תהליך ליווי (coaching) status "בתהליך קליטה ושיוך", program=בוסט
   → opens Premium Opportunity (clean, parent = Boost opp) — event-driven, NOT timed
        │
   Boost week (~50–60):  Wed evening recorded Zoom (Tal sends day-before + 30-min reminders)
   → end of Zoom: Tally questionnaire (linked to that week's cohort; identity by phone;
     result written onto the PREMIUM OPPORTUNITY: "filled questionnaire" + date)
        │
   Sales wave (Thu + Sun): sales reps work the Premium Opportunities
   → priority: questionnaire-fillers first.  Thu: bot reminder to non-fillers.
        │
   Closing Premium: rep sends signature form from CRM (button → webhook → Tofsy → recorded back)
   → rep fills: product (weeks) · bonus gift-weeks (1–3, rarely 4) · mentor · mentor's group
   → CRM checkout button (Grow) → Grow webhook #2:
      payment card · close opp won · link WhatsApp · UPDATE coaching → status "פעיל"(בתהליך ליווי):
      mentor, group, start+end dates (incl. bonus), customer, opp, product
        │
   Active coaching:  mentor gets alert → picks menu from catalog OR sends to dietitian
   → menu assignment (manual) → automation triggers bot to deliver the menu
```

**Dead-lead path:** whoever finishes Boost and doesn't convert → reps call again after a few days → if no success, **manually** updated to dead lead. No automation.

### 2.1 שלב 0 — מה קיים לפני התשלום (chat_22)

לפני שכסף עובר, בחשבון כבר קיימים:
1. **הליד** (לקוח, אובייקט 1).
2. **עסקת בוסט פתוחה עם מוצר משויך** — המוצר נקבע לפי **UTM**. שים לב: **העסקה נפתחת עם מוצר עוד לפני התשלום.**
3. **רישום שיווקי** (1002).

### 2.2 מפת מסלול הבוסט A→Z (מוסכם, chat_22)

| שלב | מה קורה | מצב |
|---|---|---|
| 0 | לפני התשלום: ליד + עסקת בוסט עם מוצר + רישום שיווקי | ✅ קיים |
| 1 | קליטת התשלום — וובהוק ממשולם, **זיהוי לפי טלפון** | 🔴 חסום |
| 2 | שכבת הכסף: הזמנה (13) → תשלום (1039) → תיעוד תשלום (1018) | 🔴 חסום |
| 3 | סגירת העסקה | 🔴 חסום |
| 4 | פתיחת תהליך ליווי (1051) | 🔴 חסום |
| 5 | שיוך למחזור (1007) | 🔴 חסום |
| 6 | צירוף לקבוצת WhatsApp (1068) | 🔴 חסום |
| 7 | הודעת Welcome | 🔴 חסום |
| 8 | פתיחת עסקת פרימיום | ⚠️ ראה §2.3 |
| 9 | יום 3 — הזמנה לוובינר | 🔴 חסום |

🔴 **החוסם:** הבלו-פרינט של **`Finance 3`** חוסם את המעבר לשלב 1. עד שהוא נפתר, שלבים 1–9 לא רצים.

### 2.3 ⚠️ סתירה פתוחה — עסקה אחת או שתיים?

| עמדה | מקור | תאריך |
|---|---|---|
| רכישת בוסט פותחת **עסקת פרימיום נוספת** (parent = עסקת הבוסט) ⇒ **2 תהליכי מכירה** | chat_27 · המסמך הזה, §2 ו-§6.5 | 22–23/07/2026 |
| **"תהליך מכירה, יש תמיד אחד, לא 2. זה מאוד חשוב."** — מייק | chat_08 | 27–28/07/2026 |

**⚠️ סתירה פתוחה.** ההכרעה משנה את כל ארכיטקטורת הוובהוק ואת המקום שבו נשמר השאלון (§6.6). **בעלים: מייק.** אין לבנות את ענף התשלום עד הכרעה.

---

## 3. Data model — objects & the fields that matter

### מפת קודי אובייקטים (אומתה על פני כל השיחות)

`1`=לקוח · `4`=תהליך מכירה · `6`=פגישה · `9`=משתמש · `10`=משימה · `13`=הזמנה · `14`=מוצר · `1002`=רישום שיווקי · `1005`=הרשמה לקורס ⚠️ · `1007`=מחזור בוסט · `1018`=תיעוד תשלום · `1030`=הרשמה לאירוע · `1032`=אירוע · `1036`=הגדרות · `1039`=תשלום · `1041`=מפגש · `1049`=הגעה למפגש · `1051`=תהליך ליווי · `1057`=חג ומועד · `1059`=הקצאת תפריט · `1060`=קטלוג תפריט · `1068`=קבוצת WhatsApp · `1069`=טופס שקילה.

### מחזור קורס / Boost cohort — `customobject1007` (type_code 1007)
The central Boost entity. Originally a generic "course cycle"; now exclusively Boost (no other courses exist in the business, confirmed by Mike).

**מודל הבוסט = `1007` בלבד (chat_26).** `1032` (אירוע) + `1030` (הרשמה לאירוע) הם **הוובינר** — לא מודל מתחרה. כל שריד לטענת "שני מודלים מתחרים" נמחק.

Key fields:
- `pcfStartDate` / `pcfEndDate` — Boost start/end (Sunday/Sunday).
- `pcfStartSaleDate` / `pcfEndSaleDate` — sales window = the previous week. `pcfEndSaleDate` = the cohort's own start day.
- `pcfStatus` — picklist. **1**=פתוח להרשמה · **3**=קורס פעיל · **4**=הסתיים · **5**=התבטל · **6**=ממתין לפתיחה.
- `pcfRegistration` — **roll-up**: counts linked records. Verified natively working in the template. This is how "how many registered" is answered.
- `pcfRegistrationQuota` — quota (set to 60 across all imported cohorts).
- `pcfRegistrationAvailability` — available (quota − registered).
- `pcfEventLink` — relabeled to **"לינק לקבוצת וואטסאפ"**. Underlying url field unchanged. ⚠️ ראה §8 — גורלו שנוי במחלוקת.
- `pcfProductId` — lookup → Product (type_code 14). Default value = the Boost product.
- **אחראי מחזור** (`ownerid`) · **קבוצת WhatsApp מקושרת** (lookup → 1068).

**אינווריאנט (chat_07): לכל מחזור חייבת להיות קבוצת WhatsApp מקושרת.** סטטוס "פתוח להרשמה" = ניתן לשייך אליו לקוחות.

Fields REMOVED from the Boost layout (Boost has no scheduled meetings): צורת העברת הקורס, מספר מפגשים, פירוט מועדים, הצעת מחיר, כתובת הקורס, לינק Waze.

#### מודל 4 החלונות — סטטוס המחזור (chat_21)

| סטטוס | ערך | חלון זמן | משמעות |
|---|---|---|---|
| ממתין לפתיחה | `6` | לפני `pcfStartSaleDate` | קיים, לא ניתן להרשמה |
| פתוח להרשמה | `1` | עד `pcfEndSaleDate` | ניתן לשייך לקוחות |
| קורס פעיל | `3` | עד `pcfEndDate` | רץ, סגור להרשמה |
| הסתיים | `4` | אחרי `pcfEndDate` | ארכיון |
| התבטל | `5` | — | **חסין** — אף אוטומציה לא נוגעת בו |

**אינווריאנט מבני:** מחזורים שבועיים ראשון→ראשון, וחלון המכירה של מחזור N+1 נפתח ביום שמחזור N מתחיל ⇒ **בכל רגע נתון קיים בדיוק מחזור אחד "פתוח להרשמה" ובדיוק אחד "קורס פעיל".**
**בדיקת בריאות:** שאילתה שסופרת מחזורים בסטטוס 1 ובסטטוס 3. תוצאה ≠ 1 בכל אחד מהם = תקלה.

#### ⚠️ סתירה פתוחה — כמה מחזורי בוסט קיימים?

| עמדה | מקור | תאריך |
|---|---|---|
| **74 מחזורים אומתו חי** — כולם מסתיימים ביום ראשון | אימות מול החשבון החי | **02/08/2026** |
| ~~22 מחזורים יובאו (2.8.2026 → סוף השנה)~~ ⛔ מיושן (הוחלף 03/08/2026) | §7 של מסמך זה | 07/2026 |

**⚠️ סתירה פתוחה.** ההפרש (52 מחזורים) אינו מוסבר — ייתכן ייבוא נוסף שלא תועד, ייתכנו כפילויות. **בעלים: מייק.** כל חישוב קיבולת/סיכון "המחזורים ייגמרו" תלוי בהכרעה הזו.

🐛 **באג דאטה לתיקון ידני:** מחזור **"בוסט · אוגוסט 02"** נושא **תאריך התחלה 09.08** — כפילות של **"בוסט · אוגוסט 09"** שמסומן **"התבטל"**. כל עוד זה כך, מחזור 02.08 **אינו מתפקד**. תיקון ידני, בעלים: מייק.

🔴 **חוסם דאטה:** מתוך 22 המחזורים שתועדו, **רק לאחד** ("בוסט · אוגוסט 09") יש `pcfEventLink` מלא. תאריך תחילת הבוסט והלינק לקבוצה מגיעים לפיילוד **רק אם** מולא `pcfBoostLinked` על תהליך הליווי ⇒ **תרחיש התשלום שיוצר את הליווי חייב לקשר את המחזור ברגע היצירה.** סעיף חוזה — לוודא כשהתרחיש ישוחרר.

🟡 **סיכון מובנה:** מחזורים קיימים ואיש לא הגדיר עד מתי הם נמשכים. כשטבלת התאריכים תיגמר — **המערכת תיעצר בשקט**, בלי שגיאה. **בעלים: עודד.**

### הרשמה לקורס / Boost registration — `customobject1005`
🔴 **⚠️ סתירה פתוחה — חוסם. הקפא כל בנייה שנשענת על `1005`.**

| עמדה | מקור | תאריך |
|---|---|---|
| **`1005` הוא אובייקט ההרשמה לבוסט** (ולא 1030); הוא מנוטרל ו**צריך הפעלה**; לכל נרשמת נוצרת רשומת 1005; N6/N9 כותבים אליו | chat_20 | 26/07/2026 18:23–19:15Z |
| מייק נשאל על 1005 וענה **"תשאיר מחזור בוסט"** — **תשובה דו-משמעית**; 1005 נשאר מחוץ להכרעה | chat_25 | 07/2026 |
| ~~**`1005` הופל**~~ לטובת **one-to-many** — המחזור מקושר ישירות על רשומת הליווי | chat_27 | 22–23/07/2026 |

**בנוסף:** יש מסמכים שטוענים שאובייקט ההרשמה הוא **`1030`** — טענה שלישית שסותרת את שתי הראשונות. `1030` ו-`1032` **ריקים לחלוטין** בחשבון החי, ולפי chat_26 הם שייכים ל**וובינר** ולא למודל הבוסט.

**תוצאה נגזרת:** `4.pcfBoostLinked` הוא **lookup ל-`1005`** ⇒ הוא **שדה זומבי** כל עוד 1005 מנוטרל.

**🔴 החלטה תפעולית: כל בנייה שנשענת על `1005` — מוקפאת עד הכרעה חד-משמעית של מייק.** אין להסתמך על אף אחת משלוש העמדות. **בעלים: מייק.**

Its layout was earlier relabeled ("הרשמות לבוסט", `pcfEventId` → "מחזור בוסט - מקושר", removed `pcfAmountMeetings`).

### מפגש (1041) + הגעה למפגש קורס (1049)
**Out of scope for Boost** — no scheduled meetings exist. Not deleted (other flows might use them someday), just excluded.

### אירוע (1032) + הרשמה לאירוע (1030) — הוובינר
- שני האובייקטים **ריקים לחלוטין** בחשבון החי.
- **אין lookup בין 1032 ל-1007.** מנגנון הקישור: **`1032.pcfExternalSoftwareID1` = מזהה המחזור (1007)**.
- הם מייצגים את **הוובינר**, לא את המחזור. אינם מודל מתחרה ל-1007.

### תהליך ליווי / Coaching process — `customobject1051` (type_code 1051)
The customer's lifelong "medical file." **ONE record per customer for the entire journey** — never duplicated, only updated. Boost → Premium → Advanced → Continuation all live on the same record.

**עיקרון מבני מרכזי (chat_07 · chat_22):** **`1051` = "תיק רפואי" מתמשך.** רשומה אחת פר-לקוחה לכל החיים. בוסט→מסלול→ריטיינר זו **אותה רשומה** — משתנים רק הסטטוס והתוכנית. מעבר בוסט→פרימיום הוא **עדכון `pcfCurrentProgram`**, לא פתיחת תיק חדש.

**שני צירים נפרדים — חייב להיות מוסבר למנטורית:**
`pcfStatus` (סטטוס ליווי = **איפה במסע**) ≠ `pcfCurrentProgram` (תוכנית נוכחית = **מה עושה עכשיו**).

Key fields:
- `pcfStatus` — **סטטוס ליווי** (axis B: the *state*). picklist: **1**=בתהליך קליטה ושיוך · **2**=בתהליך ליווי (active) · **3**=ליווי הסתיים בהצלחה · **4**=בהקפאה · **5**=בתהליך ביטול · **6**=ליווי בוטל (churn) · **7**=בהודעת סיום · **8**=סיום בוסט — לא המירה.
- **סטטוס מוצר / "תוכנית נוכחית"** (axis A) — system name was auto `pcfsystemfield102`; **recommend renaming to `pcfCurrentProgram`**. Values: **1**=בוסט · **2**=פרימיום · **3**=מתקדמים · **4**=המשך.
- `pcfProduct` — lookup → Product.
- `pcfparentprocess` — self-lookup ("שם ליווי (אב)").
- `pcfBoostLinked` / **מחזור בוסט מקושר** — lookup to the cohort. זה מה ש-`pcfRegistration` סופר.
- `pcfWeeksGift` — שבועות מתנה. **מקור הערך: נציג המכירות, לפני שליחה לחתימה. ברירת מחדל 0.** ⚠️ לאישור עסקי — ראה §8.
- Plus: mentor lookup, WhatsApp group, start date, end date (Make-computed), notice date, weight data, menu.

### קבוצת WhatsApp — `customobject1068`
- **חיבור `1007` ↔ `1068`** קיים כ-lookup.
- בעת הצירוף לקבוצה נכתבים אוטומטית **`4.pcfCourse`** ו-**`1051.pcfBoostLinked`**.
- ⚠️ **`pcfGroupid` מול `pcfGreenApiId`** — סתירה פתוחה. chat_20: `pcfGreenApiId` קנוני (אישור מייק). chat_22: מייק אמר "לא יודע, צריך לבדוק". **בדיקת אימות בת 5 דקות:** לפתוח 2–3 מתוך 8 רשומות 1068 ולראות איפה יושב הפורמט `1203630xxxxx@g.us`. **בעלים: מייק.**

### תפריטים — `pcfMenuType` (קטלוג 1060 / הקצאה 1059)
⚠️ **`pcfMenuType` מכיל שני ערכים בלבד: סטנדרטי / אישי.** **שלושת תפריטי הבוסט ממופים לערך "סטנדרטי".**
⇒ **במישור התפריטים, בוסט אינו מסלול נפרד.** אם מסמך כלשהו מתייחס לבוסט כמסלול תפריטים עצמאי — הוא שגוי.
**ההכרעה הנדרשת:** או להוסיף ערך "בוסט" ל-`pcfMenuType`, או לקבע רשמית שבוסט = סטנדרטי. **בעלים: מייק.**

### Native objects
- **Account** (customer), **Opportunity** (sales, type_code 4), **Product** (type_code 14). ⚠️ מספר העסקאות ללקוחה — ראה §2.3.
- `4.pcfCourse` — lookup → מחזור בוסט (1007). **זהו שדה המקור של WF-17.**

### טבלת קטגוריה → מסלול → חובת חתימה

| `categorycode` | קטגוריה | מסלול | חובת חתימה |
|---|---|---|---|
| 101 | תוכנית ליווי | פרימיום | ✅ נדרשת |
| 102 | תוכנית המשך | המשך / ריטיינר | **❓ פתוח להכרעה** |
| — | — | בוסט | ❌ לא נדרשת |
| — | — | מתקדמים / ריטיינר | ❌ לא נדרשת |

**מקור ההנחה:** האפיון. ההנחה **מקודדת בתוך כפתור התשלום הידני** — כלומר אם המודל העסקי משתנה, **הלוגיקה בכפתור חייבת להשתנות איתו.** בעלים להכרעת 102: מייק.

---

## 4. Coaching status model — the two-axis design (Decision #4)

Do NOT collapse everything into one giant status field. **Two orthogonal axes:**
- **Axis A — סטטוס מוצר / current program:** WHICH product (בוסט/פרימיום/מתקדמים/המשך).
- **Axis B — סטטוס ליווי:** WHAT state within it (active/frozen/notice/ended/churn/…).

**Why:** clean reporting. "How many active customers" = status=active (across all products, one query). "How many in Advanced" = program=Advanced. A single-field model would fracture "active" into 4 values.

**Critical rule — program change ≠ status change.** When a customer moves Premium→Advanced, only *program* changes; *status* stays "בתהליך ליווי" (active). "הסתיים" is reserved for **final exit**. Mike confirmed.

**רילייבל "מחזור בוסט" → "מחזור" — לא הוכרע ולא בוצע.** הוא גורר 5 תוויות: `1007.pcfStartDate`, `1007.pcfEndDate`, `4.pcfCourse`, `1051.pcfBoostLinked`, `1049.pcfRelatedCourse`.
**הבחנה חשובה:** `pcfCurrentProgram` ערך **1 = "בוסט"** ו-`pcfStatus` ערך **8** נשארים כמו שהם — שם **המוצר** הוא "בוסט" גם אם שם **המחזור** ישתנה. אל תערבב בין השניים.

### End-date logic
- Premium: start + (product weeks + **bonus** gift-weeks). Bonus affects **end date only**, never price. No discounts exist — bonus weeks are the only lever for hard-to-close deals.
- Freeze: end date pushed by the freeze duration.
- Advanced/Continuation: **no end date** until a cancellation notice → then end = notice date + 30 days.
- End date is **computed in Make**, not a Fireberry formula.

### 4.1 נקודת יציאה לא מנוצלת — `pcfStatus = 8`

`1051.pcfStatus = 8` ("סיום בוסט — לא המירה") הוא **נכס עסקי לא מנוצל**:
- **50–120 נשים בשבוע** נופלות לשם.
- **אפס אוטומציה. אפס רימרקטינג.**
- היציאה היחידה בפועל היא ידנית: "ליד מת".

זו נקודת ההשקה עם ההכנסה הגבוהה ביותר בעסק שאיש לא נוגע בה. **לפתיחה מול רויטל.**

---

## 5. The Grow payment webhook — architecture

**⚠️ סטטוס 03/08/2026: מוקפא.** תרחיש התשלום של הבוסט (משולם) **טרם נבנה / בהקפאה — אשכול A, תקלה במשולם.** כל מה שכתוב כאן הוא מפרט, לא מציאות.

### 5.1 שרשרת התלויות — קרא לפני שאתה מאשים workflow בתקלה

```
תרחיש התשלום של הבוסט (מוקפא)
   └─ יוצר רשומת ליווי 1051 עם pcfBoostLinked + pcfCurrentProgram = 1
        ├─ מעדכן ל-pcfCurrentProgram = 2 בהמרה
        ├─ WF-16 (מסלול מת) יושב במורד הזרם ⇒ בלעדיו מחזיר אפס
        └─ WF-17 (מכירת ליווי אחרי בוסט) יושב במורד הזרם ⇒ בלעדיו מחזיר אפס
```

**⇒ "ה-workflow מחזיר אפס" אינו באג כל עוד תרחיש התשלום מוקפא.** ראה §9.

The heart of the system. **One Make scenario, a Router branches by product.** Do not build four scenarios — shared actions written once.

**Anchor / identification:** **by customer phone number** (final decision — Boost is bought via the bot, so it has no `opportunity_id` to inject).

**Shared actions (all products):** create payment card w/ billing data → link to customer & opp → close opportunity won.

**Branches:**
- **Boost:** create coaching record (program=בוסט, status=קליטה ושיוך) · link active cohort onto the coaching record · WhatsApp Boost group · Welcome (bot) · open Premium Opportunity ⚠️ (ראה §2.3 — סתירה פתוחה).
- **Premium:** update coaching program=פרימיום · write mentor + mentor's group · start date · **end date = start + weeks + bonus (Make-computed)** · link product+opp · WhatsApp mentor group · status→בתהליך ליווי · **alert mentor**.
- **Advanced (349):** program=מתקדמים · **auto-fill the one fixed mentor** · shared Advanced group · **no end date** · recurring monthly billing (`recurringDebitId`).
- **Continuation (649):** program=המשך · **mentor & group unchanged** · no end date · recurring billing.

**Grow gotchas (critical):**
- `approveTransaction`: **mandatory** for regular payments (Boost, Premium); **forbidden** for token/J4J5 (Advanced, Continuation).
- All requests `multipart/form-data`, **never JSON**.
- Payment links expire in 10 minutes.
- Server-side only — button passes IDs, Make makes the calls.
- Recurring = token model (`recurringDebitId`).

**Impact map:** one webhook touches 6 objects + 2 external systems (GreenAPI, Tal's bot).

### 5.2 שיוך לקבוצה — תוקן 03/08/2026

~~השיוך לקבוצה מתבצע אחרי התשלום, ע"י הנציג~~ ⛔ מיושן (הוחלף 03/08/2026).

**המודל הנכון:**
1. **הנציג בוחר את הקבוצה *לפני* התשלום** — כחלק ממילוי פרטי העסקה (מוצר · שבועות מתנה · מנטורית · קבוצה).
2. **השיוך בפועל נורה אוטומטית ברגע התשלום** — לא לפניו ולא ידנית אחריו.
3. **קבוצה ↔ מנטורית = יחס 1:1.** לכל מנטורית קבוצה אחת, לכל קבוצה מנטורית אחת.
4. **אין שום קשר בין אורך המסלול לבין הקבוצה.** לקוחת 8 שבועות ולקוחת 12 שבועות יכולות לשבת באותה קבוצה.

**כל טקסט בכל מסמך שמתאר שיוך לקבוצה *אחרי* התשלום — שגוי.**

---

## 6. Key architectural decisions (with rationale) — READ THIS SECTION

1. **No courses exist — only Boost + coaching.** מפגש/הגעה למפגש excluded. Confirmed by Mike.
2. ~~**Dropped הרשמה לבוסט (registration junction)** — one-to-many chosen over many-to-many.~~ ⛔ **מיושן / שנוי במחלוקת (03/08/2026).** ⚠️ סתירה פתוחה — ראה §3, אובייקט `1005`. **הקפא כל בנייה שנשענת עליו.** בעלים: מייק.
3. **One coaching record per journey** ("medical file"). Never duplicated across program transitions — only updated.
4. **Two-axis status** (§4).
5. **Premium Opportunity opens event-driven** at Boost purchase, NOT on a Wednesday timer. ⚠️ **סתירה פתוחה** — ראה §2.3 (מייק: "תמיד אחד, לא 2").
6. **Questionnaire lives on the Premium Opportunity, not on coaching.** Rationale: sales reps must work in one place and must NOT enter the coaching process to complete a sale. ⚠️ תלוי בהכרעת §2.3.
7. **Opportunity identification by phone number** (final).
8. **Bonus affects end date only, never price. No discounts.**
9. **Cohort linked on BOTH sales & coaching, counted on coaching.** The roll-up counts the **coaching** side only.
10. **"ממתין לפתיחה" cohort status + daily open automation.** Internal Fireberry scheduled automation runs **daily 00:01**: if status=ממתין לפתיחה AND `pcfStartSaleDate ≤ today` AND `pcfStartDate > today` → status=פתוח להרשמה. Uses `≤` so a missed run self-heals.
    **עדכון 03/08/2026:** האוטומציה הפנימית הזו **מיועדת לכיבוי** לטובת workflow ב-n8n (עקבי עם כלל "פיתוח חדש = n8n"). לא לכבות לפני שה-workflow חי ונבדק.
11. **פיתוח חדש = n8n · תחזוקת קיים = Make ידנית ע"י מייק · קלוד לעולם לא כותב ל-Make דרך API.**
12. **קונבנציות n8n מחייבות:** בלוק `Config` · דגל `DRY_RUN` · מטפל שגיאות `WF16ErrHandler01` · קרדנציאל `Revital Yaish new CRM`.
13. **פרוטוקול הרצה ראשונה בחשבון חי:** `DRY_RUN=true` כברירת מחדל · תקרת `MAX_PER_RUN` · אם רשימת ה-DRY-RUN ארוכה מהתקרה **לא הופכים ל-false** עד הכרעת מייק · **בדיקת שלילה חובה** (לקוחה שכן קנתה לא מופיעה בדוח).
14. **מחיקות ע"י סוכן אוטונומי אסורות לחלוטין.** מחיקה ידנית בלבד, אחרי אישור פר-שדה.

---

## 7. WF-17 — מכירת ליווי לאחר בוסט (חדש, 03/08/2026)

**זרימת ההמרה בוסט→ליווי קיימת עכשיו כ-workflow.**

| מאפיין | ערך |
|---|---|
| מזהה n8n | **`e30cNECSoBNJDQcf`** |
| צמתים | **19** |
| מצב | **מושבת** (disabled) |
| דגל | **`DRY_RUN = true`** |
| טריגר | **יום רביעי 20:00, Asia/Jerusalem** |

### לוגיקה

1. **מחזור היעד:** `1007.pcfEndDate` = **יום ראשון הקרוב** (היום + 4).
2. **פילטר המקור: תהליך מכירה (אובייקט `4`) לפי `pcfCourse`** — **לא** דרך תהליך הליווי. זו נקודה קריטית: המקור הוא צד המכירות, לא צד הליווי.
3. **הוכחת רכישת בוסט: סטטוס `"עסקה נסגרה בהצלחה"`.** בלי זה אין המרה.
4. **פסילה:** כל לקוחה שיש לה רשומת ליווי **שאינה בוסט** — נפסלת (היא כבר בליווי).
5. **המוצר הנמכר:** **תוכנית ליווי 12 שבועות** · GUID `d9e842a7-f284-4596-bb61-4d2a350eebb5` · **3,601.69 ₪ לפני מע"מ**.
6. **בעלות:** אותו **`ownerid`** של עסקת הבוסט — הנציג שמכר את הבוסט מקבל את ההמשך.
7. **מעקב:** **יום חמישי 10:00** נכתב לתוך **`pcfFollowUpTime`**.
8. **שם התהליך:** **`מכירת ליווי לאחר בוסט - {שם לקוחה}`**.
9. **אב:** **`pcfParentSale`** = מזהה עסקת הבוסט.

### הגנת כפילות — קרא לפני שאתה משנה משהו

תהליך המכירה הבן **נושא את אותו `pcfCourse`** של האב. לכן **אי אפשר** לזהות כפילות לפי `pcfCourse`.
**הזיהוי מתבצע דרך `pcfParentSale`** — אם כבר קיים תהליך בן שה-`pcfParentSale` שלו הוא עסקת הבוסט הזו, לא נוצר עוד אחד.
**אל תחליף את מנגנון הזיהוי הזה בלי להבין את ההשלכה.**

### WF-16 (מסלול מת) — עודכן לעקביות

**לקוחה שיש לה תהליך מכירה פתוח שמצביע על עסקת בוסט — כבר לא מסומנת "לא המירה".**
בלי התיקון הזה WF-17 היה פותח לה תהליך מכירה ו-WF-16 היה מסמן אותה כמתה באותו שבוע. שני ה-workflows חייבים להישאר מסונכרנים — **שינוי באחד מחייב בדיקה בשני.**

---

## 8. Open items

- 🔴 **`1005` — הכרעה חד-משמעית של מייק.** חוסם. כל בנייה שנשענת עליו מוקפאת. (§3)
- 🔴 **עסקה אחת או שתיים?** מייק. חוסם את ארכיטקטורת הוובהוק. (§2.3)
- 🔴 **74 מול 22 מחזורים** — מייק. (§3)
- 🔴 **תרחיש התשלום של הבוסט מוקפא** (משולם, אשכול A) — חוסם שלבים 1–9 במפת המסלול. בלו-פרינט `Finance 3`.
- 🔴 **525 אירועים תקועים בתורי Make** — **אסור להדליק תרחיש כלשהו לפני בדיקת תוכן התור שלו.** הדלקה עיוורת תשפוך מאות רשומות למערכת.
- 🟡 **מחיר/ברירת מחדל 12 שבועות** — החלטה מסחרית של **רויטל**. (§1.1)
- 🟡 **`pcfMenuType`** — להוסיף ערך "בוסט" או לקבע שבוסט = סטנדרטי. מייק. (§3)
- 🟡 **`categorycode` 102 — חובת חתימה?** מייק. (§3)
- 🟡 **`pcfGroupid` מול `pcfGreenApiId` ב-1068** — בדיקת 5 דקות. מייק. (§3)
- 🟡 **גורל `1007.pcfEventLink`** — chat_20 סוגר כ"לא רלוונטי" אחרי המעבר ל-1068; chat_21 משאיר פתוח; chat_22 מונה כחוסם פעיל בבעלות **עודד**. **המלצה: לסגור** — מקור האמת עבר ל-`1068.pcfGroupLink`.
- 🟡 **רילייבל "מחזור בוסט" → "מחזור"** — לא הוכרע. גורר 5 תוויות. (§4)
- 🟡 **`pcfWeeksGift`** — לאשש: מקור = נציג המכירות לפני שליחה לחתימה, ברירת מחדל 0. אישור עסקי נדרש.
- 🐛 **מחזור "בוסט · אוגוסט 02" עם תאריך 09.08** — תיקון ידני. מייק.
- 🐛 **עסקת מיכאל אוקס** — יש `pcfFormLink` אך מסומנת שלא מולא שאלון. כלל: **לינק גובר על תווית.**
- **Re-marketing after "הסתיים" / `pcfStatus=8`** — pending Roital. (§4.1)
- **Rename** `pcfsystemfield102` → `pcfCurrentProgram`.
- **סיכון "המחזורים ייגמרו"** — עודד.

### Closed
Tofsy · dead-lead path (manual) · identification (phone) · Advanced mentor (one fixed, auto-filled) · `pcfRegistration` roll-up native · **WF-17 נבנה** (§7) · **מודל השיוך לקבוצה** (§5.2).

---

## 9. מצב הדאטה החי — 02/08/2026

**קרא את זה לפני שאתה מדווח על תקלה.**

| מדד | ערך |
|---|---|
| תהליכי מכירה בחשבון (אובייקט 4) | **176** |
| מתוכם בסטטוס **"ליד חדש"** | **175** |
| מתוכם משויכים למחזור בוסט (`pcfCourse`) | **2** |
| עסקאות בסטטוס **"עסקה נסגרה בהצלחה"** | **0** |

**⇒ WF-17 מחזיר אפס תוצאות היום. זו התנהגות תקינה, לא תקלה.** אין בחשבון אף עסקת בוסט סגורה, ולכן אין ממה להמיר. WF-17 יתחיל להחזיר תוצאות רק כשענף התשלום יעלה ויתחיל לסגור עסקאות.

🔴 **סיכון לרישום — קרא לפני כל מילוי רטרואקטיבי:**
**מי שימלא `pcfCourse` על תהליכי המכירה הקיימים ללא פילטר תשלום — יפתח 175 תהליכי מכירה בבת אחת.**
כל מילוי רטרואקטיבי חייב להיות מותנה בסטטוס תשלום, ולרוץ קודם ב-`DRY_RUN=true` עם תקרת `MAX_PER_RUN`.

**מצב החשבון החי:** נכון ל-26/07/2026 החשבון היה ב-**clean state תפעולי** למעט שני שינויים מ-22–23/07 (עדכון `pcfPowerlinkToken` ב-1036 ותיקון קריטריון חיפוש ב-Make). כל מי שממשיך — מתחיל משם.

---

## 10. סודות לרוטציה — 🔴 חמישה מפתחות

**⚠️ ערכי מפתחות לעולם לא נרשמים במסמך הזה ולא באף מסמך אחר.**

| # | מפתח | מצב |
|---|---|---|
| 1 | Fireberry `tokenid` | **⚠️ נחשף בצ'אט — לרוטציה** |
| 2 | Make API key | **⚠️ נחשף בצ'אט — לרוטציה** (גישה מלאה לחשבון ולכל הקונקשנים מאחוריו) |
| 3 | Tofsy `api_key` | **⚠️ נחשף בצ'אט — לרוטציה** |
| 4 | GreenAPI `apiTokenInstance` | **⚠️ נחשף בצ'אט — לרוטציה** |
| 5 | CloudChat API key | **⚠️ נחשף בצ'אט — לרוטציה** |
| — | `1036.pcfPowerlinkToken` | **⚠️ נחשף בצ'אט — לרוטציה** |

**אף רוטציה לא אומתה כבוצעה.** כל מסמך שכתוב בו "3 טוקנים" — שגוי, המספר הוא **5**.

**⚠️ תזמון — לא עכשיו.** רוטציה שוברת את כל חיבורי Make עד לעדכונם. אם טל בונה במקביל, דברים ייפלו לו בלי שיבין למה. **הוכרע: רוטציה רק אחרי סיום הטסטים**, בחלון מתואם. לא "ניצחון מהיר".

**צ'קליסט תלת-שלבי אחרי הרוטציה:**
1. החיבורים ב-Make ("Revital - New").
2. ה-credential ב-n8n (`Fireberry — tokenid`, Header Auth).
3. השדה `pcfPowerlinkToken` ב-1036.

**נכסים מזוהמים:** `Meetings_Reminders_FIXED_blueprint.json` (הטוקן מוטמע במודולים 1 ו-6) · בלו-פרינט מודול 93 (CloudChat) · קוד טופס הליד.
**כלל אבטחה קשיח:** אם ייבחר GreenAPI ישיר כערוץ שליחה — הטוקן נכנס ל-URL של הצומת ⇒ נכנס ל-export של ה-workflow ⇒ **אסור לשלוח את ה-JSON בצ'אט או בוואטסאפ.**
**דפוס תקין לחיקוי:** בכפתור התשלום הידני **לא נחשף שום טוקן** — כל הקריאות עוברות דרך `/api/record/...` בסשן של המשתמש המחובר. **זה התקן לכל כפתור/ווידג'ט עתידי בפיירברי.**

---

## 11. What earlier chats changed (the diff)

- Boost cohort (1007): relabeled link → WhatsApp, removed 6 meeting-era fields, added status "ממתין לפתיחה" (6).
- Registration (1005): relabeled, then dropped from flow ⚠️ **שנוי במחלוקת** — §3.
- מפגש/הגעה: excluded from Boost.
- Coaching (1051): added program axis (`pcfCurrentProgram`, 4 values), added status 7 & 8, confirmed one-record model, cohort link added on coaching.
- Verified `pcfRegistration` roll-up is native.
- Defined the full customer journey + Tal's 7 bot touchpoints.
- Defined the 4-product coaching lifecycle + state machine.
- Specced the Grow payment webhook (one scenario, phone-anchored, 4 branches).
- ~~**Imported 22 Boost cohorts**~~ ⛔ מיושן (הוחלף 03/08/2026) — **74 מחזורים אומתו חי ב-02/08/2026.** ⚠️ סתירה פתוחה, §3. Import gotcha learned: use **real Excel date cells**, not text.
- **03/08/2026:** נבנה **WF-17** (§7) · עודכן **WF-16** · תוקן מודל השיוך לקבוצה (§5.2) · תועד מצב הדאטה החי (§9) · תועד מרשם הרוטציה (§10).

---

## 12. Cross-project gotchas & learnings (carry forward)

- **Fireberry query:** `POST api.fireberry.com/api/query`, `tokenid` header. Results array named `Data`. Always explicit field names, never wildcards.
  ⚠️ **סתירה פתוחה:** `POST /api/v3/query` (chat_20, החלטה למעבר) מול `POST /api/query` (chat_21, legacy). **הוכרע עקרונית: כל workflow חדש עובר ל-v3**, מותנה באימות בחשבון החי. שני הנתיבים מתועדים עד אימות.
- ⚠️ **Rate limit — שתי מגבלות נפרדות:** 100 בקשות/דקה לארגון (chat_20, chat_21) · צינון 10–15 דקות אחרי ~350 קריאות מטא-דאטה (chat_26). לא סותרות — מגבלות שונות.
- **Fireberry formulas:** number-output OK; **date-output formulas fail** → compute dates in Make/n8n. `FLOOR` unavailable → set field precision 0. Formula-on-formula references don't work → inline.
- **Fireberry picklist:** each option is `value` (int) + `label`. No per-option "system name".
- **Roll-up counting linked records IS supported natively.** Verified on `pcfRegistration`.
- **Max 50 internal Fireberry automations** — complex logic runs in Make/n8n.
- **Tofsy:** `form_id` from builder URL = API `_id`. `/create` needs TWO_STEP forms. Webhook returns hidden fields by field id. `opportunity_id` is the anchor pattern.
- **Excel import to Fireberry:** always real date cells; watch DD/MM vs MM/DD.
- **Never delete fields/objects without per-item Mike confirmation.** Uncertain items → "לא בשימוש".
- **n8n:** `n8n import:workflow` **לא מייבא credentials** — חיבור ה-credential ידני בממשק, תמיד.
- **קונקטור ClickUp נכשל שוב ושוב** (`clickup_get_task` → "No approval received"; timeouts). עקיפה: `getTaskById` ישיר, או הדבקת תוכן המשימה ע"י מייק.
- **GreenAPI = ניהול קבוצות בלבד · CloudChat = שליחת הודעות ללקוחות.** שני שימושים שונים לחלוטין.
- ⚠️ **לפני שמסתמכים על "אישור" שניתן בצ'אט — לוודא מי בעל/ת הצ'אט.** לפחות שיחה אחת בפרויקט נוהלה ע"י גורם שאינו מייק.

---

## 13. Deliverables produced (earlier chats)

| File | Purpose |
|---|---|
| `roital_customer_flow.html` | Full visual customer-flow diagram + Tal's 7 bot touchpoints |
| `תהליך_ליווי_רויטל_אפיון.md` | Coaching model (⚠️ predates dropping registration; this HANDOFF supersedes) |
| `וובהוק_תשלום_Grow_מפרט.md` | Grow webhook spec (⚠️ predates registration drop) |
| `מחזורי_בוסט_לייבוא_v4.xlsx` | 22 Boost cohorts ⚠️ **74 אומתו חי — ראה §3** |

> If discrepancies arise between the older .md deliverables and this HANDOFF, **this HANDOFF wins**.
> **אם סעיף מסומן ⚠️ סתירה פתוחה — אף צד לא "מנצח". אין לבנות עליו עד הכרעת הבעלים הנקוב.**
