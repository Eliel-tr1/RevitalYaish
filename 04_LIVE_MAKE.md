# 04 · מצב חי — Make.com

> **עודכן 03/08/2026 — סקירת 26 שיחות הפרויקט.**

## יומן שינויים (03/08/2026)

| # | מה שונה | מקור |
|---:|---|---|
| 1 | נוסף כלל הפרויקט המחייב לגבי Make מול n8n, בניסוח verbatim | chat_20, chat_21, chat_26, chat_27 |
| 2 | נוספה טבלת **"מה רץ איפה בפועל"** — Make / n8n / JS בצד לקוח, עם סטטוס לכל צינור | chat_08, chat_10, chat_12, chat_21 |
| 3 | נוסף כרטיס מלא ל-`Main Leads CRM - Revital Yaeish N v1.02` (מבנה, טריגר, ריצה אחרונה) | chat_05 |
| 4 | נוספה **⚠️ סתירה פתוחה** על מזהה התרחיש: 9339860 מול 6600296 (1452508 = תרחיש פנימי אחר) | chat_04, chat_05 |
| 5 | נוספה רשימת **5 הבאגים המאומתים** ב-`Main Leads CRM` + טבלת תיקונים פר-מודול | chat_04 |
| 6 | נוסף `pcfPage` כנקודת כשל יחידה החוזרת ב-5 מודולים (25/37/41/46/49) | chat_04 |
| 7 | נוסף `pcfRegistrationForm` picklist — **באג שנפתר** ע"י אליאל (ערך "טופס חדש" = 5) | chat_04 |
| 8 | נוסף: **דף הנחיתה לא ממפה UTM** — 6 מתוך 8 ענפי UTM לא רצים; התיקון בצד ה-LP | chat_04 |
| 9 | נוספה שרשרת ה-`productid`: מודולים 54→69→153/157→37 | chat_05 |
| 10 | נוסף ראוטר `148` ושני הפילטרים `opportunity_record` / `marketing_record` + באג "ריק = yes" | chat_22 |
| 11 | נוספה מפת עד 11 האובייקטים שהתרחיש יוצר, כולל ההבחנה "תמיד" מול "רק אם לא קיים" | chat_22 |
| 12 | נוסף חוזה `WebhookRespond` כולל שגיאת הכתיב המכוונת `oppurtunity_id` | chat_22 |
| 13 | נוסף פירוק `New payment - CloudChat (1.01)` + מודול 93 (נרמול דו-לשוני) + באג מודול 142 | chat_22 |
| 14 | נוספה שרשרת התשלום המלאה עד `Finance 3`, עם סימון הבלו-פרינט החסר כחסם | chat_22, chat_27 |
| 15 | נוסף פירוק `Signed Document from Tofsy` (4 מודולים) + הגדרות retry/DLQ | chat_27 |
| 16 | נוסף תרחיש `Meetings Reminders` (13 מודולים) + 6 התיקונים + חוב טכני | chat_10 |
| 17 | נוסף תרחיש `weekly_guest_broadcast` (10 מודולים) + באג ה-Iterator `data.data` | chat_19 |
| 18 | נוסף חוזה ה-params בתרחיש ה-Welcome (params 1–4 בלבד; 5–10 שאריות) | chat_19 |
| 19 | ~~סנריו שליחת מסמך = 4 Query + בורר SMS/Email/WhatsApp~~ ⛔ מיושן — צומצם ל-Query אחד וערוץ וואטסאפ קבוע | chat_09 |
| 20 | ~~`Boost Cohort — Daily Status Sync` כתרחיש Make~~ ⛔ מיושן — עבר ל-n8n; נשמר כנספח "חלופת Make" | chat_21 |
| 21 | `Webinar Reminders (New CRM)` (27 מודולים, מעולם לא רץ) סומן **deprecated** — נבנה מחדש ב-n8n | chat_17 |
| 22 | נוספו 4 התרחישים הקריטיים הכבויים כהסבר ל-3 עסקאות ו-0 הזמנות | chat_26 |
| 23 | נוספו רשימות "החשבון הישן" (פעילים/כבויים) + 4 תרחישים עם יעד כתיבה לא ידוע | chat_22 |
| 24 | פילוח **525 האירועים התקועים** לפי וובהוק + כלל החסימה המפורש | chat_22, chat_26 |
| 25 | נוספה תוכנית ה-cutover בת 5 השלבים | chat_22 |
| 26 | נוספו gotchas רוחביים: `ifempty(Data[1])`, `data.data` ב-Iterator, שדה חסר = ריק ≠ yes | chat_06, chat_19, chat_22 |
| 27 | נוסף מרשם רוטציית טוקנים (5 מפתחות) — **ללא ערכים**, עם סייג התזמון | chat_20–27 |

---

## פרטי חשבון

> נקרא מ-API של Make ב-26.07.2026.
**חשבון:** `Revital Yaish רויטל יעיש` · organization **4829531** · team **2425546** · אזור **eu2**
**משתמש:** revital.vitrue@gmail.com (id 5058425) · timezone Asia/Jerusalem
**API base:** `https://eu2.make.com/api/v2/` · header `Authorization: Token <key>` — ⚠️ **המפתח נחשף בצ'אט — לרוטציה.** לא לרשום ערך במסמך.
**שם החיבור (connection) בכל מודולי פיירברי:** **"Revital - New"**
**Timezone של הארגון חייב להיות `Asia/Jerusalem`** — כל חישוב תאריכים בתרחישים נשען עליו.

> ⚠️ **גוצ'ה:** Make חוסם קריאות API ללא `User-Agent` של דפדפן ומחזיר `403 error code: 1010` (Cloudflare). חובה לשלוח User-Agent.
> ⚠️ **גוצ'ה:** הגדרת `fields` **ריקה** במודול פיירברי = **כל השדות**. תקין ועובד, לא באג.

---

## ⛔ כלל הפרויקט — Make מול n8n

> **"פיתוח חדש = n8n. תחזוקת קיים = Make, ידנית, ע"י מייק בלבד. קלוד לעולם לא כותב ל-Make דרך API."**

הכלל אושרר במפורש ב-chat_04 ו-chat_05 (קלוד סירב מיוזמתו לגעת ב-Make וניתב את התיקון לצד Fireberry) ונאכף שוב ב-chat_20/21/26/27.
כלל משלים מ-chat_12: **לוגיקת מסך (UI) = JS בצד לקוח בתוך פיירברי. אורקסטרציה ואינטגרציות = n8n/Make.** מייק פסל n8n עבור לוגיקת UI: "חיפוש המוצרים, החתימה ובניית הקישור — הכל ישירות בקוד ב-JS, בלי לצאת החוצה למערכת חיצונית."

---

## מה רץ איפה בפועל

| צינור / תהליך | פלטפורמה | סטטוס | הערה |
|---|---|---|---|
| קליטת לידים מרכזית (`Main Leads CRM v1.02`) | **Make** | 🟢 חי | הוובהוק `Revital_NewCRM_Michael`; 5 באגים מאומתים פתוחים |
| Facebook Leads → Main Leads CRM | **Make** | 🔴 כבוי | מעולם לא רץ · 10 מודולים |
| Website Leads → Main Leads CRM | **Make** | 🔴 כבוי | מעולם לא רץ · 5 מודולים |
| שליחת מסמך לחתימה (Scenario A טעינה + B שליחה) | **Make** + JS בצד לקוח (הכפתור) | 🟢 חי חלקית | סנריו B לא מחזיר `submission_url` — חוסם |
| קליטת מסמך חתום מטופסי (`Signed Document from Tofsy`) | **Make** | 🟢 חי | 4 מודולים · retry 3×30 דק' · DLQ |
| תשלומים — `New payment - CloudChat` | **Make** | 🟢 חי | **לא כותב לפיירברי כלל** |
| תשלומים — `Finance 3 - Create Payments Records` | **Make** | 🔴 כבוי · 42 בתור | 30 מודולים · רץ בהצלחה 22.07 · בלו-פרינט לא סופק |
| מסך סליקה מוטמע / בניית קישור תשלום | **JS בצד לקוח** + וובהוק Make מתוכנן | 🟡 נבנה ולא הועלה | תרחיש Make בן **4 מודולים** ל-`createPaymentProcess` של Grow — טרם נבנה |
| כפתור תשלום ידני | **JS בצד לקוח** | 🟢 חי | כל הקריאות דרך `/api/record/...` בסשן המשתמש — **אפס טוקנים בקוד** |
| תזכורות וובינר — עולם ישן | **Make** (`Webinar Reminders - Old CRM`) | 🟢 חי | **נכס** — מפרט התנהגות אמין |
| תזכורות וובינר — עולם חדש | **Make** (`Webinar Reminders (New CRM)`) | ⛔ deprecated · כבוי | 27 מודולים · **מעולם לא רץ** · נבנה מחדש ב-n8n (6.6a / 6.6 / 6.7) |
| תזכורת פגישות למחר (`Meetings Reminders`) | **Make** | 🟡 נבנה ולא הועלה | 13 מודולים · **לא מתוזמן** · חסום על `flow_ns` מטל · Run once ידני |
| ברודקאסט אורחים שבועי (`weekly_guest_broadcast`) | **Make** | 🟢 חי | 10 מודולים · Schedule יומי 18:00 · יובא 9/10, מודול 10 תוקן ידנית |
| טופס שקילה שבועי — תהליך ליווי | **Make** (`9490447`) | 🟢 חי | רץ 20.07 · ⚠️ ראה סתירת יום השקילה למטה |
| סנכרון סטטוסי מחזור בוסט | **n8n** | 🟡 נבנה ולא הועלה | ⛔ **לא** תרחיש Make. חלופת Make בת 5 מודולים שמורה כנספח בלבד |
| WF-16 מעקב סטטוסים / WF-17 מכירת ליווי אחרי בוסט | **n8n** | 🟡 נבנה ולא הועלה | קונבנציות: בלוק `Config`, דגל `DRY_RUN`, `WF16ErrHandler01`, credential `Revital Yaish new CRM` |
| צירוף לקבוצת WhatsApp | **n8n** | 🟡 נבנה ולא הועלה | GreenAPI = **ניהול קבוצות בלבד**; CloudChat = שליחת הודעות |
| ניהול קבוצות GreenAPI ב-Make | **Make** (`9484992`) | 🔴 כבוי | **סטאב של מודול אחד** ונשאר כזה |

> ⚠️ **סתירה פתוחה — קריטריון בחירת פלטפורמה.** ההכרעה לא הייתה עקבית היסטורית: WF-08 תועד כ-n8n אך מומש ב-Make; WF-16/WF-17 ב-n8n; קליטת הלידים והחתימות ב-Make. הכלל הרשמי (למעלה) קובע קדימה, אך המימושים הישנים סותרים אותו.
> **מקור:** chat_08 + chat_10 (27–28/07/2026) · chat_21/26/27. **בעלים להכרעה:** מייק.

---

## מצב החשבון — צילום 26/07/2026

- **37 תרחישים** · **30 וובהוקים** · **19 פעילים** · **18 כבויים** · **525 אירועים תקועים בתורים** · אזור **eu2**
- ⚠️ **סטטוסי ON/OFF דורשים אימות מחדש** — הצילום מ-26/07 והתמונה השתנתה מאז (chat_26).
- 🔴 **מצב תפעולי:** נכון ל-26/07/2026 החשבון החי במצב **clean state** למעט שני שינויים מ-22-23/07: עדכון `pcfPowerlinkToken` ב-1036, ותיקון קריטריון חיפוש ב-Make. בשש מתוך שמונה השיחות האחרונות **לא בוצע שום שינוי בחשבונות החיים**.

### 🔴 4 תרחישים קריטיים כבויים — ההסבר ל-3 עסקאות ו-0 הזמנות

| תרחיש | השלכה |
|---|---|
| `Facebook Leads > Main Leads CRM רויטל יעיש` | לידים מפייסבוק לא נכנסים ל-CRM החדש |
| `Website Leads > Main Leads CRM (רויטל יעיש)` | לידים מהאתר לא נכנסים ל-CRM החדש |
| `Webinar Reminders (New CRM)` | כבוי בזמן שהגרסה הישנה רצה — כפילות עולמות |
| `Finance 3 - Create Payments Records` | **0 רשומות תשלום** במערכת החדשה |

---

## כל התרחישים (37)

| id | מצב | שם | מודולים | נערך | היסטוריית ריצה |
|---|:--:|---|---:|---|---|
| `8223019` | 🟢 ON | BoTcast Sequencial | — | — | ❓ יעד כתיבה לא ידוע |
| `7415737` | 🟢 ON | Boost Reminder | — | — | ❓ יעד כתיבה לא ידוע |
| `7133762` | 🟢 ON | Create contact - Cloudchat (1.01) | — | — | חשבון ישן |
| `9523761` | 🟢 ON | Document button from CRM | — | — | Scenario A — טעינת קטלוג |
| `7133769` | 🟢 ON | Facebook Leads - Cloudchat (1.01) | — | — | חשבון ישן |
| `7158111` | 🟢 ON | Firberry CRM | — | — | חשבון ישן — האחרון לכבות ב-cutover |
| `9513015` | 🟢 ON | Form_After Boost Webinar | — | — | — |
| `6812655` | 🟢 ON | Integration Facebook Lead Ads | — | — | חשבון ישן |
| `7133758` | 🟢 ON | Main Chatbot Scenario - CloudChat (1.01) | — | — | חשבון ישן |
| `9339860` | 🟢 ON | Main Leads CRM  - Revital Yaeish N(Template Version 1.02) | — | — | רץ 26.07.2026 07:36 (15 ops) |
| `7133760` | 🟢 ON | Main Leads CloudChat (1.01) | — | — | חשבון ישן |
| `7133755` | 🟢 ON | New payment - CloudChat (1.01) | — | — | חשבון ישן · לא כותב לפיירברי |
| `7133754` | 🟢 ON | Performance Report (1.01) | — | — | חשבון ישן |
| `9547511` | 🟢 ON | Signed Document from Tofsy | 4 | — | רץ 23.07.2026 |
| `7166372` | 🟢 ON | Webinar Reminders - Old CRM | — | — | חשבון ישן — **נכס** |
| `7810658` | 🟢 ON | Webinar_Welcome | — | — | ❓ יעד כתיבה לא ידוע |
| `9490447` | 🟢 ON | טופס שקילה שבועי - תהליך ליווי - מוכן | — | — | רץ 20.07.2026 |
| `9472247` | 🟢 ON | עדכון מסמכים בכפתור שליחת מסמכים | — | — | — |
| `7413890` | 🟢 ON | עדכון קישור קבוצה שבועי | — | — | ❓ יעד כתיבה לא ידוע |
| `7155969` | 🔴 OFF | 5. Webinar Movements | — | — | חשבון ישן |
| `7228986` | 🔴 OFF | After Webinar (עבר למייק שלהם) | — | — | חשבון ישן |
| `7133771` | 🔴 OFF | Create CloudChat Message Template For Botcast (1.01) | — | — | חשבון ישן |
| `9362315` | 🔴 OFF | Facebook Leads > Main Leads CRM רויטל יעיש | 10 | 09.06.2026 | מעולם לא רץ · 🔴 קריטי |
| `9560342` | 🔴 OFF | Finance 3 - Create Payments Records On Powerlink CRM (Template) | 30 | 22.07.2026 | רץ בהצלחה 22.07.2026 (9 ops) · 42 בתור · 🔴 קריטי |
| `9484992` | 🔴 OFF | Green API | 1 | 21.07.2026 | סטאב מודול אחד |
| `7904290` | 🔴 OFF | HTTP | — | — | — |
| `7107797` | 🔴 OFF | Integration Google Sheets | — | — | חשבון ישן |
| `9461766` | 🔴 OFF | Integration HTTP | — | — | — |
| `9504448` | 🔴 OFF | Integration Tally | 1 | 09.07.2026 | — |
| `7133774` | 🔴 OFF | Notifications System - CloudChat (1.01) | — | — | חשבון ישן · 5 בתור |
| `9513781` | 🔴 OFF | Test #! | — | — | — |
| `7133773` | 🔴 OFF | Testing Scenario - CloudChat (1.01) | — | — | חשבון ישן |
| `9363636` | 🔴 OFF | Webinar Reminders (New CRM) | 27 | 09.06.2026 | מעולם לא רץ · ⛔ deprecated → n8n |
| `9362762` | 🔴 OFF | Website Leads > Main Leads CRM (רויטל יעיש) | 5 | 09.06.2026 | מעולם לא רץ · 🔴 קריטי |
| `8119255` | 🔴 OFF | דיוור | — | — | חשבון ישן |
| `9523034` | 🔴 OFF | חיבור טפסים - מקור (טופסי) | 3 | 14.07.2026 | — |
| `7414624` | 🔴 OFF | עדכון בטבלה לאחר הצטרפות לקבוצה | — | — | חשבון ישן |

---

## ⭐ `Main Leads CRM - Revital Yaeish N (Template Version 1.02)`

**התרחיש המרכזי של קליטת לידים ל-Fireberry החדש.** דלוק ורץ. ריצה אחרונה מתועדת **26.07 בבוקר, 15 אופרציות**.
**טריגר:** וובהוק מרכזי **`Revital_NewCRM_Michael`** — `https://hook.eu2.make.com/srwyryrt7083d17hk1aidxnt9bjj7fqx`
**סיווג בצ'קליסט הפערים:** "בנוי ועובד — לא נוגעים" — ⚠️ הסיווג נכון פורמלית (הבאגים אינם בסנריו לבדו), אך יש להוסיף את הסייג: "עובד — כפוף לערך ברירת המחדל ב-1036/`pcfproduct`".

### ⚠️ סתירה פתוחה — מזהה התרחיש

| עמדה | מקור | תאריך |
|---|---|---|
| **Scenario ID = `9339860`** | chat_05 (אליאל + קלוד, ניתוח blueprint) | ~28/07/2026 |
| **Scenario ID = `6600296`** ("הוובהוק מדף הנחיתה") | chat_04 (דיבוג הריצה שנכשלה) | ~28/07/2026 |
| `1452508` — **תרחיש/ריצה אחרים**, אוטומציה פנימית "לא רכשו בוסט 5 ימים"; שימש כריצה משווה | chat_04 | ~28/07/2026 |

⚠️ **אותו קובץ `Main Leads CRM Revital Yaeish N Version 1.02.blueprint.json` יוחס לשני מזהים שונים.** ההשוואה בין שתי הריצות **אינה ראיה מכריעה** כי הן משני סנריו שונים.
**דרוש אימות בממשק Make: איזה מספר הוא Scenario ID ואיזה Execution ID.** **בעלים: מייק.**

### מבנה התרחיש

```
Webhook (מודול 1)
 └─ משיכת הגדרות (מודול 54 — אובייקט 1036, name="1")
 └─ ~9 ענפי "בדוק אם קיים → צור אם לא"  [plquery → router → createobject]
     מקור הגעה · צורת הגעה · מודעה · קהל יעד · תוכן · מילת מפתח · מיקום · קמפיין · פאנל
 └─ נירמול טלפון (TransformerParseNumber · Ignore על שגיאה)
 └─ חיפוש Google Sheets (מודול 59)
 └─ ראוטר 148 ── ענף 1: {{1.opportunity_record}} = yes → תהליך מכירה (4)
 │              └─ ענף 2: {{1.marketing_record}} = yes → רישום שיווקי (1002)
 └─ ראוטר ראשי: זיהוי מוצר לפי UTM → חיפוש לקוח → יצירה/עדכון
 │              → חיפוש מכירה → יצירה / עדכון / סימון כפול לפי חלון זמן
 └─ WebhookRespond
 └─ ענף HTTP — שולח JSON הלאה
```

### שרשרת ה-`productid` — 54 → 69 → 153/157 → 37

| מודול | מה עושה |
|---|---|
| **54** | Query על **אובייקט 1036** ("הגדרת משתמש") עם `name = "1"`. מחזיר תמיד את אותה רשומת הגדרות. בתוכה `pcfproduct` = מוצר ברירת מחדל. **מודול 54 לא בוחר מוצר — הוא שולף הגדרות.** |
| **69** | מציב `{{54.pcfproduct}}` לתוך המשתנה `productid` |
| **153** | דריסת `productid` — חיפוש מוצר **לפי שם** (רץ רק אם הוובהוק הגיע עם `utm_product`) |
| **157** | דריסת `productid` — חיפוש מוצר **לפי מזהה** (רץ רק אם הוובהוק הגיע עם `utm_product`) |
| **37** | יצירת/עדכון העסקה — כאן `productid` נכנס לשדה `pcfProduct` |

> **הכלל:** בלי `utm_product` בוובהוק — ברירת המחדל מ-1036 היא זו שנכנסת לעסקה. הערך השמור שם ("הרצאת אורח") הוא ככל הנראה שריד משכפול תבנית Vitrue. **זה לא באג ב-Make — זה ערך דאטה שגוי ב-Fireberry.**
> **מודול 54 מחזיק גם את `pcfNumOfHoursNewOpportunity`** (=24) — חלון הזמן שבו עסקה עם אותו מוצר **מתעדכנת במקום להיווצר**. מתאים לליד, **לא לתשלום**.

### ראוטר 148 — ושדה חסר שנחשב "ריק"

- ענף 1 · פילטר `{{1.opportunity_record}} = yes` → יוצר תהליך מכירה (אובייקט 4)
- ענף 2 · פילטר `{{1.marketing_record}} = yes` → יוצר רישום שיווקי (אובייקט 1002)

🔴 **הבאג שמסביר "96 לקוחות מול 3 עסקאות":** שדה **חסר** בפיילוד מתפרש כ**ריק** ב-Make, ו-`ריק = "yes"` הוא שקר ⇒ **שני הענפים נחסמים בשקט והריצה נראית ירוקה.**
בפיילוד שמייק הריץ היו רק `q1`–`q6`, `email`, `phone`, `f_name`, `l_name`, `full_name`, `utm_source`, `botcast_*` — **אין `opportunity_record`, אין `marketing_record`**.

> ⚠️ **כלל מחייב:** כל מקור ליד שמחובר לוובהוק המרכזי **חייב** לשלוח `opportunity_record` ו-`marketing_record` במפורש.
> ⚠️ **בתשלום חובה לשלוח `utm_product = בוסט`**, אחרת העסקה נפתחת בלי מוצר. פרמטרים נוספים שנצפו: `funnel`, `placement`, `utm_*`.

### מודולים 40 / 41 — הרישום השיווקי

- **מודול 40 "קבלת משתנים"** — פילטר בשם "לא ממשיכים אם לא רוצים לפתוח רישום שיווקי", דורש `marketing_record = "yes"`.
- **מודול 41 "יצירת רישום שיווקי"** — יוצר רשומה **1002** עם `pcfAccountid`, `pcfSale`, כל ה-UTM-ים, טופס/עמוד/פאנל, אישור דיוור וסוג רישום.

🟡 **המלצה פתוחה — טרם בוצעה:** לרכך את הפילטר במודול 40 ל-"המשך אלא אם `marketing_record = no`". החלופה (לוודא שכל דף נחיתה שולח `marketing_record=yes`) **נדחתה** כנקודת כשל בכל מקור ליד חדש. **בעלים: אליאל (Make ידני).**

### לוגיקת הדה-דופ — שלושה מסלולים, לא שניים

טלפון → `TransformerParseNumber` → חיפוש לקוח לפי טלפון (עם Feeder ל"יותר מלקוח אחד") → ואז:

1. **אין מכירה פתוחה** → יצירה
2. **יש** → עדכון מלא
3. **יש** → **"עדכון מכירה כ-כפול"** — מסמן `pcfReregistration`, מעדכן רק UTM + תאריך כניסה אחרון

המוצר נקבע לפי UTM: חיפוש לפי שם, ואם נכשל — לפי מזהה.

### מה התרחיש יוצר — עד 11 אובייקטים

| קטגוריה | אובייקטים |
|---|---|
| **תמיד** | לקוח (1) — יוצר/מעדכן · תהליך מכירה (4) — יוצר/מעדכן · **רישום שיווקי (1002) — תמיד נוצר חדש בכל כניסה** |
| **רק אם לא קיים** | 8 אובייקטי UTM מאסטר: `1043`, `1044`, `67`, `1003`, `1028`, `1045`, `1046`, `1047` |
| **לעולם לא נוצר** | **`1042` (משפך) — חיפוש בלבד, אין `createobject`** |

### חוזה תשובת הוובהוק

```json
{"account_id":"...","oppurtunity_id":"...","marketing_record_id":"..."}
```

> ⚠️ **`oppurtunity_id` — שגיאת כתיב מכוונת בקוד: שתי p, בלי o. להעתיק verbatim.**
> ⚠️ חובה לוודא ש-**`Wait for response` מסומן** בוובהוק, אחרת מוחזר ריק.

---

## 🐛 רשימת הבאגים ב-`Main Leads CRM` — 5 מאומתים מול החשבון החי

> נבדקו מול ה-API החי של רויטל (chat_04, ~28/07/2026). **טרם בוצעו ב-Make.** ביצוע ידני של מייק בלבד.

### באג 1 · שדות שלא קיימים באובייקט — סיבת הכישלון העיקרית

**Fireberry מפיל את כל המודול על כל שדה לא מוכר אחד.**

| מודול | אובייקט | שדה שגוי | התיקון |
|---|---|---|---|
| **25** יצירת לקוח | לקוח (1) | `pcfFunnelName` | ← `pcfFunnels` (lookup ל-1042) |
| **25** | לקוח (1) | `pcfCompany`, `pcfDepartment`, `pcfRole` | ← **מחק** (קיים רק `pcfOccupation`) |
| **37** יצירת מכירה | תהליך מכירה (4) | `pcfFunnelName` | ← `pcfFunnels` |
| **37** | תהליך מכירה (4) | `pcfBillingcity` | ← `pcfCity` |
| **44** עדכון לקוח | לקוח (1) | `pcfCompany`, `pcfRole`, `pcfDepartment` | ← **מחק** |
| **46 / 49** עדכון מכירה | תהליך מכירה (4) | `pcfFunnelName`, `pcfBillingcity` | ← `pcfFunnels` / `pcfCity` |

> **מקור הבאג:** `pcfFunnelName` קיים **רק באובייקט 1002 (רישום שיווקי)**, כטקסט. מי שבנה את הסנריו העתיק את השם משם גם ללקוח ולמכירה, שם הוא נקרא `pcfFunnels`. **טעות העתקה בבנייה, לא רגרסיה** — ה-snapshot מ-7.5.2026 כבר לא מכיל `pcfFunnelName` בלקוח ובמכירה.
> ⚠️ **אם זו טעות בתבנית המקורית של ויטרו — היא יושבת אצל כל לקוחות ויטרו שקיבלו את הסנריו. מייק צריך לדעת.** (החקירה נדחתה.)

### באג 2 · ענף הפאנל שבור לחלוטין (מודולים 143–147)

- **143** מחפש באובייקט **1042** (משפך) ✅
- **145** יוצר באובייקט **1047** (מיקום הגעה — UTM Placement) ❌ — copy-paste מענף ה-placement
- הראוטר **144** בודק `143.Data[].customobject1047id` — שדה שלעולם לא יחזור מ-1042, ולכן ענף "אם קיים" **לא רץ אף פעם**
- **תוצאה:** כל ליד יוצר רשומת "משפך" חדשה **בתוך אובייקט המיקום**. זבל מצטבר.

### באג 3 · סדר הראוטים — המשתנה `funnel` תמיד ריק

ענף הפאנל הוא הראוט **האחרון** ברואטר **74**. מודול **123** (GetVariables) קורא את `funnel` **לפני** שהוא נכתב.
**תיקון:** להעביר את ענף הפאנל למעלה ברואטר 74, לפני הענף הראשי — כמו שאר ענפי ה-UTM.

### באג 4 · מודול 166 — מיפוי ריק

מודול **166** (עדכון לקוח) — מיפוי ריק לגמרי (`objectid` + `objecttype` בלבד). עדכון עם body ריק מחזיר שגיאה.
**תיקון: למחוק את המודול.**

### באג 5 · סימן הפוך ב-`addHours` (ראוטר 51)

- **49:** `createdon > addHours(now; 24)` → **אף פעם לא true**
- **46:** `createdon < addHours(now; 24)` → **תמיד true**
- במודול **37** זה כתוב נכון (`"-" + 24`). **חסר המינוס.**
- **תוצאה:** "עדכון מכירה מלא" לא רץ אף פעם; הכל הולך ל"עדכון כ-כפול".
- **תיקון:** להוסיף מינוס ל-`addHours` בשני התנאים בראוטר 51.

### 🔴 `pcfPage` — גלישת אורך · נקודת כשל יחידה ב-5 מודולים

`pcfPage` הוא **text** בלקוח (1), תהליך מכירה (4) ורישום שיווקי (1002). **כל שדות ה-text ב-Fireberry הם `maxlength: 200` כברירת מחדל.** ה-URL מדף הנחיתה הוא **~750 תווים** (ה-`ttclid` של טיקטוק לבדו ~380) — פי 3.5 מהמגבלה.

`pcfPage` יושב במודולים **25, 37, 41, 46, 49**.
> **`pcfPage` = נקודת כשל יחידה החוזרת ב-5 מודולים (25/37/41/46/49). זה לא 5 באגים — זה אחד.**

**פעולה:** לאמת `maxlength` בממשק (לא ב-snapshot, לא ב-API). אם 200 — אחת מהשלוש: (א) להעלות ל-2000; (ב) `{{substring(1.page; 0; 200)}}`; (ג) לשלוח רק path בלי query string (הנקי ביותר).

### ✅ `pcfRegistrationForm` — picklist · **נפתר**

| אובייקט | טיפוס |
|---|---|
| לקוח (1) | text ✅ |
| תהליך מכירה (4) | text ✅ |
| **רישום שיווקי (1002)** | **picklist** — ערכים 1–4 בלבד |

מודול **41** שלח `pcfRegistrationForm = {{1.form}} = "טופס חדש"` → ה-picklist דחה מחרוזת לא חוקית.
✅ **נפתר** — **אליאל** הוסיף ערך **"טופס חדש" = 5**. מודול 41 אמור לעבור. (תועד chat_04, ~28/07/2026.)

### 🔴 דף הנחיתה לא ממפה UTM — התיקון **לא** ב-Make

הפיילוד מגיע עם `utm_source: null`, `utm_medium: null`, `utm_adset: null`, `utm_content: null`, `utm_keyword: null`, `placement: null` —
**אבל בשדה `page` יושב הכל:** `utm_source=tiktok`, `utm_medium=paid`, `utm_id=1858172580954417`.

**דף הנחיתה שולח רק `utm_ad` ו-`utm_campaign`.** ⇒ **6 מתוך 8 ענפי ה-UTM לא רצים בכלל, וכל האטריביושן של רויטל ריק.**
> **כשל אטריביושן — התיקון הוא בצד דף הנחיתה, לא ב-Make.** אלטרנטיבה זמנית: פרסור של `1.page` בתוך התרחיש.

### 🟠 חשד פתוח בעדיפות גבוהה — מודול 59 (Google Sheets)

מודול **59** מצביע על spreadsheet קשיח **`18dKg8S8...`** בעוד `pcfCustomFieldsSheetID` בהגדרות של רויטל הוא **null**.
אם זו טבלת ויטרו ולא של רויטל, או שאין הרשאה → המודול מחזיר **0 bundles** ו**כל הזרוע הראשית נעצרת בשקט, בלי שגיאה.**
זו גם **תלות חיצונית לא-ממופה**: מחיקה או שינוי של הגיליון שוברים את התרחיש. **משימה פתוחה: לבדוק מה יושב בגיליון.**

### ⛔ מודול 25 — עדיין לא נסגר

השגיאה גנרית. 4 השדות שנמחקים כנראה לא הסיבה (הגיעו ריקים, ו-Make משמיט שדות ריקים). שני חשודים:

1. **`statuscode` מופיע פעמיים במודול** (פעם 1, פעם 6)
2. **`pcfQuestionSelect1`** — רשימת בחירה עם ערך אחד בלבד ("כן"), מוזנת מנוסחה התלויה במודול Google Sheets

> **דרוש: צילום INPUT של מודול 25 מה-execution log.**

### רשומת ההגדרות (אובייקט 1036, `name = "1"`) — ערכים שנקראו

- `pcfproductname` = **"סדנה בוסט"** · `pcfproduct` = `2f73403a-20de-47a7-b0cb-df4761b45f21`
- `pcfNumOfHoursNewOpportunity` = **24**
- `pcfSmsName` = **"Vitrue"** ⚠️ (צריך להשתנות לרויטל?)
- `pcfUpdateLeadSameProductInterest` = **"עדכון"**
- כל 8 שדות `pcfCreateUTM*NotFound` = **"כן"**
- `pcfupdatemarketingregis` (סשן קצר) = **"לא"** · `pcfupdatemarketingregislong` (סשן ארוך) = **"כן"**
- `pcfLeadsSheetID`, `pcfCustomFieldsSheetID`, `pcfImportLeadsGS`, `pcfSalesManger`, `pcfmarketingwebhook` = **null**
- `pcfPowerlinkToken` — ⚠️ **נחשף בצ'אט — לרוטציה.**

---

## שכבת התשלומים

> ⚠️ **התשלומים אינם "העברה" אלא בנייה מחדש** — הישן על **קארדקום**, החדש על **משולם**. כל ניסוח שמתאר את שכבת התשלומים כ"העברה" שגוי.

### השרשרת המלאה

```
Grow / משולם
  → webhook 3167900 (Cardcom - new payment - Cloudchat)
  → New payment - CloudChat (1.01)   [🟢 חי · לא כותב לפיירברי]
  → HTTP → hook.eu2.make.com/hmutuk26...
  → Finance 3 - Create Payments Records   [🔴 כבוי · 30 מודולים · 42 בתור · רץ בהצלחה 22.07]
  → Fireberry ❓
```

⛔ **הבלו-פרינט של `Finance 3` לא סופק — זה חסם.** החוליה האחרונה (האם ומה נכתב לפיירברי) לא מאומתת.

### `New payment - CloudChat (1.01)` — 3 ענפים

1. יוצר/מעדכן מנוי בבוט
2. מעדכן שדות מותאמים ושולח ל-flow
3. **שולח ל-`Finance 3` ב-HTTP**

> **התרחיש לא כותב לפיירברי כלל.**

### מודול 93 — נרמול דו-לשוני (קארדקום ↔ משולם)

כל שדה עטוף ב-`ifempty`:

| נתון | קארדקום | משולם |
|---|---|---|
| מוצר | `Custom24` | `paymentDesc` |
| סכום | `suminfull` | `paymentSum` |
| תשלומים | `NumberOfPaymentsToPrint` | `allPaymentNum` |
| מזהה עסקה | `internaldealnumber` | `transactionCode` |
| טלפון | `InvMobile` | `payerPhone` |
| מייל | `UserEmail` | `payerEmail` |

### 🐛 מודול 142 — הנרמול מתבזבז

**מודול `142`** (ה-JSON ל-`Finance 3`) בנוי **אך ורק על שדות משולם**: `payerPhone`, `paymentSum`, `asmachta`, `cardSuffix`, `purchasePageKey`.
⇒ **תשלום מקארדקום: כל השדות ריקים, הנרמול של מודול 93 מתבזבז, והתשלום נופל בשקט.**

### פערי `Finance 3`

1. **`identifyParam` מועבר ל-`Finance 3` אך אף אחד לא מזין אותו** — זה השדה שאמור לשאת את `opportunity_id` מדף הסליקה. בלעדיו הזיהוי נשען על טלפון בלבד.
2. התרחיש **לא מחפש לקוחה**.
3. התרחיש **לא מחפש עסקה ולא מחזיר כלום**.

### ⚠️ מודולים 7 ו-31 ב-`Finance 3` — `ifempty` שלא היה שם

**במצב התבניתי המקורי מודולים 7 ו-31 עושים `customobject1039id = {{1.object_id}}` ישירות — התבנית לא משתמשת ב-`ifempty` כלל.**
ה-`ifempty` שהוסף גרם ל-**403**.
**הנחיה לתיקון:** fallback ל-GUID תקין + סימון **"Continue when no results"**.

### תרחיש התשלום המוטמע — מתוכנן, טרם נבנה

תרחיש Make חדש בן **4 מודולים** שקורא ל-`createPaymentProcess` של Grow ומחזיר URL על `secure.meshulam.co.il`.
מסך הסליקה כבר קורא ל-Make דרך `SIGN_URL`, כך שזה **וובהוק שני באותו דפוס**.
הפניה: `מדריך תרחיש make דף תשלום מוטמע`.

---

## מסמכים לחתימה — סנריו A ו-B

| | Scenario A — טעינת קטלוג | Scenario B — שליחה |
|---|---|---|
| וובהוק | `LOAD_WEBHOOK_URL` = `https://hook.eu2.make.com/c3lcf9yf35xfngvxmv1xhw28i3cmi2p2` | `SEND_WEBHOOK_URL` = `https://hook.eu2.make.com/53w7nb0ktyb42h5ymsfwmokpp2r6ovdf` |
| קריאה | POST עם `{opportunity_id}` | POST |
| timeout | 15000ms | 20000ms |

⛔ **מיושן:** ~~סנריו B בנוי מ-4 מודולי Query ומכיל בורר ערוצים SMS / Email / WhatsApp~~ ⛔ מיושן (הוחלף 03/08/2026).
**המצב הנכון:** **Query אחד** על `objecttype 4` לפי `opportunityid` (מחזיר lookups של לקוח ומוצר), **בלי Router**, והערוץ הוא **וואטסאפ קבוע** — `send_method:"whatsapp"` hardcoded בכפתור.

### חוזה התגובה של סנריו A

מחזיר **רק** `{recommended_id, product_name, catalog}` — **לא** מזהי הקשר.
`data.catalog` יכול לחזור כמחרוזת ⇒ `JSON.parse`, ואז `cat.data.Data || cat.data.DataArray`.
סינון פעילים: `String(r.pcfformactivename || r.pcfformactive || '').trim() === 'כן' || === '1'`.

### 🐛 חוסם — סנריו B לא מחזיר `submission_url`

הכפתור כבר קורא את השדה, אבל הוובהוק לא מחזיר אותו. **הפורמט הנדרש:**

```
Status 200 · Content-Type: application/json
{"response":"success","submission_url":"https://fill.tofsy.co.il/{{url_code}}"}
```

> **נימוק ארכיטקטוני (chat_25):** בלי אובייקט 1058, ה-`form_id` של כל חוזה מוטמע **קשיח בתוך Make**, וכל חוזה חדש דורש נגיעה בסנריו. עם 1058 — שורה בטבלה + קישור מוצר, ועודד יכול לעשות זאת לבד.

---

## `Signed Document from Tofsy` (`9547511`) — 4 מודולים

| מודול | מה עושה |
|---|---|
| **1** | וובהוק "קבלת טופס מטופסי" (instant). Payload: **`Opportunityid`** (העוגן), `pdf_url`, `Full_Name`, `date` |
| **4** | חיפוש תהליך מכירה (אובייקט 4) לפי `opportunityid` — לשליפת `accountid` |
| **5** | עדכון תהליך מכירה: `pcfSignatureStatus = 2` ("נחתם") + `pcfcfDocLink = {{pdf_url}}` |
| **7** | יצירת רשומה באובייקט **1038**: `name = {{Full_Name}} {{date}}`, `pcfLinkToDocument`, `pcfLinkedSale`, `pcfaccountid`, `pcfdocsigned = 1` |

**מה הסנריו לא עושה:** לא נוגע ב-Account · לא נוגע ב-1051 · לא מפעיל תשלום · **לא שולח כלום ללקוחה.**

**עמידות:** לכל 3 מודולי פיירברי **retry אוטומטי — 3 ניסיונות כל 30 דקות** · DLQ פעיל (Incomplete executions) + autoCommit.
מודול 4 שולף את **כל** שדות העסקה בשביל `accountid` אחד — בזבזני אך תקין; אופטימיזציה לא דחופה.

---

## `Meetings Reminders` — חיפוש פגישות למחר

**סטטוס: נבנה, לא מתוזמן, חסום על `flow_ns` מטל, במצב Run once ידני.**
13 מודולים בסדר: `1, 2, 3, 19, 20, 21, 22, 23, 24, 25, 26, 6, 7`

| מודול | תפקיד |
|---|---|
| **1** | HTTP — Fireberry v3 query |
| **2** | BasicFeeder — iterator |
| **3** | SetVariables |
| **19** | API auth |
| **20** | TransformerParseNumber |
| **21** | CreateJSON |
| **22** | Cloud Chat — New Subscriber |
| **23 / 25** | Break (onerror) |
| **24** | Get Contact Info |
| **26** | **Send Flow — נוסף ע"י קלוד, לא היה קיים** |
| **6** | PUT — סימון `pcfZoomReminderDay` |
| **7** | Sleep 2s |

### 6 התיקונים שהוחלו על הבלו-פרינט של מייק

| # | מודול | תיקון |
|---|---|---|
| Fix1 | 1 | הוספת `pcfClient_emailaddress1` |
| Fix2 | 20 | מקור הטלפון → `pcfClient_telephone1` |
| Fix3 | 21 | מקורות `first_name` / `last_name` / `phone` |
| Fix4 | 3 | `replace` שבור + `parseDate` / `formatDate` עם UTC |
| Fix5 | 6 | `tokenid` חסר ב-PUT |
| **Fix6** | **26** | **מודול Send Flow היה חסר לגמרי** |

### חוב טכני מתועד

- 🐛 **מודול 21** מפצל שם ל-first/last לפי מילה 1 ומילה 2 בלבד — **שם בן שלוש מילים ("רויטל בת שבע") יאבד את המילה השלישית.** לא תוקן.
- 🟡 **מודול 24 (Get Contact Info) מיותר** — ה-`user_id` ל-Send Flow נלקח ישירות מתשובת מודול 22.
- ⚠️ **קובץ `Meetings_Reminders_FIXED_blueprint.json` הוא נכס מזוהם** — טוקן פיירברי מוטמע בתוכו בשני מודולים (1 ו-6).

---

## `weekly_guest_broadcast` — 10 מודולים

**טריגר: Schedule יומי 18:00** (לא Webhook). הייבוא הצליח ב-9/10; **מודול 10 נפל ב-"Module Not Found"** (שם פנימי שגוי של מודול ההשהיה) ותוקן ידנית ל-**Tools → Sleep, Delay 2 שניות**, אחרי "CloudChat - שיגור ההזמנה".

סדר המודולים:
1. Set Variables
2. שאילתת מפגשים (אובייקט **1041**) למחר
3. Iterator — "לכל מפגש"
4. שאילתת ליוויים פעילים (אובייקט **1051**, `pcfStatus=2`)
5. Iterator — "לכל לקוחה פעילה"
6. נרמול טלפון (`onerror: Ignore`)
7. יצירת/מציאת מנוי בקלאודצ'אט
8. עדכון `data_param1-4`
9. שיגור תבנית
10. Sleep 2 שניות

### 🐛 באג Iterator שתוקן — gotcha כללי

- מודול 3 ("לכל מפגש"): Array שונה מ-`{{2.data}}` ל-**`{{2.data.data}}`**
- מודול 5 ("לכל לקוחה פעילה"): מ-`{{4.data}}` ל-**`{{4.data.data}}`**

אחרי התיקון: 5 סיבובים ירוקים, 5 שליחות.

> **gotcha כללי: תשובת פיירברי היא `{data:{data:[...]}}` — כל Iterator על שאילתת REST של פיירברי חייב נתיב כפול.**

---

## חוזה ה-params בתרחיש ה-Welcome

**`params 1–4` נושאים ערכים. `params 5–10` חייבים להיות ריקים לחלוטין בכל מסלול** — דריסה בכל שליחה, אחרת שאריות ישנות זולגות לקלאודצ'אט.

נוסחת `param_4` במודול 2 (verbatim):

```
{{if(1.product_name = "סדנה בוסט"; 1.boost_cycle_start; emptystring)}}
```

שדה הוובהוק הגולמי: `{{1.boost_cycle_start}}`

### באגים שנמצאו בשאריות

| param | מה הכיל |
|---|---|
| `param_5` | תאריך התחלה ומקף מילולי |
| `param_6` | `1.param6` — שדה שכבר לא קיים |
| `param_7`–`param_10` | אותה שארית |

### מפת ה-Switch לפי מוצר

| מסלול | params שמוזנים |
|---|---|
| **ליווי** | `data_param1` / `data_param2` / `data_param3` |
| **בוסט** | `data_param2` / `data_param3` / `data_param4` |
| **else** | — |

> ⚠️ **"הרצאת אורח" נשארת ב-Else ואינה מקבלת הודעה** — עד החלטת רויטל.

---

## GreenAPI ב-Make

התרחיש `Green API` (`9484992`) הוא **סטאב של מודול אחד** ונשאר כזה. **החלטת הפרויקט: אין תהליכים חדשים ב-Make.**
הפרדת תפקידים: **GreenAPI = ניהול קבוצות בלבד** (`getContacts`, `getGroupData`, יצירת קבוצה, נעילה) · **CloudChat = שליחת הודעות ללקוחות.**

⚠️ **אזהרת אבטחה:** אם ייבחר GreenAPI ישיר כערוץ שליחה — **הטוקן נכנס ל-URL של הצומת ⇒ נכנס ל-export של ה-workflow.** אסור לשלוח את ה-JSON בצ'אט או בוואטסאפ.

---

## תזכורות וובינר — נכס מול חוב

| תרחיש | מצב | הערה |
|---|---|---|
| `Webinar Reminders - Old CRM` (`7166372`) | 🟢 ON | **נכס** — מפרט התנהגות אמין. משמש כמקור אמת להתנהגות הנדרשת. |
| `Webinar Reminders (New CRM)` (`9363636`) | ⛔ **deprecated** · 🔴 OFF | **27 מודולים שמעולם לא רצו.** הוכרע לבנות מחדש ב-n8n → ראה `06_N8N_WORKFLOW_SPECS.md`, workflows **6.6a / 6.6 / 6.7**. |

---

## החשבון הישן — מפה

### תרחישי Make פעילים מול החשבון הישן

`Firberry CRM` · `Main Chatbot Scenario - CloudChat` · `Main Leads CloudChat` · `Create contact - Cloudchat` · `New payment - CloudChat` · `Facebook Leads - Cloudchat` · `Performance Report` · `Integration Facebook Lead Ads` · `Webinar Reminders - Old CRM`

### כבויים בחשבון הישן

`After Webinar` · `Create CloudChat Message Template For Botcast` · `Notifications System - CloudChat` · `Testing Scenario - CloudChat` · `5. Webinar Movements` · `עדכון בטבלה לאחר הצטרפות לקבוצה` · `דיוור` · `Integration Google Sheets`

### ❓ 4 תרחישים פעילים שלא ברור לאיזה חשבון הם כותבים

`Boost Reminder` · `Webinar_Welcome` · `BoTcast Sequencial` · `עדכון קישור קבוצה שבועי`

סווגו כ"בנוי ועובד" אך **אף אחד לא פתח אותם.** בדיקה של 10 דקות. **בעלים: מייק.**

### טופס האתר

WordPress · **`revital.mediasecret.co.il`** — **מחובר לחשבון הישן.**

---

## תוכנית ה-cutover (5 שלבים)

1. **חפיפה בכתיבה כפולה** — המשך לפי ביטחון, **לא לפי תאריך**.
2. **אימות יומי** בהשוואת ספירות בין המערכות.
3. **הפיכת `WRITE_TO_OLD_CRM = false`** — בלי לגעת בלוגיקה.
4. **כיבוי בסדר:** מקורות לידים ← הבוט ← תשלומים ← וובינר ← דיווחים ← `Firberry CRM`.
5. **הקפאת החשבון הישן ל-read-only. לא מוחקים.**

---

## וובהוקים (30) — כולל תורים תקועים

| id | שם | URL | **בתור** |
|---|---|---|---:|
| `3479103` | My Zoom Webinars webhook | (אין URL) | 🔴 **292** |
| `4241264` | Revital 6.7.2026 | `https://hook.eu2.make.com/d6hwc9o7b1q991ydfefk7otf4hz3cjcu` | 🔴 **179** |
| `4274104` | Create Payments Records ⭐ תשלומים | `https://hook.eu2.make.com/hmutuk26wedyj64r1kh2lyz2qwim37df` | 🔴 **42** |
| `4250062` | Welcome To Premium | `https://hook.eu2.make.com/bgj1ecpj7ypc427akrscbur895jt8a52` | 🔴 **6** |
| `3167909` | Notifications System - Cloudchat | `https://hook.eu2.make.com/yfaqutmaihlcchwowkyiwwp33gxdkfry` | 🔴 **5** |
| `3293927` | Add to group sheet | `https://hook.eu2.make.com/8228hof14pdg47c8e4wicndu3is6tpv0` | 🔴 **1** |
| `3167900` | Cardcom - new payment - Cloudchat | `https://hook.eu2.make.com/chw3swfshc1yicbwj7nf68k4lu6tkkmr` | 0 |
| `3167901` | Main Chatbot Scenario | `https://hook.eu2.make.com/uwmi6h5v2qgeyv2cqxjnriwq55kqlbkd` | 0 |
| `3167903` | Main Leads | `https://hook.eu2.make.com/vjoddgjbvdwj5nxcl0wq4w8yc2qnbx3y` | 0 |
| `3167904` | Create contact - Cloudchat | `https://hook.eu2.make.com/848xf9z43h71ifoy7f8s2skh5ewqdffa` | 0 |
| `3179611` | Firberry Webhook | `https://hook.eu2.make.com/uvhg84wahk9n86ne5al0obsb6pj57mpw` | 0 |
| `3209831` | Get Webinar Deatails | `https://hook.eu2.make.com/pbudj3320yalelmgqyw96nk72naboghn` | 0 |
| `3211877` | After Webinar | `https://hook.eu2.make.com/8c768qfetdpll1r80vnpsmv53c8ilo2s` | 0 |
| `3293516` | Join to whatsapp group | `https://hook.eu2.make.com/vnr46qr5wwn91cru0eh5f73au7ipp65n` | 0 |
| `3295659` | Boost Reminder | `https://hook.eu2.make.com/ljvu2b7dsyp8usbb12sffzck4cb00q5k` | 0 |
| `3470095` | Welcome Webinar | `https://hook.eu2.make.com/7ppiik6vvpxiz1hs21q4h5kdjx2a3vin` | 0 |
| `3660229` | Botckast Sequencial | `https://hook.eu2.make.com/2gove73j2ihq3aqpmlqiwxc0n8crbem7` | 0 |
| `4176436` | Revital_NewCRM_Michael ⭐ הוובהוק המרכזי | `https://hook.eu2.make.com/srwyryrt7083d17hk1aidxnt9bjj7fqx` | 0 |
| `4186110` | Website Leads #1 | `https://hook.eu2.make.com/yulw1jnwojl0xhq5ghpyxj8it3cqx5mt` | 0 |
| `4186124` | טופס מסמך לחתימה #1 ⭐ SEND_WEBHOOK | `https://hook.eu2.make.com/53w7nb0ktyb42h5ymsfwmokpp2r6ovdf` | 0 |
| `4196969` | מסמך לחתימה Tofsy#1 | `https://hook.eu2.make.com/yfi1r7n8k1n8eax7xa6jmlf9haaxq6tf` | 0 |
| `4235980` | שליחת מסמך לחתימה ⭐ LOAD_WEBHOOK | `https://hook.eu2.make.com/c3lcf9yf35xfngvxmv1xhw28i3cmi2p2` | 0 |
| `4243469` | Revital #1 | `https://hook.eu2.make.com/hd0qsibftbk4ewnn7sejamnd92xeqauu` | 0 |
| `4246730` | Weekly_Weight_Status ⭐ שקילה שבועית | `https://hook.eu2.make.com/cj15un4dudvcsozp13y1433994xmq4t2` | 0 |
| `4253774` | Welcome to Premium | `https://hook.eu2.make.com/wrf7at2u9jl5ku1afzmpod7za5ipmdp8` | 0 |
| `4254124` | TEst - New Leads | `https://hook.eu2.make.com/s8eede571aclv123vk8u1omauo5bjzao` | 0 |
| `4268332` | קבלת מסמך מטופסי ⭐ Tofsy | `https://hook.eu2.make.com/7g2xvjmgulpqoic8ai69e5sfm60vp4n7` | 0 |

### 🔴 525 האירועים התקועים — פילוח מלא

| וובהוק | אירועים בתור |
|---|---:|
| `My Zoom Webinars` | **292** |
| `Revital 6.7.2026` | **179** |
| `Create Payments Records` | **42** |
| `Welcome To Premium` | **6** |
| `Notifications System` | **5** |
| **סה"כ** | **525** |

**471 מתוך 525 שייכים לעולם הישן.**

> ⛔ **"אסור להדליק תרחיש כלשהו לפני בדיקת תוכן התור שלו."**
> הדלקה עיוורת של תרחיש **תשפוך מאות רשומות למערכת בבת אחת.** זו **משימה מספר 1 בפרויקט**.
> תקדים ה-525 הוא הנימוק לדפוס הבטיחות בכל אוטומציה חדשה: `DRY_RUN = true` כברירת מחדל · תקרת `MAX_PER_RUN` (25 ב-WF-16) · אם רשימת ה-DRY-RUN ארוכה מהתקרה — **לא הופכים ל-false** עד הכרעת מייק · בדיקת שלילה חובה.

---

## Gotchas רוחביים ב-Make

| # | Gotcha | מקור |
|---|---|---|
| 1 | **שדה חסר בפיילוד = ריק, ו"ריק = yes" הוא שקר.** פילטר שדורש `= yes` נחסם בשקט והריצה נראית ירוקה. | chat_22 |
| 2 | **`Data[]` ללא אינדקס = מערך.** ⛔ ~~`{{ifempty(3.Data[].pcfWeeksGift; 0)}}`~~ שגוי — מערך שמכיל איבר ריק אחד נחשב "לא ריק" וברירת המחדל 0 לא תופעל. **חובה `{{ifempty(3.Data[1].pcfWeeksGift; 0)}}`.** | chat_06 |
| 3 | **תשובת פיירברי היא `{data:{data:[...]}}`** — כל Iterator על שאילתת REST חייב נתיב כפול (`{{N.data.data}}`). | chat_19 |
| 4 | **`oppurtunity_id`** — שגיאת כתיב מכוונת בקוד (שתי p, בלי o). להעתיק verbatim. | chat_22 |
| 5 | **`Wait for response`** חייב להיות מסומן בוובהוק, אחרת `WebhookRespond` מחזיר ריק. | chat_22 |
| 6 | Make חוסם קריאות API ללא **User-Agent** של דפדפן → `403 error code: 1010`. | 26/07/2026 |
| 7 | `fields` **ריק** במודול פיירברי = **כל השדות**. תקין. | chat_27 |
| 8 | **Fireberry מפיל את כל המודול** על שדה אחד לא מוכר. | chat_04 |
| 9 | **כל שדות ה-text ב-Fireberry הם `maxlength: 200` כברירת מחדל.** | chat_04 |

---

## נספח — חלופת Make לסנכרון סטטוסי מחזור בוסט

⛔ **~~תרחיש `Boost Cohort — Daily Status Sync` נבנה ב-Make~~ ⛔ מיושן (הוחלף 03/08/2026).**
**לא נבנה שום תרחיש חדש ב-Make.** האוטומציה עברה ל-**n8n** → ראה `06_N8N_WORKFLOW_SPECS.md`.

הנספח נשמר **למקרה חזרה בלבד**:

**5 מודולים:** Query 1007 → Iterator `{{1.Data}}` → Set 5 משתנים (`today`, `d_startsale`, `d_boundary`, `d_end`, `cur`) → Set `desired` → [Filter] → Update

**הגדרות תרחיש נדרשות:**
- Sequential processing **ON**
- consecutive errors = **3**
- Allow storing incomplete executions **ON**
- Max cycles = **1**
- **Make → Organization → Timezone חייב `Asia/Jerusalem`**

⚠️ אם מודול 1 מוציא באנדל לכל רשומה — מדלגים על ה-Iterator ומזיזים את כל ההפניות מ-`2.` ל-`1.`.

> ⚠️ **הבהרה נוספת (chat_23):** אוטומציית פתיחת המחזורים **פותחת מחזור בלבד ולעולם לא סוגרת.** מגבלה חד-כיוונית — לכן **תיקון ידני של סטטוס יתבטל מעצמו במחזור הבא.** כל ניסוח שמתאר אותה כ"מנהלת סטטוס מחזור" שגוי.

---

## ⚠️ סתירות פתוחות

### 1. מזהה התרחיש של `Main Leads CRM`

**`9339860`** (chat_05, ~28/07/2026) מול **`6600296`** (chat_04, ~28/07/2026). `1452508` הוא **תרחיש פנימי אחר** ("לא רכשו בוסט 5 ימים") ששימש כריצה משווה — **ההשוואה אינה נקייה** כי מדובר בשני סנריו שונים.
**דרוש אימות בממשק Make — איזה מספר הוא Scenario ID ואיזה Execution ID. בעלים: מייק.**

### 2. קריטריון בחירת פלטפורמה — Make מול n8n

chat_26: "אין תהליכים חדשים ב-Make, אבל מה שבנוי ועובד ב-Make נשאר." · chat_21: היפוך אמצע-שיחה — כל אוטומציית הסטטוסים ל-n8n · chat_20: WF הצירוף לקבוצה ב-n8n · chat_27: **כל העבודה בפועל נעשתה ב-Make.** בנוסף WF-08 תועד כ-n8n ומומש ב-Make.
הכלל הרשמי נוסח (ראה למעלה), אך המימושים הקיימים סותרים אותו. **בעלים: מייק.**

### 3. יום השקילה השבועית

**ראשון 09:00** (משימה 13.1 ב-ClickUp + התרחיש `9490447` בפועל) מול **חמישי** (המצגת שהוצגה ללקוחה + ציר הזמן של סער וינברג שבו כל 6 השקילות בימי חמישי).
**מקור:** chat_08 + chat_10 (27–28/07/2026). **הסתירה מופיעה בארבעה נכסים:** `06_N8N_WORKFLOW_SPECS.md`, מסמך זה, המצגת, ותוכנית דאטת ההדגמה. **בעלים: מייק (מול רויטל).**

---

## 🔴 רוטציית טוקנים — 5 מפתחות

**⚠️ לעולם לא לרשום ערכי מפתחות במסמך.** כל אחד מהחמישה: **⚠️ נחשף בצ'אט — לרוטציה.**

| # | מפתח | היכן נחשף |
|---|---|---|
| 1 | **Fireberry `tokenid`** | chat_03, chat_10, chat_19, chat_25, chat_27 · גם בתוך `Meetings_Reminders_FIXED_blueprint.json` (מודולים 1, 6) |
| 2 | **Make API key** | טקסט גלוי — מקנה גישה מלאה לחשבון **וכל הקונקשנים מאחוריו** (Fireberry, Tofsy, GreenAPI, WhatsApp) |
| 3 | **Tofsy `api_key`** | סומן בתיעוד קודם (§9 של `PROJECT_KNOWLEDGE_signature_system.md`), טרם בוצע |
| 4 | **GreenAPI `apiTokenInstance`** | chat_20 |
| 5 | **CloudChat API key** | chat_13 · יושב כטקסט גלוי בבלו-פרינט של מודול 93 |

**אף רוטציה לא אומתה כבוצעה.** (תיעוד קודם שדיבר על "3 טוקנים" — ⛔ מיושן, המספר **5**.)

### צ'קליסט אחרי הרוטציה — 3 מקומות חובה

1. החיבורים ב-**Make** — connection **"Revital - New"**
2. ה-credential ב-**n8n** — `Fireberry — tokenid`, Header Auth
3. השדה **`pcfPowerlinkToken`** באובייקט **1036**

### ⚠️ תזמון — לא עכשיו

רוטציה **שוברת את כל חיבורי Make** עד שמעדכנים אותם. אם טל בונה במקביל — דברים ייפלו לו בלי שיבין למה.
הוכרע: **הרוטציה תבוצע רק אחרי סיום הטסטים**, בחלון מתואם. אחרי הרוטציה מעדכנים רק את ה-credential ב-n8n; ה-workflows עצמם לא נוגעים בטוקן ולכן לא יישברו.
**זו משימה E2 ב-`09_OPEN_QUESTIONS.md`. לא "ניצחון מהיר".**

> ✅ **דפוס נגדי לחיקוי:** בכפתור התשלום הידני **לא נחשף שום טוקן** — כל הקריאות עוברות דרך `/api/record/...` בסשן המשתמש המחובר. **זהו תקן הפרויקט לכל כפתור/ווידג'ט עתידי בפיירברי.**
