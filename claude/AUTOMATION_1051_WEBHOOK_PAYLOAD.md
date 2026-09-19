# אוטומציה פנימית: פתיחת תהליך ליווי חדש → וובהוק Make

> **עודכן 03/08/2026 — סקירת 26 שיחות הפרויקט.**

| # | מה שונה | מקור |
|---|---|---|
| 1 | הפיילוד **אושר ותקין ללא שינוי** — אומת 3 פעמים מול החשבון החי (27/07) | chat_19 |
| 2 | נוסף **המעטפת (envelope)** בת 4 השדות — `message_type` · `phone` · `fullname` · `email` — שמסבירה את הפער 92↔96 | chat_19 |
| 3 | נוסף **כלל בניית פיילוד**: רק שדות האובייקט שהאוטומציה יושבת עליו (1051→96 · 1041→5) | chat_19 |
| 4 | נוספה אזהרה מודגשת על התלות הקריטית ב-`pcfBoostLinked` עבור `boost_cycle_start` / `boost_cycle_group_link` | chat_19 |
| 5 | נוסף מיפוי ה-traversal המלא של קבוצת הוואטסאפ ושל מחזור הבוסט (verbatim) | chat_19 |
| 6 | נוסף **חוזה מינימלי מחייב**: 6 שדות חובה ביצירת רשומת 1051 | chat_22 |
| 7 | נוסף סיכון כשל: `ownerid` חובה + אין "מנטורית ברירת מחדל" על מוצר (14) | chat_22 |
| 8 | נוספה נוסחת `pcfEstimatedEndDate` וסייגיה (מחושבת ב-Make/n8n בלבד) | chat_22 |
| 9 | נוספה אזהרת **זוגות שדות כפולים** ב-1051 שעלולים לפצל דאטה | chat_22 |
| 10 | עודכן: 1051 גדל מ-31 ל-**57 שדות**, **26 מהם לא אופיינו מעולם** → ייתכן שהפיילוד חסר | chat_25 |
| 11 | נוסף: הטריגר **"בזמן יחסי" חסום ברישיון של רויטל** → כל תזמון עובר ל-Make/n8n | chat_19 |
| 12 | נוסף: `pcfContinuationStatus` (שדה חדש ב-1051) **כבר בפיילוד** — אושר | chat_18 |
| 13 | נוסף: `1051.pcfBoostLinked` נכתב בזמן צירוף לקבוצת בוסט; אין ליווי → **דלג בלי שגיאה** | chat_20 |
| 14 | נוספה **לוגיקת ה-Switch של מודול 24** (regex על `product_name`) + אזהרה על מודול 24 בתרחיש אחר | chat_19 / chat_10 |

---

> **נוצר:** 27/07/2026 · נבנה ונבדק מול החשבון החי (רשומת "בדיקה של הבדיקות")
> וובהוק יעד: `https://hook.eu2.make.com/b7ca4dujc848jbru83a0psoalhqloqg7`
> טריגר: רשומת תהליך ליווי (1051) נוצרה · פעולה: קריאה לכתובת אינטרנט (POST, Content-Type: application/json)

## מטרה
פיילוד שמן אחד ביצירת ליווי כדי לחסוך חיפושים במודולים ב-Make (מניעת 429).

---

## ⛔ אילוץ רישיון — הטריגר "בזמן יחסי" חסום

**טריגר "בזמן יחסי" באוטומציות הפנימיות של פיירברי אינו זמין ברישיון הנוכחי של רויטל** (המערכת מציגה "שדרג עכשיו").
המשמעות: **כל תזמון בפרויקט עובר ל-Make או ל-n8n** — אין הסתמכות על תזמון פנימי בפיירברי.

- דוגמה למימוש הנכון: תרחיש האורח השבועי הועבר ל-**Schedule יומי ב-Make (18:00)** במקום טריגר "בזמן יחסי". התרחיש בודק בעצמו אם יש מפגש מחר; אין — נגמר בשקט.
- **האוטומציה הזו (1051) אינה מושפעת** — היא יושבת על טריגר "רשומה נוצרה", שהוא אירועי ולא מבוסס-זמן.
- **כלל פרויקט:** כל מפרט שמניח תזמון בפיירברי — לתקן. תזמון = Make/n8n בלבד.
`[מקור: chat_19 · 27/07/2026]`

---

## 🔑 ממצאים מאומתים על מנוע התבניות של אוטומציות פנימיות (חלים על כל אוטומציה!)

0. **כלל בניית פיילוד:** הפיילוד נבנה **רק משדות האובייקט שהאוטומציה יושבת עליו.** ליווי (1051) → **96 שדות**; מפגש (1041) → **5 שדות בדיוק** (`message_type`, `lecture_topic`, `lecturer`, `lecture_date`, `zoom_link`). שדות של אובייקט אחר חוזרים ריקים או שוברים רינדור. `[chat_19]`
1. **אין גישה ל-GUID.** `{[!customobject1051id]}` וכל lookup מרונדרים כ**שם תצוגה**, לא כמזהה. נבדק גם בבורר השדות `{}` — אין "מזהה רשומה"/"קישור לרשומה". → כל תרחיש Make שצריך לעדכן את הרשומה חייב **חיפוש אחד**: query על 1051 לפי `name` = process_name, ממוין `createdon` desc, page_size 1. החיפוש מחזיר את כל ה-GUIDs האמיתיים.
2. **פיקליסטים מרונדרים כתוויות עברית** ("ליווי בתהליך"), לא כמספרים. פילטרים ב-Make על הפיילוד = השוואת טקסט; כתיבה חזרה ל-API = מספרים. לא לערבב.
3. **תאריכים בפורמט `DD/MM/YYYY HH:mm`** — לא ISO. ב-Make להשתמש ב-parseDate.
4. **תחביר traversal עובד:** `{[!lookup_field]}` (רמה אחת), `{[!lookupname]}` לשם ה-lookup. אומת כולל `pcfSalename`, `pcfProduct_pcfProductType`, `pcfaccountid_telephone1`.
5. **שדות textArea מסוכנים ב-JSON** — פיירברי לא עושה escaping לגרשיים/ירידות שורה. הם יושבים בסוף הפיילוד למחיקה קלה אם ריצות נופלות.
6. פתוח לבדיקה: `pcfSale_owneridname` חזר ריק בטסט — ייתכן שלא נתמך וייתכן שהעסקה בלי נציג. לוודא בטסט עם נציג משויך.
7. **gotcha כללי לכל שאילתת REST בפיירברי:** תשובת ה-API היא `{ data: { data: [ ... ] } }` — כל Iterator חייב נתיב כפול (`{{X.data.data}}`). באג זה הפיל את תרחיש הברודקאסט. `[chat_19]`
8. **ב-`/api/v3/query`** אפשר לשלוף את טלפון הלקוחה ישירות מתוך שאילתת הליווי דרך השדה המקושר **`pcfaccountid_telephone1`**, בלי שאילתה שנייה על אובייקט 1. **נגזרת:** ייתכן שחלק מהפיילוד מיותר — להצליב מול 96 השדות לפני קיצוץ. `[chat_17]`

---

## המעטפת (envelope) — 4 שדות

הפיילוד נשלח עטוף ב-4 שדות מעטפת שקודמים לגוף רשומת 1051. **הם אלה שמסבירים את הפער בין 92 מפתחות בגוף ל-96 שדות בסך הכול.**

```json
"message_type":"welcome",
"phone":"{[!pcfaccountid_telephone1]}",
"fullname":"{[!pcfaccountidname]}",
"email":"{[!pcfaccountid_emailaddress1]}",
```

| שדה | תפקיד |
|---|---|
| `message_type` | קבוע `"welcome"` — **מפתח הניתוב ב-Make.** נכנס ישירות ל-Input של ה-Switch במודול 24. מבדיל בין הפיילוד הזה לפיילוד המפגש (1041), שבו `message_type` נושא ערך אחר |
| `phone` | טלפון הלקוחה — הכניסה ליצירת/מציאת מנוי בקלאודצ'אט. **חייב נרמול** לפני שליחה (`0`→`972`, סיומת `@c.us`) |
| `fullname` | שם מלא — נשלח לקלאודצ'אט. ⚠️ **באג ידוע:** מודול הפיצול ל-first/last מפצל לפי מילה 1 ומילה 2 בלבד — **שם בן שלוש מילים ("רויטל בת שבע") מאבד את המילה השלישית** |
| `email` | מייל הלקוחה |

**הערה:** שדות אלה מופיעים גם בגוף הפיילוד תחת שמות אחרים (`client_phone`, `client_name`, `client_email`). הכפילות מכוונת — המעטפת היא החוזה שה-Make קורא, הגוף הוא הדאטה המלאה.

---

## הפיילוד (96 שדות = 4 מעטפת + 92 גוף)

> ✅ **מאושר ותקין ללא שינוי — אומת 3 פעמים מול החשבון החי, 27/07/2026.** `[chat_19]`
> ~~הפיילוד (92 שדות)~~ ⛔ מיושן (הוחלף 03/08/2026) — הספירה הנכונה כוללת את 4 שדות המעטפת = **96**.

```json
{
"message_type":"welcome",
"phone":"{[!pcfaccountid_telephone1]}",
"fullname":"{[!pcfaccountidname]}",
"email":"{[!pcfaccountid_emailaddress1]}",
"record_id":"{[!customobject1051id]}",
"process_name":"{[!name]}",
"created_on":"{[!createdon]}",
"created_by":"{[!createdbyname]}",
"created_by_person_or_system":"{[!pcfCreatedByPersonOrSystem]}",
"status":"{[!pcfStatus]}",
"status_update_time":"{[!pcfStatusUpdateTime]}",
"current_program":"{[!pcfCurrentProgram]}",
"continuation_status":"{[!pcfContinuationStatus]}",
"start_date":"{[!pcfStartDate]}",
"estimated_end_date":"{[!pcfEstimatedEndDate]}",
"weeks_number":"{[!pcfWeeksNumber]}",
"current_week":"{[!pcfCurrentWeek]}",
"initial_weight":"{[!pcfInitialWeight]}",
"current_weight":"{[!pcfCurrentWeight]}",
"weekly_weight":"{[!pcfWeeklyWeight]}",
"target_weight":"{[!pcfTargetWeight]}",
"distance_from_target":"{[!pcfsystemfield100]}",
"height_cm":"{[!pcfHeight]}",
"age":"{[!pcfAge]}",
"birthdate":"{[!pcfBirthdate]}",
"rmr":"{[!pcfRMR]}",
"rmr_formula":"{[!pcfsystemfield101]}",
"weigh_count":"{[!pcfWeighCount]}",
"last_weigh_date":"{[!pcfLastWeighDate]}",
"weighing_date":"{[!pcfWeighingDate]}",
"meetings_total":"{[!pcfMeetingsNumber]}",
"meetings_monthly":"{[!pcfNumMonthelyMeetings]}",
"meetings_done":"{[!pcfNumberMeetingsDone]}",
"meetings_left":"{[!pcfNumberMeetingsLeft]}",
"weekly_contact":"{[!pcfWeeklyContact]}",
"watched_zoom":"{[!pcfWhatchedZoom]}",
"welcome_sent":"{[!pcfWelcomeSent]}",
"readiness_score":"{[!pcfReadinessScore]}",
"satisfaction":"{[!pcfSatisfication]}",
"form_link":"{[!pcfFormLink]}",
"mentor_id":"{[!ownerid]}",
"mentor_name":"{[!owneridname]}",
"client_id":"{[!pcfaccountid]}",
"client_name":"{[!pcfaccountidname]}",
"client_phone":"{[!pcfaccountid_telephone1]}",
"client_phone2":"{[!pcfaccountid_telephone2]}",
"client_email":"{[!pcfaccountid_emailaddress1]}",
"client_idnumber":"{[!pcfaccountid_idnumber]}",
"client_city":"{[!pcfaccountid_billingcity]}",
"client_number":"{[!pcfaccountid_accountnumber]}",
"client_status":"{[!pcfaccountid_statuscode]}",
"client_gender":"{[!pcfaccountid_pcfGender]}",
"client_birthdate":"{[!pcfaccountid_pcfbirthdaydate]}",
"sale_id":"{[!pcfSale]}",
"sale_name":"{[!pcfSalename]}",
"sale_status":"{[!pcfSale_statuscode]}",
"sale_rep":"{[!pcfSale_owneridname]}",
"sale_signature_status":"{[!pcfSale_pcfSignatureStatus]}",
"sale_doc_link":"{[!pcfSale_pcfcfDocLink]}",
"sale_amount":"{[!pcfSale_pcfsystemfield106]}",
"sale_amount_after_discount":"{[!pcfSale_pcfsystemfield108]}",
"sale_weeks_gift":"{[!pcfSale_pcfWeeksGift]}",
"sale_whatsapp_group_chosen":"{[!pcfSale_pcfWhatsAppToRefname]}",
"sale_initial_weight":"{[!pcfSale_pcfQuestionNumber1]}",
"sale_target_weight":"{[!pcfSale_pcfQuestionNumber2]}",
"sale_dietary_select":"{[!pcfSale_pcfQuestionSelect1]}",
"sale_parent_name":"{[!pcfSale_pcfParentSalename]}",
"product_id":"{[!pcfProduct]}",
"product_name":"{[!pcfProductname]}",
"product_type":"{[!pcfProduct_pcfProductType]}",
"product_category":"{[!pcfProduct_categorycode]}",
"product_duration_weeks":"{[!pcfProduct_pcfDurationWeeks]}",
"product_billing_type":"{[!pcfProduct_pcfBillingType]}",
"product_price_incl_vat":"{[!pcfProduct_pcfItempriceIncludingVAT]}",
"order_id":"{[!pcfcrmorderid]}",
"order_name":"{[!pcfcrmorderidname]}",
"order_number":"{[!pcfcrmorderid_crmordernumber]}",
"order_status":"{[!pcfcrmorderid_statuscode]}",
"order_total":"{[!pcfcrmorderid_totalamount]}",
"whatsapp_group_id":"{[!pcfActualGroup]}",
"whatsapp_group_name":"{[!pcfActualGroupname]}",
"whatsapp_group_link":"{[!pcfActualGroup_pcfGroupLink]}",
"whatsapp_group_greenapi_id":"{[!pcfActualGroup_pcfGreenApiId]}",
"whatsapp_group_mentor":"{[!pcfActualGroup_owneridname]}",
"boost_cycle_id":"{[!pcfBoostLinked]}",
"boost_cycle_name":"{[!pcfBoostLinkedname]}",
"boost_cycle_start":"{[!pcfBoostLinked_pcfStartDate]}",
"boost_cycle_group_link":"{[!pcfBoostLinked_pcfEventLink]}",
"parent_process_id":"{[!pcfparentprocess]}",
"parent_process_name":"{[!pcfparentprocessname]}",
"external_id1":"{[!pcfExternalSoftwareID1]}",
"external_id2":"{[!pcfExternalSoftwareID2]}",
"dietary_prefs":"{[!pcfDietaryPrefs]}",
"intake_notes":"{[!pcfIntakeNotes]}",
"form_qa":"{[!pcfFormQA]}",
"satisfaction_explanation":"{[!pcfSatisficationExplaination]}"
}
```

---

## 🔴 תלות ארכיטקטונית קריטית — `pcfBoostLinked`

```
"boost_cycle_id"        : {[!pcfBoostLinked]}
"boost_cycle_name"      : {[!pcfBoostLinkedname]}
"boost_cycle_start"     : {[!pcfBoostLinked_pcfStartDate]}      ← שורה 85 בפיילוד
"boost_cycle_group_link": {[!pcfBoostLinked_pcfEventLink]}
```

**`boost_cycle_start` ו-`boost_cycle_group_link` מתמלאים רק אם מולא `pcfBoostLinked` על תהליך הליווי.**
ריק שם = **ריק בפיילוד = בוסטית מקבלת הודעת Welcome בלי תאריך התחלה ובלי לינק לקבוצה.** ההודעה תצא, לא תיפול, ותיראה שבורה.

👉 **תרחיש התשלום שיוצר את הליווי חייב לקשר את המחזור ברגע היצירה.** זהו סעיף בחוזה של A2 (התרחיש המוקפא) שיש לוודא כשישוחרר.
👉 **מסלול כתיבה נוסף:** בעת צירוף לקבוצת בוסט, שאילתה על 1051 לפי הלקוחה → כתיבת **`1051.pcfBoostLinked` = GUID המחזור (1007)**. **לא קיים ליווי → דלג בלי שגיאה** (לא ליפול, לא ליצור). `[chat_20]`
`[מקור: chat_19, chat_20]`

---

## 🔴 חוזה מינימלי מחייב — יצירת רשומת 1051

מתוך 11 שדות החובה באובייקט 1051, **6 שדות חייבים להגיע מהאוטומציה** בכל יצירה:

| שדה | תיאור |
|---|---|
| `name` | שם תהליך הליווי |
| `pcfStatus` | סטטוס (`2` = "ליווי בתהליך") |
| `pcfaccountid` | לקוחה |
| `pcfProduct` | מוצר |
| `ownerid` | מדריכה/מנטורית |
| `pcfStartDate` | תאריך התחלה |

⚠️ **סיכון כשל מתועד — `ownerid`:** השדה **חובה**, אך המנטורית נבחרת **ידנית ע"י נציג המכירות**. **נציג ששכח לבחור ⇒ יצירת רשומת הליווי תיכשל.**
התלות שפותרת: **חסר במוצר (14) שדה "מנטורית ברירת מחדל"**. בלעדיו אין fallback.
בעלים: **מייק** (מימוש השדה) / **רויטל** (הכרעה מי מנטורית ברירת המחדל פר-מוצר).
`[מקור: chat_22]`

### `pcfEstimatedEndDate` — מחושב חיצונית

**אינו שדה חובה — וטוב שכך**, כי הוא מחושב מחוץ לפיירברי:

```
pcfEstimatedEndDate = addDays( parseDate(pcfStartDate), pcfDurationWeeks * 7 )
```

שלושה סייגים:
1. החישוב מתבצע **פעם אחת בלבד, ביצירה**.
2. הוא רץ **ב-Make/n8n בלבד** — לא באוטומציה הפנימית.
3. **מוצר ללא `pcfDurationWeeks` (מנויים) ⇒ תאריך סיום ריק.** זה תקין ומכוון, לא באג.
`[מקור: chat_22]`

---

## ⚠️ זוגות שדות כפולים ב-1051 — סכנת פיצול דאטה

לפני כתיבה חזרה ל-1051, **לוודא לאיזה מהזוג כותבים.** כתיבה לאחד וקריאה מהשני = דאטה שנעלמת בשקט.

| זוג | הערה |
|---|---|
| `pcfRMR` / `pcfsystemfield101` | RMR מול נוסחת RMR |
| `pcfLastWeighDate` / `pcfWeighingDate` | שני תאריכי שקילה |
| `pcfCurrentWeight` / `pcfWeeklyWeight` | שני משקלים "נוכחיים" |
| `pcfCurrentProgram` / `pcfsystemfield102` | `pcfsystemfield102` = **זומבי ידוע**, הושמט מהפיילוד בכוונה |

`[מקור: chat_22]`

---

## ⚠️ אובייקט 1051 גדל — הפיילוד עלול להיות חסר

~~אובייקט 1051 = 31 שדות~~ ⛔ מיושן (הוחלף 03/08/2026)
**מצב עדכני: 1051 מונה 57 שדות. 26 מהם לא אופיינו מעולם**, בהם `pcfInitialWeight`, `pcfTargetWeight`, `pcfCurrentWeek`, `pcfWeighCount`, `pcfCurrentProgram`.

**נגזרת:** ייתכן שהפיילוד חסר שדות רלוונטיים — או להפך, שהוא מכיל שדות שאיש לא מתכוון למלא. **לפני הפעלה בפרודקשן: לעבור על 26 השדות הלא-מאופיינים ולהכריע פר-שדה.** בעלים: **מייק** + **אליאל**.
`[מקור: chat_25]`

**`pcfContinuationStatus`** ("סטטוס המשך", picklist בן 4 ערכים) — שדה שנוסף ל-1051 ב-chat_18. **החלטה: נכלל בפיילוד** תחת `"continuation_status"`. ✅ סגור. `[chat_18]`

---

## מפת ניתוב ב-Make — `message_type` וה-Switch של מודול 24

הפיילוד נכנס לתרחיש **"Welcome - General Message - CloudChat"**.

### מודול 24 — `util:Switcher`, **regex = Yes**

**Input:**
```
{{if(1.message_type = "welcome"; 1.product_name; 1.message_type)}}
```
כלומר: כשהמעטפת מסמנת `message_type = "welcome"` — הניתוב מתבצע לפי **שם המוצר**; אחרת לפי `message_type` עצמו.

**התאמות ה-regex:**

| Pattern | יעד | הערה |
|---|---|---|
| `^תוכנית ליווי` | flow **ליווי** | תופס את כל 7 התוכניות הקיימות **וגם תוכניות עתידיות** — זו הסיבה שאין `$` בסוף |
| `^סדנה בוסט$` | flow **בוסט** | התאמה מדויקת |
| *(Else — ריק)* | — | **תוכניות המשך והרצאת אורח לא מקבלות כלום. בכוונה.** |

**מודול 2 (SetVariables) שאחריו:**
- `flow_ns = {{ifempty(24.output; 1.flow_ns)}}` — תאימות לאחור
- `param_1 = {{1.mentor_name}}`
- `param_2/3/4` — עם `if` על `product_name = "סדנה בוסט"` (מחזור/קבוצה · לינק · תאריך התחלה)
- `param_5`–`param_10` — **ריקים**

**פילטר על מודול 22 (`send-sub-flow`):** `flow_ns` Exists.

**החלטות שהובילו לעיצוב הזה:**
- ❌ נדחתה הצעה לאוטומציות נפרדות פר-מוצר.
- ❌ נדחה Switch על picklist קטגוריה — כי "הרצאת אורח" מסווגת גם היא כ"סדנה".
- ✅ **נבחר regex על שם המוצר — לבקשת אליאל.**

⚠️ **גוצ'ת ממשק:** ה-Switch של Make ב-**No-regex** הוא **Equal מדויק**, לא Contains. עברית ב-Pattern תקינה; אבל ב-**regex חובה להקליד `^` ראשון** — תצוגת ה-RTL מטעה ונראה כאילו הוא בסוף.

`[מקור: chat_19 · 27/07/2026 · מתועד גם ב-claude/SESSION_2026-07-27_הודעות_קלאודצ'אט.md §1]`

### מיפוי מסלול ↔ params

| מסלול | `data_params` שמוזנים |
|---|---|
| **ליווי** | `data_param1` / `data_param2` / `data_param3` |
| **בוסט** | `data_param2` / `data_param3` / `data_param4` |
| **else** | — |

**חוזה ה-params:** `params 1–4` נושאים ערכים · **`params 5–10` חייבים להיות ריקים לחלוטין בכל מסלול.** אין דריסה = שאריות ישנות זולגות לקלאודצ'אט. באגים שנמצאו: `param_5` הכיל תאריך התחלה + מקף מילולי; `param_6`–`param_10` הכילו `1.paramX` — שדה שכבר לא קיים בפיילוד. **הניקוי הוגדר כמשימה ב-27/07 אך טרם אושר כבוצע.** בעלים: **אליאל**.

נוסחת `param_4` במודול 2 (verbatim):
```
{{if(1.product_name = "סדנה בוסט"; 1.boost_cycle_start; emptystring)}}
```
שדה הוובהוק הגולמי: `{{1.boost_cycle_start}}`

### ⚠️ אזהרה — "מודול 24" מופיע בשני תרחישים שונים

| תרחיש | מודול 24 = | מקור |
|---|---|---|
| **Welcome - General Message - CloudChat** | **`util:Switcher` עם regex** — הליבה של הניתוב, כמתואר לעיל | chat_19 · 27/07/2026 |
| **Meetings Reminders — חיפוש פגישות למחר** | **"Get Contact Info"** — **מיותר**, ה-`user_id` ל-Send Flow נלקח ישירות מתשובת מודול 22. מועמד למחיקה | chat_10 · 27/07/2026 |

⛔ **אין למחוק "מודול 24" בלי לוודא באיזה תרחיש מדובר.** מספור המודולים ב-Make הוא פר-תרחיש. מחיקה בתרחיש ה-Welcome תשבור את כל הניתוב.
הכרעה על מחיקת מודול 24 ב-Meetings Reminders: **מייק**.

---

## הערות

- הטריגר "נוצרה" = תמונת רגע היצירה. שדות שמתמלאים אחר כך (קבוצה, הזמנה, משקלים) יגיעו ריקים.
- הושמטו בכוונה: `deleted*`, `modified*`, `pcfSystemSettings`, `pcfsystemfield102` (זומבי), `pcfBusinessUnit`.
- שדות `*_id` מחזירים שמות (מגבלת המנוע) — הושארו כי השם עצמו שימושי; ה-GUID מגיע מהחיפוש היחיד ב-Make.
- **rate limit פיירברי: 100 קריאות/דקה** → בלולאות ברודקאסט להוסיף Sleep 2 שניות בין לקוחות.

> **הערת אבטחה:** טוקן ה-API של פיירברי ⚠️ נחשף בצ'אט — לרוטציה. הוא מסתובב גם בקוד טופס הליד, גם ב-blueprints של Make וגם בשיחות. **אין לרשום ערכי טוקן במסמך זה.** הרוטציה (משימה E2) מבוצעת **רק אחרי סיום הטסטים** ובחלון מתואם עם טל, אחרת נשברים כל חיבורי Make באמצע עבודה.
