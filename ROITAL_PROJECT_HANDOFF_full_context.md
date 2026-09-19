# Roital Yaish — Full Project Handoff (Claude-to-Claude Context)

> **עודכן 03/08/2026 — סקירת 26 שיחות הפרויקט.**

> 📜 **מסמך היסטורי — לא מקור אמת עדכני.**
> מסמך זה נכתב ב-21/07/2026 והוא **הועבר ברובו** ע"י **חבילת 00–09 + `README.md`** שנוצרה ב-**26/07/2026**.
> **מקור האמת התקף היום:** חבילת **00–09** + **סקירת 03/08/2026** (26 שיחות הפרויקט).
> **סדר הקדימות המלא מופיע ב-`README.md`** — קרא אותו לפני שאתה מסתמך על משהו כאן.
> **המסמך נשמר במכוון** — הוא עדיין ההסבר הרציף היחיד של מודל העסק, הנוסחאות, ולקחי Fireberry/Make. פרקים 5 ו-4 (הנוסחאות והגוצ'ות) עדיין תקפים ברובם.
> כל טענה שתוקנה מסומנת בגוף המסמך: `~~טענה ישנה~~ ⛔ מיושן (הוחלף 03/08/2026)`.

| # | מה שונה | מקור |
|---|---|---|
| 1 | נוסף באנר "מסמך היסטורי" + הפניה ל-`README.md` לסדר הקדימות | chat_26 |
| 2 | תוקן: "כל הלוגיקה ב-Make" ⛔ — הכלל היום: פיתוח חדש ב-n8n, Make ידני ע"י מייק בלבד | chat_21, chat_26, chat_27 |
| 3 | נוספו החלטות D1 (`pcfSignatureStatus` רילייבל ערך `1`) ו-D2 (`statuscode`=7 נשאר, אין כתיבה) | chat_18 |
| 4 | עודכנו ספירות שדות מיושנות (`1`, `4`, `6`, `14`, `1051`, `1069`, `1007`) לפי אודיט 26/07 | chat_18, chat_22 |
| 5 | תוקן: שדות הקיבולת של אובייקט הקבוצה כבר **קיימים** — לא "to add" | HANDOFF שלב 2 |
| 6 | תוקן: `pcfLeadLevel` **בוטל** — אינו ברצועה העליונה של `4` | chat_07 |
| 7 | תוקן: GreenAPI **אינו** ערוץ ההודעות. CloudChat = הודעות · GreenAPI = ניהול קבוצות בלבד | chat_13 |
| 8 | ⚠️ סתירה פתוחה: יום השקילה — חמישי מול ראשון 09:00 | chat_08, chat_10 |
| 9 | ⚠️ סתירה פתוחה: `pcfGroupid` מול `pcfGreenApiId` באובייקט הקבוצה | chat_20, chat_22 |
| 10 | ⚠️ סתירה פתוחה: `POST /api/query` מול `POST /api/v3/query` + שתי מגבלות rate limit | chat_20, chat_21, chat_26 |
| 11 | ⚠️ סתירה פתוחה: 22 מול 74 מחזורי בוסט (`1007`) | chat_03, chat_08 |
| 12 | ⚠️ סתירה פתוחה: גורל אובייקט `1005` — שלוש עמדות | chat_20, chat_25, chat_27 |
| 13 | **נוסף פרק 10 — מרשם רוטציית סודות: חמישה טוקנים, אף אחד לא אומת כסובב** | chat_20–27 |
| 14 | נוסף סייג תזמון לרוטציה: שוברת את כל חיבורי Make — לתאם עם טל אחרי סיום הטסטים | chat_22, chat_19 |
| 15 | נוסף צ'קליסט תלת-שלבי לאחר הרוטציה (Make · n8n · `1036.pcfPowerlinkToken`) | chat_21, chat_26 |
| 16 | נוסף: מפתח ה-SSH שנמסר הוא **ציבורי** — לא סוד, לא נספר ברוטציה | chat_21 |
| 17 | נוסף מיפוי בעלי תפקידים: עודד (סליקה/קבוצות/דומיין), רחלי (מכירות), טל, שחר | chat_08 |
| 18 | נוסף: דיאטניות = אנשי קשר (`2`), קבלניות — לא משתמשי מערכת (`9`) | chat_07 |
| 19 | נוספו חסמים תפעוליים: מנטוריות ללא גישה (`ownerid` ריק) · משתמש תזונאית לא הוקם | chat_02, chat_08 |
| 20 | נוסף: מוצר ברירת המחדל ב-`1036` (`name="1"`, `pcfproduct`) ממתין להחלטת רויטל | chat_05 |
| 21 | נוספו שינויי `1059` (ערך `5`, `pcfScheduledSendAt`) + שדות CloudChat `diet_menu_name` / `diet_menu_link` | chat_13 |
| 22 | נוסף מצב `1060`: 14 רשומות ממתינות לייבוא · `pcfGreenApiId` ריק ⇒ WF-03 חסום | chat_14 |
| 23 | נוסף WF-16 לרשימת התוצרים — מאופיין, לא נבנה | chat_16 |
| 24 | נוסף תוצר `Roital objects fields v2` (XLSX, 21 גיליונות, 916+18+266) | chat_25 |
| 25 | נוסף: ClickUp `86c8zamc2` = מקור אמת לסטטוס (133 משימות / 23 קטגוריות) | chat_22 |
| 26 | נוסף מצב אשכולות: A ❄ מוקפא · G1 🟢 בתהליך · E3 נוסף | chat_27 |
| 27 | נוסף: 525 אירועים תקועים — אסור להדליק תרחיש לפני בדיקת תוכן התור | chat_22, chat_26 |
| 28 | נוסף מצב תשתית ההודעות: 3 צינורות בנויים, המסירה בפועל שבורה (ערוץ של טל) | chat_19 |

---

> **Purpose.** Self-contained master context so a future Claude instance can operate with zero prior knowledge. Written in English per the Claude-to-Claude artifact standard. Deliverables to Mike/Eliel are in Hebrew; this doc is internal.
> **Default identity in this project:** *Sensei (Roital)* — strategic orchestrator. Stay macro; Mike executes.

---

## 1. What this project is

Vitrue (implementation consultancy) is configuring a **Fireberry CRM** for client **Roital (Revital) Yaish**, who runs an online **women's weight-loss coaching business**. The Fireberry account is a **cloned Vitrue template** (region **eu2**). Customization is **subtractive / cosmetic / occasionally additive — never rebuild from zero.**

**People:**
- **Mike (מיכאל)** — the implementer. Builds everything manually in the Fireberry UI and in Make. **Does not read code. Limited terminal.** Prefers Hebrew, directness, concision. Pushes back on over-engineering. Claude gives him architecture + exact field values + step-by-step specs, not theory.
- **Eliel** — reviewer/approver. Receives Hebrew change-logs.
- **Roital / Oded** — client side. Know Fireberry well (years of use). Confirm business content and scope.

**🆕 מיפוי בעלי תפקידים מלא (הוסף 03/08/2026):**

| שם | תפקיד בפועל | למה זה משנה |
|---|---|---|
| **מייק (מיכאל)** | המיישם. בעלים של כל שינוי בחשבון החי ובעל ההכרעה | כל סתירה פתוחה נסגרת אצלו |
| **אליאל** | מאשר/סוקר. מקבל change-log בעברית | **אישור מחיקה הוא פר-שדה, לא גורף** |
| **רויטל** | הלקוחה. מחזיקה תוכן עסקי והכרעות מוצר | חוסמת: קיבולת קבוצות, מוצר ברירת מחדל |
| **עודד** | **מחזיק הסליקה, קבוצות ה-WhatsApp והדומיין** | חובה בפגישת ההצגה; חוסם לינקי קבוצות |
| **רחלי** | מכירות | רצויה בפגישת ההצגה — היא המשתמשת בפועל |
| **טל** | בונה במקביל ב-Make / ערוץ המסירה | **רוטציית טוקנים תשבור לו דברים — חובה לתאם** |
| **שחר וינברג** | יוצר המשימות ב-ClickUp | מקור ציר הזמן והמשימות |

**נוכחים נדרשים בפגישת ההצגה:** רויטל **ועודד** — חובה. רצוי: מנטורית + רחלי.

**Hard constraints (non-negotiable):**
- **Max 50 Fireberry internal automations.** Essentially all used. → ~~All logic runs in Make (external). Do NOT build Fireberry internal automations.~~ ⛔ **מיושן (הוחלף 03/08/2026)**
  🆕 **הכלל התקף:** **פיתוח חדש = n8n. תחזוקת קיים = Make, ידנית, ע"י מייק בלבד. קלוד לעולם לא כותב ל-Make דרך API.** האיסור על אוטומציות פנימיות בפיירברי **נשאר בתוקף** (תקרת 50).
  ⚠️ בפועל המצב מעורב: WF-08 מתועד כ-n8n אך מומש ב-Make; WF-16/WF-17 ב-n8n; קליטת לידים וחתימות ב-Make. אין קריטריון מוצהר מתי בונים איפה — ראה פרק 12.
  🆕 **לוגיקת מסך = client-side JS בתוך פיירברי** (הכרעת מייק, chat_12): "חיפוש המוצרים, החתימה ובניית הקישור — הכל ישירות בקוד ב-JS, בלי לצאת החוצה." n8n/Make = אורקסטרציה ואינטגרציות בלבד.
- **Do NOT touch Make via Claude Code.** Make is built manually by Mike. ✅ **הכלל אושרר מחדש** (chat_04, chat_05) — קלוד סירב מיוזמתו וניתב תיקון לצד פיירברי.
- **Do NOT trigger a Fireberry clone via API** (paid, manual).
- **`template_snapshot.json`** (`/mnt/project/`) = structural ground truth. **Field validation rules (mandatory/readonly/default/max_length) are NOT in the snapshot — ask Mike.**
- **Field economy:** Account = ~130 fields, Opportunity = ~123 — near the plan cap. **Reuse relabeled generic placeholders; avoid new fields on these two.**
  🆕 **ספירות מעודכנות (אודיט 26/07/2026):** Account `1` = **131** · Opportunity `4` = **130** · Product `14` = **37** · ליווי `1051` = **57** · פגישה `6` = **41** · שקילה `1069` = **21** · מחזור `1007` = **36** · קבוצת WhatsApp `1068` = **21** · הקצאת תפריט `1059` = **23–26** · קטלוג תפריט `1060` = **13**.
- **No destructive delete** of fields/objects without explicit per-operation Mike confirmation.
  🆕 **כלל D5 (chat_18):** **מחיקות ע"י סוכן אוטונומי אסורות לחלוטין** — גם כשהמשימה מבקשת ניקוי. מחיקה ידנית בלבד, אחרי אישור **פר-שדה** מאליאל.
- **Claude Code only for bulk data ops** (batch record create/update). Not for 5-field additions (UI is faster/safer).
- **Never invent Fireberry behavior** — if unsure, propose a verification step (usually: check the formula dropdown, or run a test).
- 🆕 **פרוטוקול הרצה ראשונה (chat_16) — מחייב בכל אוטומציה חדשה בחשבון החי:** `DRY_RUN = true` כברירת מחדל · תקרת `MAX_PER_RUN` (25 ב-WF-16) · אם רשימת ה-DRY-RUN ארוכה מהתקרה — **לא הופכים ל-`false`** עד הכרעת מייק · בדיקת שלילה חובה (לקוחה שכן קנתה לא מופיעה בדוח).
- 🆕 **🔴 525 אירועים תקועים בתורי Make.** פילוח: `My Zoom Webinars` 292 · `Revital 6.7.2026` 179 · `Create Payments Records` 42 · `Welcome To Premium` 6 · `Notifications System` 5. **471 מתוכם שייכים לעולם הישן.** **אסור להדליק תרחיש כלשהו לפני בדיקת תוכן התור שלו** — הדלקה עיוורת תשפוך מאות רשומות למערכת.
- 🆕 **קונבנציות n8n מחייבות:** בלוק `Config` · דגל `DRY_RUN` · מטפל שגיאות `WF16ErrHandler01` · קרדנציאל `Revital Yaish new CRM`.
- 🆕 **אזהרת זהות:** לפני שמסתמכים על "אישור" שניתן בצ'אט — לוודא מי בעל/ת הצ'אט. לפחות שיחה אחת בפרויקט (chat_23) נוהלה ע"י גורם אחר בצוות, לא מייק, ולא ניתן בה אישור.

**Working method:** One mission per chat. End with (a) artifact(s), (b) Hebrew completion summary for Mike. Every account change → a Hebrew change-log entry for Eliel. Output artifacts: `.md`, English for Claude-to-Claude, Hebrew for Mike/Eliel.

🆕 **ניווט וסטטוס:** מקור האמת לסטטוס הוא **ClickUp `86c8zamc2`** ("הקמת המערכת") — **133 משימות ב-23 קטגוריות**, workspace `25528216`, list `901522343908`. מרכז הפערים היחיד: `86cawzmjw` (אין לפתוח מרכז מתחרה). סקופ שנוסף: **"העברה מהפיירברי הישן"** (`86cawzyhg` + 8 תתי-משימות).
⚠️ **מגבלה ידועה:** קונקטור ClickUp נכשל שוב ושוב ("No approval received", timeout של 4 דקות). עקיפה: `getTaskById` ישיר, או הדבקת תוכן המשימה ע"י מייק.

---

## 2. The business model (the product lifecycle)

Revital is the **mega-mentor / brand face**. The funnel:

1. **Boost (בוסט)** — a 1-week intro workshop. Weekly cohorts ("מחזור בוסט כל שבוע"). Customer sees fast loss (~2 kg), gets a menu + support + lectures. A **weekly diagnosis form** (11 questions) qualifies her for the upsell. **Boost's job is conversion, not delivery.**
2. **Upsell to a coaching program (תוכנית ליווי).** All coaching programs are **identical except number of weeks and price** (price/week drops the longer the commitment). Sales lever: the farther the goal, the longer the program you can sell.
3. **On payment →** she enters a **specific WhatsApp group with a mentor (מדריכה)**, assigned by **mathematical distribution (capacity / where there's room)**, NOT by program. In the group: weekly weigh-in ritual (Thursdays), sharing, support, content.
4. **Menu (תפריט)** — mostly a **small set of standard menus reused across many**, plus **personal menus** for special needs/allergies. Personal menus are made by a **dietitian (דיאטנית)** who is **paid extra per personal menu**; the customer pays nothing. "Medical file" model: tried menu → didn't work → try another → personal.
5. **End of program →** assess goal attainment; **re-sale conversation ~1–2 weeks before end.** Renewals produce "continuing customers."

**Weigh-in ritual:** ~~Thursdays~~ ⛔ **מיושן (הוחלף 03/08/2026)** — ראה ⚠️ סתירה פתוחה בפרק 12.1. Customers currently post weight in WhatsApp manually and a mentor logs it. Being automated via a **WhatsApp bot**.

🆕 **הדיאטניות = אנשי קשר (אובייקט `2`), קבלניות — לא משתמשי מערכת (`9`).** ה-lookup `pcfDietitian` ב-`1059` מצביע לאובייקט `2`. הסיבה: לא לשרוף רישיונות.

---

## 3. Data model — objects (as built/used this session)

### 3.1 תהליך ליווי — coaching process — `customobject1051` (THE SPINE)
Central record; one per coaching program instance per customer. One customer can have several over time (chained).
**Key links:** `pcfaccountid`→Account, `pcfSale`→Opportunity, `pcfProduct`→Product, `pcfparentprocess`→customobject1051 (self, "שם ליווי אב" — renewal/continuity chain), `pcfActualGroup`→קבוצה (NEW — actual WhatsApp group), `ownerid`→CrmUser ("יועץ"/mentor).
**Status:** `pcfStatus` picklist — **1**=בתהליך קליטה ושיוך, **2**=בתהליך ליווי (**ACTIVE**), 3=ליווי הסתיים בהצלחה, 4=בהקפאה, 5=בתהליך ביטול, 6=ליווי בוטל.
**Dates/config:** `pcfStartDate`, `pcfEstimatedEndDate`, `pcfWeeksNumber` (program length in weeks, copied at open).
**Weight dashboard:** `pcfInitialWeight` (baseline, from onboarding), `pcfCurrentWeight` (Make-stamped each weigh-in), `pcfTargetWeight`, `pcfTotalLoss` (native formula: initial − current, **positive = loss**), `pcfDistanceToTarget` (native formula), `pcfLastWeighDate`, `pcfLastWeighWeek`.
**Computed (native formulas):** `pcfCurrentWeek` = `DATEDIFFDAY(pcfStartDate, NOW())/7 + 1` (number, precision 0 — **no FLOOR**, see §5); `pcfAge` = `DATEDIFFDAY(pcfBirthdate, NOW())/365.25`; `pcfRMR` = Mifflin-St Jeor (see §4.2).
**Intake:** `pcfHeight`, `pcfBirthdate` (date, copied from Account by Make), `pcfReadinessScore`, `pcfIntakeNotes` (textArea — concatenated open answers), `pcfOnboardingDone` (date — anti-duplication lock), `pcfDietaryPrefs` (pending).
**Convention field:** `pcfCreatedByPersonOrSystem` picklist (**1**=אנושי, **2**=מערכת) — reused everywhere; Make-created records = 2.

🆕 **תוספות 03/08/2026 ל-`1051`:**
- **57 שדות בחשבון** מול 31 במיפוי — פער של 26.
- **11 שדות חובה**, מתוכם **6 שהאוטומציה חייבת לספק ביצירה:** `name` · `pcfStatus` · `pcfaccountid` · `pcfProduct` · `ownerid` · `pcfStartDate`. ⚠️ `ownerid` חובה אבל נבחר ידנית ע"י נציג המכירות ⇒ **נציג ששכח לבחור → יצירת הליווי תיכשל.** `pcfEstimatedEndDate` **אינו** חובה.
- שדה חדש: **`pcfContinuationStatus`** ("סטטוס המשך") — `1` בוצעה שיחה · `2` פולו-אפ · `3` בחרה לא להמשיך · `4` בחרה להמשיך.
- שדה קיים: **`pcfWhatchedZoom`** — `1` ראתה · `2` ראתה הקלטה · `3` לא ראתה.
- **רצועה עליונה מוצמדת:** `pcfStatus` · `pcfCurrentProgram` · `pcfCurrentWeek` · `pcfContinuationStatus` · `ownerid`.
- **זוגות כפולים לניקוי:** `pcfRMR`/`pcfsystemfield101` · `pcfLastWeighDate`/`pcfWeighingDate` · `pcfCurrentWeight`/`pcfWeeklyWeight` · `pcfCurrentProgram`/`pcfsystemfield102`.
- 🔒 **`pcfsystemfield102`** — כפילות של `pcfCurrentProgram` שנוצרה בטעות ב-20/07. אין דאטה בסיכון. **המחיקה עדיין ממתינה לאישור פר-שדה מאליאל.** ⚠️ `pcfsystemfield100` (מרחק מהיעד) ו-`101` (RMR) **תקינים — לא לגעת**.

### 3.2 שקילה — weigh-in log — `customobject1069` (Mike's new object)
One row per weigh-in. Rendered as a related-list ("log") inside the ליווי.
**Fields:** `name` (auto "{customer} — {date}"), `pcfaccountid`→Account (**primary anchor — enables continuous weight graph across programs**), `pcfFollowupProcess`→customobject1051, `ownerid` (mentor), `pcfWeight`, `pcfWeighDate` (DateTime), `pcfFeeling` (TextArea), `pcfPhoneEntered` (Telephone), `pcfWeightDelta` (vs previous, **positive = loss**), `pcfChangeFromStart` (vs initial, **positive = loss**), `pcfWeekIndex`, `pcfCreatedByPersonOrSystem`.
**Sign convention (LOCKED):** positive = loss, consistent across `pcfWeightDelta`, `pcfChangeFromStart`, and ליווי `pcfTotalLoss`.

🆕 **תוספות 03/08/2026 ל-`1069`:** האובייקט מונה כיום **21 שדות** (2 רשומות בלבד בפועל). נוספו: **`pcfMentorNotes`** (טקסט ארוך, "הערות מנטורית") ו-**`pcfcrmorderid`** (lookup → `13` הזמנה, "הזמנה - מקושר"). שניהם ✅ חיים ומאומתים.
🔴 **מלכודת קריטית:** `pcfCreatedByPersonOrSystem` **הפוך ב-`1069` בלבד** — כאן `1`=מערכת · `2`=אנושי. בכל שאר האובייקטים (`1051`, `1007`, `14`, `6`, `1059`, `1068`) — `1`=אנושי · `2`=מערכת. **על `1069` יש לכתוב `1` כדי לסמן "מערכת".** כתיבת `2` תסמן כל שקילה אוטומטית כידנית.

### 3.3 תפריט (catalog) + הקצאת תפריט (assignment) — menu model
Two objects (created this session). Catalog + assignment = the "medical file" pattern.
**Catalog (תפריט):** `name`, `pcfMenuType` (1=סטנדרטי, 2=אישי), `pcfDietaryCategory`, `pcfCalories`, `pcfMenuUrl` (url — **no file field type in Fireberry; use url or record attachment**), `pcfCreatedByPersonOrSystem`.
**Assignment (הקצאת תפריט):** `name`, `pcfMenu`→catalog, `pcfFollowupProcess`→customobject1051, `pcfaccountid`→Account, `pcfResult` (1=עבד, 2=עבד חלקית, 3=לא עבד, 4=מוקדם לדעת), `pcfMenuStatus` (בהכנה/נשלח/פעיל/הוחלף), `pcfSentDate`, `pcfValidFrom`/`pcfValidTo` (adherence period), `pcfDietitian`→**Contact** (dietitian = external payee, NOT CrmUser — no license burn), `pcfDietitianFee`/`pcfDietitianPaid`/`pcfDietitianPaidDate` (**FROZEN** — see §7), `pcfAllergiesNeeds`, `pcfNotes`, `pcfCreatedByPersonOrSystem`, `ownerid` ("אחראי/ת רשומה").
**PENDING migration:** 4 template fields (`pcfMenuType`, `pcfDietaryCategory`, `pcfCalories`, `pcfMenuUrl`) were duplicated on BOTH catalog and assignment. They belong on the catalog only → **delete from the assignment** (destructive → confirm per field).

🆕 **עדכוני 03/08/2026 למודל התפריטים:**
- **קטלוג התפריטים = אובייקט `1060`.** ⚠️ **הסכימה שאומתה מהחשבון החי** (`fields related (35).csv` + צילומי מסך, chat_14) **גוברת על ההגדרה שבמסמך זה.** `1060` = 13 שדות / 3 רשומות בחשבון.
- **מצב דאטה:** **14 רשומות תפריט ממתינות לייבוא ל-`1060`.**
- **הקצאת תפריט = אובייקט `1059`** — 23 שדות, כולם עם שם מערכת ותווית ייחודיים. ~~4 שדות כפולים ב-1059~~ ⛔ **מיושן** — הטענה נבדקה ונמצאה שגויה; ההפרש מול התיעוד הישן הוא 3 שדות מערכת שהייצוא לא מציג (`customobject1059id`, `deletedon`, `deletedby`).
- **שינויים שנוספו 27/07:** ערך picklist **`5` = "מוכן לשליחה"** ב-`pcfMenuStatus` · שדה חדש **`pcfScheduledSendAt`** (dateTime).
- 🔴 **זוג כפול קריטי ב-`1059`:** `pcfSentDate` מול `pcfMenuMsgSent` — **דגל "נשלח" מתפצל לשני שדות ⇒ סכנת כפל שליחה.** להכריע לפני הפעלת אוטומציית שליחת התפריט.
- **שדות משתמש חדשים בקלאודצ'אט:** `diet_menu_name` = `f201689v15923499` · `diet_menu_link` = `f201689v15923501`.
- ✅ `pcfDietitianPaid` (סטטוס) מול `pcfDietitianPaidDate` (תאריך) — **אינם כפילות**, שניהם נחוצים.

### 3.4 קבוצה — WhatsApp group (Mike's object, created 02/07)
Persistent, mentor-led, capacity-managed, cross-program. 🆕 **קוד האובייקט: `1068`.**
**Existing fields:** `name`, `ownerid` ("מנהל הקבוצה"/mentor), `pcfGroupLink` (url), `pcfGroupid` (GreenAPI group id).
~~**To add (capacity model — copy the pattern from מחזור קורס):** `pcfCapacity`, `pcfCurrentCount` (Make-maintained), `pcfAvailableSlots`, `pcfGroupStatus` (1=פעילה, 2=מלאה, 3=סגורה), `pcfGroupPhoto` (url — for the welcome message).~~ ⛔ **מיושן (הוחלף 03/08/2026)**
🆕 **הסכמה כבר קיימת ומאומתת בחשבון:** `pcfCapacity` (Number) · `pcfCurrentCount` (Number) · **`pcfAvailableSlots` (Number, שדה נוסחה — מחשב את עצמו מ-`pcfCapacity` ו-`pcfCurrentCount`)** · `pcfGroupNumber` (Number) · `pcfGroupPhoto` (Url). סה"כ 21 שדות.
**Wiring:** Opportunity `pcfWhatsAppToRef` (INTENT — seller picks) → קבוצה; ליווי `pcfActualGroup` (ACTUAL — after she joins) → קבוצה ✅ **מאומת שמצביע נכון ל-`1068`**; Account `pcfWhatsAppReferans` (redundant → convenience "current group" via Make, or drop).

🆕 **מצב הדאטה (החוסם האמיתי — לא הסכמה):**
- **8 קבוצות קיימות** ("להתאהב בעצמך מחדש 1–8"), כולן בסטטוס פעילה.
- **קיבולת ריקה ב-6 מתוך 8.** לשתיים יש `999` ו-`99` — מספרי בדיקה.
- **מספר לקוחות רשומים = 0** בכל הקבוצות למעט אחת.
- **מדריכת הקבוצה = "ויטרו ראשי" בכולן** — אין שיוך מנטורית אמיתי, בניגוד ליחס החד-חד-ערכי שבאפיון.
- 🔒 **רויטל טרם מסרה את מספר הקיבולת** ("כמה לקוחות בקבוצה = מלא"). ללא זה `pcfAvailableSlots` חסר משמעות ואוטומציית התפוסה לא ניתנת להפעלה.
- 🔴 **`pcfGreenApiId` ריק ⇒ WF-03 חסום.**
- ⚠️ **סתירה פתוחה:** `pcfGroupid` מול `pcfGreenApiId` — ראה פרק 12.2.
- **זוג כפול נוסף:** `pcfCurrentCount` / `pcfGroupNumber`.

### 3.5 Opportunity — תהליך מכירה (type 4) — sales
Mature Vitrue sales object. **statuscode pipeline:** ליד חדש → לל"מ 1–5 → פולואפ → פגישת מכירה → ממתין לתשלום → עסקה נסגרה/הופסדה/בוטלה. ~~`pcfLeadLevel` (קפוא/קר/חם/רותח)~~ ⛔ **מיושן (הוחלף 03/08/2026)** — **`pcfLeadLevel` בוטל** ואינו חלק מהמודל התפעולי. full UTM, financials, demographics.
**Key links:** `pcfProduct`→Product, `pcfCourse`→customobject1007 (cohort), `pcfParentSale`→Opportunity (self, **dormant "לא בשימוש" → ACTIVATE** for boost→coaching→renewal chain), `pcfReregistration` (dormant → activate; marks renewals).
**Relabeled generic placeholders (already used):** משקל התחלתי/נוכחי/יעד, nutrition prefs — sit on generic `pcfQuestionNumber/Text/Select` fields (~35 available; **reuse these instead of new fields**).
`pcfWhatsAppToRef` = group-assignment intent.

🆕 **תוספות 03/08/2026 ל-`4`:**
- **130 שדות בחשבון** מול 123 במיפוי.
- **רצועה עליונה מוצמדת:** `statuscode` · `pcfdayspast` · `pcfFollowUpTime` · `ownerid` — **בלי `pcfLeadLevel`**.
- **החלטה D1:** `pcfSignatureStatus` — **ערך `1` עבר רילייבל מ-"נשלח" ל-"ממתין לחתימה".** **לא נוסף ערך `4`.** הערכים התקפים: `1`=ממתין לחתימה · `2`=נחתם · `3`=בוטל. הנימוק: ערך `4` היה יוצר שני ערכים למצב אחד ומחייב כל תרחיש Make לבדוק "1 או 4". אפס שינוי ב-Make, אפס דאטה שנשברת, פעולה הפיכה.
- 🔴 **`pcfBoostLinked` על `4` הוא שדה זומבי** — lookup לאובייקט **`1005`** (שהוחלט לנטרל). על `1051` אותו שם שדה מצביע נכון ל-`1007`. **השדה הנכון לשיוך מחזור על העסקה הוא `pcfCourse` → `1007`.**
- ⚠️ גורל `1005` עצמו — סתירה פתוחה, ראה פרק 12.5.

### 3.6 Account — לקוח (type 1) — customer 360
Mature. statuscode (ליד חדש → בתהליך מכירה → לקוח פעיל → לא פעיל → סגור). Financial rollups, `pcfsatisfaction`, demographics, `pcfbirthdaydate` (source for age/RMR copy). Related lists already surface Opportunity/orders/invoices/activities.
**Customer-page 360 = mostly LAYOUT work:** add ליווי, שקילה (Account-anchored → full cross-program weight journey), and menu-assignment related lists to the layout.

🆕 **תוספות 03/08/2026 ל-`1`:**
- **131 שדות** בחשבון (מול 129 במיפוי). מתוכם **2 שדות צהובים** (קיימים ולא אופיינו מעולם) ו-**44 שדות בסטטוס "בדיקה"** שדורשים הכרעה.
- **שדות ירושה להסתרה (עדיפות גבוהה):** `accountratingcode` · `industrycode` · `lostreason` · **כל שדות ה-UTM** · `pcfQuestionNumber*` / `pcfQuestionSelect*` הגנריים. הערכת קלוד: *"הניקוי כאן שווה יותר מבכל אובייקט אחר."*
- ⚠️ **פתוח:** רשימת "מותר להסתיר" **פר-שדה** לא הופקה — קלוד הציע, **מייק לא אישר**. בעלים: מייק.
- **זו התחנה הבאה** בסדר העבודה של שכבת השדות.

🆕 **סדר עבודה מחייב לשכבת השדות (chat_25):**
`1` לקוחות → `4` תהליכי מכירה → `1051` תהליכי ליווי → `14` מוצרים → `1007` מחזור → הפיננסי (`13` / `1039` / `1018` / `1035`) → התפעולי.
**מתודולוגיה פר-אובייקט:** קלוד מביא 4 סוגי ממצא — (1) שדות צהובים · (2) כפילויות ושדות מתים · (3) lookups מפוקפקים · (4) ערכי picklist שלא מתיישבים עם המודל. **מייק מכריע → קלוד מייצר רשימת PUT-ים + change-log בעברית לאליאל.** אין ביצוע לפני הכרעה.

### 3.7 Supporting
- **`customobject1007` — מחזור קורס (cohort, ~34 fields):** has a **built-in capacity model** — ~~`pcfRegistrationQuota` / `pcfRegistration` / `pcfRegistrationAvailability`~~ ⛔ **מיושן (הוחלף 03/08/2026)** — השמות שאומתו בחשבון החי הם **`pcfRegistration` / `pcfAvailability` / `pcfQuota`**, ולצידם `pcfBoostCount` / `pcfOpertuintyCount` (זוג כפול 🟡). plus `pcfStartDate`/`pcfEndDate`, `pcfProductId`. **Used for boost weekly cohorts.** Opportunity links via `pcfCourse`.
  🆕 **`1007` = 36 שדות.** נוסף לאחרונה: **`pcfwhatspgrouprelated`** ("קבוצת בוסט WhatsApp - מקושר") — ככל הנראה זהו ה-lookup `1007`→`1068` שהיה שנוי במחלוקת.
  🆕 **`pcfStatus` על `1007`:** `1`=פתוח להרשמה · `3`=קורס פעיל · `4`=הסתיים · `5`=התבטל · `6`=ממתין לפתיחה. ⚠️ **הסטטוסים בדאטה החי הפוכים/שגויים — אסור לסנן לפיהם. סינון לפי תאריך בלבד.** נכון ל-26/07: **22 מחזורים עם `pcfEventLink` ריק** ו-**21 מחזורים עם סטטוס הפוך**.
  ⚠️ **ספירת המחזורים עצמה — סתירה פתוחה (22 מול 74).** ראה פרק 12.4.
  🟡 **`1007.pcfEventLink` (באג 2) — גורל לא מוכרע:** chat_20 סוגר כ"לא רלוונטי" אחרי המעבר ל-`1068`; chat_21 משאיר פתוח ומוציא מסקופ; chat_22 מונה כחוסם פעיל בבעלות **עודד** ("לינקי קבוצות WhatsApp"). **המלצה: לסגור** — מקור האמת עבר ל-`1068.pcfGroupLink`.
- **Contact (type 2):** holds **dietitians** (external payees). ✅ **אושרר:** דיאטניות = **קבלניות**, מנוהלות כאנשי קשר, **לא כמשתמשי מערכת (`9`)**.
- **Product (type 14):** programs. `pcfDurationWeeks` = weeks per program ("28 שבועות" stored as number 28). Feeds ליווי end-date. 🆕 **37 שדות** בחשבון.
- **Activity — פגישה (type 6):** holds **sales Zoom meetings.** New fields go here: `pcfZoomLink` (url, **per-meeting — link varies**), `pcfZoomMsgSent`/`pcfZoomReminderDay`/`pcfZoomReminder30` (anti-duplication flags). Has native scheduled datetime.
  🆕 **`6` = 41 שדות.** נוסף: **`pcfArrivalConfirmation`** ("סטטוס אישור הגעה") — `1` אישרה · `2` לא אישרה · `3` לא ענתה. ✅ חי ומאומת.
  🆕 **החלטה D2:** ב-`statuscode` קיימים `6`=לא הופיע/ה ו-`7`=אישר/ה הגעה — מה שמערבב אישור מראש עם הגעה בפועל. **הערך `7` נשאר** (יש בו דאטה היסטורית), אבל **אף אוטומציה לא כותבת אליו יותר.** כל כתיבה של אישור הגעה עוברת ל-`pcfArrivalConfirmation` בלבד.
  🆕 **הפרדת צירים:** "אישור הגעה" = פגישות עם רויטל. צפייה בזום = `pcfWhatchedZoom` על `1051`, ציר נפרד.

🆕 **מפת קודי אובייקטים מאוחדת (אומתה על פני כל השיחות):**
`1`=לקוח · `2`=איש קשר · `4`=תהליך מכירה · `6`=פגישה · `9`=משתמש · `10`=משימה · `13`=הזמנה · `14`=מוצר · `1002`=רישום שיווקי · `1007`=מחזור בוסט · `1018`=תיעוד תשלום · `1030`=הרשמה לאירוע · `1032`=אירוע · `1036`=הגדרות · `1039`=תשלום · `1041`=מפגש · `1051`=תהליך ליווי · `1057`=חג ומועד · `1058`=רשימת מסמכים לחתימה · `1059`=הקצאת תפריט · `1060`=קטלוג תפריט · `1068`=קבוצת WhatsApp · `1069`=טופס שקילה.

🆕 **7 אובייקטים חיים ופעילים ללא גיליון אפיון — 225 שדות (chat_25):**

| אובייקט | שדות | רשומות |
|---|---|---|
| `1007` מחזור בוסט | 36 | 22 ⚠️ (ראה 12.4) |
| `13` הזמנה | 98 | 0 |
| `1059` הקצאת תפריט | 26 | 5 |
| `1068` קבוצת WhatsApp | 21 | 8 |
| `1069` טופס שקילה | 19 | 2 |
| `1060` קטלוג תפריט | 13 | 3 |
| `1058` רשימת מסמכים לחתימה | 12 | 9 |

🆕 **תוצאת אודיט השדות הרוחבי (26/07/2026):** **אפס שדות חובה חסרים** ב-10 האובייקטים שנבדקו. **4 שדות חסרים בסך הכול, כולם שדות שיקוף לא-חובה** שסומנו "בדיקה": `pcfEventId` על `1002` + 3 שיקופים מ-Opportunity על `1030`.
🆕 **חסר חוסם:** **אין דגל "הזמנה לוובינר נשלחה"** — לא על `1007` ולא על `1051`. בלעדיו אוטומציית יום 3 תשלח כל יום מחדש.

---

## 4. Formulas & computed values

### 4.1 End date (Make, NOT native)
`pcfEstimatedEndDate = pcfStartDate + (pcfWeeksNumber × 7 days)`. Computed **once at ליווי creation** (not weekly). **Native date-output formula FAILED** (Fireberry formula fields reject/mishandle DATE output). Also, weeks come from the Product (cross-object) which native can't pull. → **Make.** Use `addDays(parseDate(pcfStartDate), pcfWeeksNumber*7)`; empty weeks → empty (workshops/subscriptions).

### 4.2 Current week / Age / RMR (native, NUMBER output — works)
- `pcfCurrentWeek` = `DATEDIFFDAY(pcfStartDate, NOW()) / 7 + 1` — number field precision 0. **Live** (NOW re-evaluated on read — verified working).
- `pcfAge` = `DATEDIFFDAY(pcfBirthdate, NOW()) / 365.25` — number.
- `pcfRMR` (Mifflin-St Jeor, women) = `10*pcfCurrentWeight + 6.25*pcfHeight - 5*AGE - 161`. **Formula-on-formula is NOT allowed** in Fireberry → do NOT reference `pcfAge`; **inline** the age: `... - 5*(DATEDIFFDAY(pcfBirthdate, NOW())/365.25) - 161`. If native still refuses, compute RMR in the weigh-in Make scenario instead (it already writes current weight).

✅ **פרק 4 נבדק ב-03/08/2026 ולא נמצאה בו טעות.** הוא עדיין תקף במלואו.

---

## 5. Fireberry / Make / Tally — hard-won facts (READ BEFORE BUILDING)

**Fireberry native formulas:** NUMBER output works; **DATE output fails**. Confirmed functions in the dropdown: `DATEDIFFDAY`, `DATEADDDAY`, `DATEADDHOUR`, `NOW`, `IF`. **`FLOOR` is NOT available** — use number-field precision 0 to round, or look for `INT`/`TRUNC`/`ROUNDDOWN`. Formula output type must equal field type or it won't save. **Formula cannot reference another formula field** (inline the sub-expression). **Cross-object references don't work** (compute in Make).
**Fireberry picklist filtering:** filter by the **numeric value**, not the Hebrew label (e.g. active ליווי = `pcfStatus = 2`).
**PowerLink query (plquery):** endpoint semantics — a lookup field returns both `pcfX` (the **id**) and `pcfXname` (the **display name**). **Match id-type fields (e.g. `accountid`, `opportunityid`) against the `pcfX` id variant, never `pcfXname`.** Query results array is `Data` (Make UI mislabels it "DataArray"). Use explicit field names, never wildcards. `objecttype` codes: Account=1, Contact=2, Opportunity=4, Activity=6, Product=14, ליווי=1051, cohort=1007.
**Make arithmetic:** must be a **single `{{ }}` expression** — `{{a}}-{{b}}` produces the STRING "a-b"; use `{{a - b}}`. Wrap form values in `parseNumber(...)` (Tally/bot send text). ISO dates: `parseDate(x)` parses ISO natively (drop the format string). Read a field's OLD value BEFORE overwriting it (weekly delta reads `pcfCurrentWeight` before the update stamps the new one).
**Tally:** hidden fields prefilled via URL query params (`?key=value`, case-sensitive); native Make app + webhooks; RTL supported. **A group-broadcast form cannot carry a per-person id** (all recipients share one link) → the weekly weigh-in matches by **phone**. **A per-person form (onboarding) CAN carry `process_id`** (gold anchor).
**No file field type in Fireberry** — menus/booklets/photos are **record attachments or `url` fields**.
~~**GreenAPI** sends WhatsApp text, images, PDFs — used for the message automations.~~ ⛔ **מיושן (הוחלף 03/08/2026)**
🆕 **הכרעת ערוצים:** **CloudChat = שליחת הודעות ללקוחות. GreenAPI = ניהול קבוצות בלבד** (`getContacts`, `getGroupData`, יצירת קבוצה, נעילה). שני שימושים שונים לחלוטין.
🆕 **כלל אבטחה קשיח:** אם ייבחר GreenAPI ישיר כערוץ שליחה — **הטוקן נכנס ל-URL של הצומת ⇒ נכנס ל-export של ה-workflow** ⇒ **אסור לשלוח את ה-JSON בצ'אט או בוואטסאפ.**

🆕 **גוצ'ות Fireberry UI (נלמדו 26/07):**
- **החיפוש ב-Object Studio לא אמין** — מחזיר "לא נמצאו רשומות" גם לשדות קיימים. **הדרך שעובדת:** ניקוי החיפוש → מיון לפי "שם מערכת" → גלילה ידנית.
- **נתיב עריכת לייאאוט:** מתוך **רשומה** (לא מ-Object Studio) ← ⋮ ← עריכת עמוד ← לחיצה על כותרת המקטע ← "+ הוספת שדה" ← שמור.
- **בהוספת lookup:** לחיצה על החץ `‹` נכנסת לשדות של האובייקט המקושר, **לא** מוסיפה את השדה. השדה נוסף בלחיצה על השורה.
- **"תיבת טקסט"** (אייקון כתום) = טקסט ארוך/TextArea · **"טקסט"** (אייקון כחול Aa) = שורה אחת. השמות מטעים.
- **יצירת lookup ב-UI בטוחה יותר מ-API** — בוחרים את האובייקט כסוג השדה, אין `relatedObjectType` לנחש.
- **ייצוא CSV של שדות אובייקט לא כולל `<obj>id`, `deletedon`, `deletedby`** — הפרש קבוע של 3 מול ספירת התיעוד.

🆕 **תשתית n8n (chat_17, chat_21):** Host `srv964196.hstgr.cloud` · IPv4 `72.60.34.206` · Port `22` · User `root` · n8n רץ ב-Docker · מפתח SSH קיים בשם **`claude-code-n8n-dedupe`** · skill `n8n-hostinger`.
⚠️ **`n8n import:workflow` לא מייבא credentials** — חיבור ה-credential ידני בממשק, תמיד.
💡 המלצה: משתמש `n8nops` בקבוצת `docker` במקום `root`.
📌 החוסם "אין SSH" שהופיע בשיחות 13/15/16 **נפתר** — הפרטים היו קיימים; הבעיה הייתה **העברת ידע**, לא היעדר גישה.

🆕 **GreenAPI של רויטל:** `idInstance` שנמסר = `710701674604` ⚠️ **לא אומת** (מייק מסר "שם Instance", לא idInstance). `apiUrl` לא ודאי — לנסות גם `https://api.green-api.com` וגם `https://7107.api.greenapi.com`. **המספר המחובר הוא אדמין בכל קבוצות הבוסט** (אישור מייק). **אימות ה-`idInstance` וה-`apiUrl` הוא תנאי פתיחה לכל ביצוע.**

---

## 6. Make scenarios

### 6.1 Weekly weigh-in receive (built; being migrated to bot)
**Source:** originally Tally; migrating to a **WhatsApp bot** posting JSON to a custom webhook. **Bot JSON:** `{ "phone", "weight", "feeling", "weighed_at" (ISO 8601) }`. (Webhook: `https://hook.eu2.make.com/cj15un4dudvcsozp13y1433994xmq4t2`.)
**Flow:** Webhook → Parse phone → Query Account by phone (4 normalized variants: 0-prefix / E.164 / RFC3966) → Query ליווי (`pcfStatus=2`, sort `pcfStartDate` DESC, limit 1) → **filters** ("customer exists", "ליווי exists") → Set Variables → **Create שקילה** (compute `pcfWeightDelta` = prev − new; `pcfChangeFromStart` = initial − new; `pcfWeekIndex`; all positive=loss; `pcfCreatedByPersonOrSystem=2`) → **Update ליווי** (`pcfCurrentWeight`, `pcfLastWeighDate` raw, `pcfLastWeighWeek`; totalLoss/distance are native). **Gotchas fixed:** single-expression arithmetic + parseNumber; read current weight before overwrite; feeling must be mapped (was dropped once).
🔴 **תיקון קריטי:** `pcfCreatedByPersonOrSystem=2` **שגוי עבור `1069`** — שם `1`=מערכת. ראה 3.2.
⚠️ **יום ההרצה של התרחיש — סתירה פתוחה.** ראה פרק 12.1.

### 6.2 Onboarding "Welcome" receive (IN PROGRESS)
**Tally form 5B5p6Z.** Hidden `process_id` = `customobject1051id` (gold anchor). **Flow (new-customer branch):** Webhook → Parse phone → If-else (new / continuing) → **[6] Query ליווי** by id (`customobject1051id = {{2.fields.process_id}}`) → **[8] Query Account** (`accountid = {{6.pcfaccountid}}`) → **Update ליווי** (`pcfInitialWeight`=current weight from form, `pcfTargetWeight`, `pcfHeight`, `pcfBirthdate`={{8.pcfbirthdaydate}}, `pcfReadinessScore`, `pcfIntakeNotes`=concatenated open answers, `pcfOnboardingDone`=now). Age & RMR compute natively afterward.
**IMPORTANT correction made this session:** the "find the sales process" step (Query Opportunity) was **REMOVED** — onboarding only needs to find the ליווי + the customer to write the baseline. (An optional "stamp onboarding-done on the sale" was dropped to reduce confusion; the earlier `opportunityid = {{6.pcfSalename}}` was also wrong — would have needed `pcfSale` id, not the name — but the whole module is gone.)
**Continuing-customer branch:** placeholder only, **not built.** Should mirror the new branch, shorter: current weight → `pcfInitialWeight` (FRESH baseline for the new process), updated target, "what worked" note. (Parent-process linkage is set at ליווי creation, not here.)
**Open field question:** where dietary prefs land (a ליווי field `pcfDietaryPrefs`, or straight to the first menu assignment).

### 6.3 WhatsApp message automations (blueprint; not built)
10 manual messages → **3 clusters, all Make + ~~GreenAPI~~ CloudChat, "poll + sent-flag" pattern** (scheduled poll of Fireberry filtered by trigger + empty sent-flag; send; stamp flag; zero Fireberry automations, zero double-sends):
1. **Zoom sales flow** (msgs 2–4): trigger = meeting scheduled (Activity). Event msg + day-before + 30-min reminders (timed). Dynamic: name, per-meeting `pcfZoomLink`, datetime.
2. **Onboarding welcome** (msgs 5–8): trigger = ליווי active. Dynamic: **group name + mentor from `pcfActualGroup`→קבוצה**, group photo. Static: booklet, recordings.
3. **Menu delivery** (msgs 9–11): trigger = הקצאת תפריט sent. Dynamic: menu PDF/image from assignment. Static: recipes.
**Static content** (booklet/recordings/recipes/group photos) must live where the team can edit — a small "message templates" object or a Make Data Store — **not hardcoded in Make.**

🆕 **מצב בפועל (03/08/2026):** ~~not built~~ ⛔ **מיושן** — **שלושת צינורות ההודעות (ליווי / בוסט / אורח שבועי) בנויים ומאומתים** בצד פיירברי → Make → קלאודצ'אט. ⚠️ **המסירה בפועל שבורה** ("Delivery failed") — הכשל הוא **בערוץ שבאחריות טל**, לא בצד הפיירברי/Make.

### 6.4 Future Make work
Renewal auto-creation (end −~10 days → renewal Opportunity, `pcfParentSale`, `pcfReregistration`); group auto-assignment by `pcfAvailableSlots`; boost diagnosis form receive (→ Opportunity + lead scoring).
🆕 **סייג:** כל פיתוח חדש כאן נבנה **ב-n8n**, לא ב-Make. ראה פרק 1.
🆕 **WF-16 (מסלול מת):** **מאופיין, לא נבנה.** היה חסום על SSH (נפתר) ועל תרחיש התשלום של הבוסט.
⚠️ **סתירת מספרי תרחישים:** `Main Leads CRM` מדווח כ-**9339860** מול **6600296**, עם **1452508** כריצה משווה מאוטומציה פנימית ("לא רכשו בוסט 5 ימים"). **ההשוואה בין הריצות אינה נקייה** — הן משני סנריו שונים. לאמת בממשק Make ולקבע מספר אחד.

---

## 7. Open decisions & pending items
- **Dietitian payment scope — FROZEN.** Fee fields exist on the assignment but the payment WORKFLOW (views/reminders) is NOT built. Awaiting Roital/Eliel: manage dietitian payables inside the CRM, or leave to accounting? Beyond Eliel's original spec.
- **Menu assignment cleanup:** delete the 4 duplicated template fields from the assignment (confirm per field).
- **Onboarding continuing-branch:** not built.
- **`pcfDietaryPrefs`:** create on ליווי, or route to menu assignment.
- **Sales chain:** activate `pcfParentSale` + `pcfReregistration` (add to layout, remove "לא בשימוש").
- ~~**Group capacity fields:** add the 4 to the קבוצה object~~ ⛔ **מיושן (הוחלף 03/08/2026)** — **השדות כבר קיימים.** מה שחסר הוא **הדאטה** (מספר הקיבולת מרויטל) ושיוך מנטוריות אמיתיות. wire the two existing WhatsApp lookups; `pcfActualGroup` ✅ קיים ומחובר.
- **Boost:** decided = REUSE (Product + Opportunity + מחזור קורס), no new object. Diagnosis-form receive scenario not built.
- **Customer-page 360:** add ליווי / weigh-in / menu related lists to the Account layout.

🆕 **פריטים פתוחים שנוספו 03/08/2026:**

| # | פריט | בעלים | חוסם |
|---|---|---|---|
| 1 | **מספר קיבולת הקבוצה** (`pcfCapacity`) — "כמה לקוחות = מלא" | **רויטל** | אוטומציית תפוסה 90% + שיוך אוטומטי |
| 2 | **אישור מחיקת `pcfsystemfield102`** — פר-שדה | **אליאל** | ניקוי בלבד |
| 3 | **שיוך מנטורית אמיתית ל-8 הקבוצות** (כרגע "ויטרו ראשי" בכולן) | רויטל / עודד | שיוך אוטומטי |
| 4 | **המנטוריות טרם קיבלו גישה למערכת** — כל `ownerid` ריק, וכל הערת פיד נכתבת על שם המשתמש המזין | רויטל / מייק | פיד, שיוך, דוחות פר-מנטורית |
| 5 | **משתמש התזונאית לא הוקם** (דרישה פתוחה מ-`02_TRANSCRIPT_DECISIONS` §8) | מייק | תהליך התפריטים האישיים |
| 6 | **מוצר ברירת המחדל ברשומת ההגדרות** — `1036`, `name="1"`, שדה `pcfproduct` | **רויטל** | קליטת לידים / יצירת עסקאות |
| 7 | **רשימת "מותר להסתיר" פר-שדה לאובייקט `1`** — קלוד הציע, מייק לא אישר | **מייק** | ניקוי אובייקט הלקוח |
| 8 | **`pcfGreenApiId` ריק** בכל רשומות `1068` | עודד / מייק | **WF-03 חסום** |
| 9 | **14 רשומות קטלוג תפריט ממתינות לייבוא** ל-`1060` | מייק | אוטומציית שליחת תפריטים |
| 10 | **דגל "הזמנה לוובינר נשלחה"** — לא קיים על `1007` ולא על `1051` | מייק | אוטומציית יום 3 תשלח כל יום מחדש |
| 11 | **525 האירועים התקועים** — בדיקת תוכן תור לפני כל הדלקה | **מייק** | **משימה מספר 1 בפרויקט** |
| 12 | **רוטציית 5 הטוקנים** (E2) — ראה פרק 10 | **מייק** | פרודקשן |

🆕 **מצב אשכולות (chat_27):**

| אשכול | תיאור | מצב |
|---|---|---|
| **A** | וובהוק Grow | ❄ **מוקפא** |
| **G1** | קליטת לידים | 🟢 **בתהליך** |
| **E2** | רוטציית טוקנים | 🔴 פתוח — ראה פרק 10 |
| **E3** | אימות וובהוק על 9 חוזי החתימה | 🆕 נוסף |

---

## 8. Tools & resources
Fireberry eu2 (`api.fireberry.com`, `tokenid` header, ~~`POST /api/query`~~ ⚠️ ראה פרק 12.3). Make eu2 (webhook-based). ~~GreenAPI (WhatsApp groups + messaging)~~ ⛔ **מיושן** → **CloudChat = הודעות · GreenAPI = ניהול קבוצות בלבד.** Tally (forms; onboarding = 5B5p6Z). Grow (payments; multipart/form-data, server-side). Tofsy (signatures — separate workstream). n8n on Hostinger VPS (ראה פרק 5). Snapshot: `/mnt/project/template_snapshot.json`. Outputs: `/mnt/user-data/outputs/`. Prior session artifacts (in outputs): weigh-in field spec, onboarding form spec, menu build guide, sales/boost/group build guide, WhatsApp automations blueprint, onboarding Make-scenario flow.

🆕 **תוצרים רשמיים שנוספו מאז:**
- **`Roital objects fields v2`** (XLSX) — **21 גיליונות · 916 שורות שדה קיימות בפועל · 18 שורות וירטואליות · 266 שדות שלא אופיינו.** **מחליף את קובץ האפיון המקורי.**
  **מקרא:** שורה **צהובה** = קיים בחשבון ולא אופיין מעולם · שורה **אפורה נטויה** = שיקוף או שדה ליצירה, לא פיזי · שורה **רגילה** = החלטת האפיון המקורית נשמרה במלואה כולל עמודה A.
- **חבילת 00–09 + `README.md`** — היורשת של המסמך הזה (26/07/2026).
- **`HANDOFF_שלב2_שדות_2026-07-26.md`** — מודל השדות המפורט.
- **ClickUp `86c8zamc2`** — מקור האמת לסטטוס.

---

## 9. How to work with Mike (operational reminders)
Hebrew, direct, concise. Give architecture + exact system names + step-by-step; not theory. He builds manually (UI + Make). Verify against the snapshot; never invent Fireberry behavior. When a native formula fails, ask for the dropdown contents + exact error rather than guessing again (a repeated pain point). Reuse placeholders over new fields on Account/Opportunity. Produce a Hebrew change-log for Eliel per account change. Sensei stays macro; end each mission with artifact + Hebrew summary.

🆕 **כלל הזהב לפגישת הצגה (chat_08):** **לא פותחים מסך ללא דאטה אמיתית.** הזמנות / תשלומים / אירועי וובינר = 0 רשומות ⇒ מצגת בלבד.
**סימון קבוע:** ✅ בנוי וחי (מראים) · ★ מסבירים בעל פה בלבד · ❓ הכרעה לאסוף.

---

## 10. 🔴 מרשם רוטציית סודות (נוסף 03/08/2026) — משימה E2

> **לעולם אין לרשום ערך של טוקן במסמך.** כל ערך שנחשף מסומן כאן בשם בלבד.

**חמישה מפתחות, לא שלושה. אף אחד מהם לא אומת כסובב.**

| # | הסוד | היכן נחשף | היקף הסיכון | סטטוס |
|---|---|---|---|---|
| 1 | **Fireberry `tokenid`** | ⚠️ נחשף בצ'אט — לרוטציה. הודבק ע"י מייק (chat_03, chat_10, chat_19), סומן שוב ב-chat_25 ו-chat_27. **מוטמע גם בתוך `Meetings_Reminders_FIXED_blueprint.json` (מודולים 1 ו-6)** ובקוד טופס הליד | קריאה/כתיבה מלאה על החשבון החי | 🔴 **לא סובב** |
| 2 | **Make API key** | ⚠️ נחשף בצ'אט — לרוטציה. הודבק בטקסט גלוי (26/07, chat_21) | **הגרוע ביותר** — גישה מלאה לחשבון Make (קריאה/כתיבה/מחיקה של תרחישים) **וכל הקונקשנים מאחוריו: Fireberry, Tofsy, GreenAPI, WhatsApp** | 🔴 **לא ידוע אם סובב** |
| 3 | **Tofsy `api_key`** | ⚠️ נחשף בצ'אט — לרוטציה. סומן כבר ב-`PROJECT_KNOWLEDGE_signature_system.md` §9, **פתוח מאז 07/2026** | מערכת החתימות | 🔴 **לא סובב** |
| 4 | **GreenAPI `apiTokenInstance`** | ⚠️ נחשף בצ'אט — לרוטציה. chat_20 | ניהול קבוצות WhatsApp של רויטל | 🔴 **לא סובב** |
| 5 | **CloudChat API key** | ⚠️ נחשף בצ'אט — לרוטציה. chat_13; **יושב כטקסט גלוי בבלו-פרינט של מודול 93** | שליחת כל ההודעות ללקוחות | 🔴 **לא סובב** |

**סודות נוספים שנחשפו ומצטרפים לרוטציה:** `pcfPowerlinkToken` (מתוך רשומת ההגדרות `1036`, chat_04) · מפתח ה-API של **n8n** (chat_03).

⚠️ **הבהרה — מה *לא* סוד:** מפתח ה-SSH שמייק שלח הוא ה**ציבורי** בלבד (`claude-code-n8n-dedupe`). **אינו סוד ואינו דורש רוטציה.** לא לספור אותו כטוקן.

### 10.1 ⏱️ תזמון — לא עכשיו

**רוטציה שוברת את כל חיבורי Make** עד שמעדכנים אותם. **אם טל בונה במקביל — דברים ייפלו לו בלי שיבין למה.**
**ההכרעה:** הרוטציה מבוצעת **רק אחרי סיום הטסטים**, בחלון מתואם **עם טל**.
**הנימוק שלא לדחות ללא הגבלה:** אחרי הרוטציה מעדכנים רק את ה-credential; ה-workflows עצמם לא מחזיקים את הטוקן ולכן לא יישברו. זו פעולה קצרה — אבל **לא "ניצחון מהיר"**, ואסור להריץ אותה כלאחר יד.

### 10.2 ✅ צ'קליסט תלת-שלבי אחרי הרוטציה

1. **Make** — לעדכן את החיבורים בקבוצת החיבורים **"Revital - New"**.
2. **n8n** — לעדכן את ה-credential **`Fireberry — tokenid`** (Header Auth). ה-workflows עצמם לא נוגעים בטוקן.
3. **Fireberry** — לעדכן את השדה **`pcfPowerlinkToken`** ברשומת ההגדרות (`1036`).

**מקומות שליפה של הטוקן (לבדיקה שכולם עודכנו):** (א) מודול HTTP בתרחיש "Weekly Guest Broadcast" ב-Make · (ב) Fireberry ← הגדרות ← API ← Token ID · (ג) משתנה הסביבה `FIREBERRY_TOKEN_ID` ב-MCP config של Claude Code · (ד) `Meetings_Reminders_FIXED_blueprint.json` — **קובץ הבלופרינט עצמו הוא נכס מזוהם** · (ה) קוד טופס הליד · (ו) בלו-פרינט מודול 93 (CloudChat).

**פעולות ביצוע ל-Make:** Make ← Profile ← API access ← מחיקה + יצירה מחדש ← שמירה ב-password manager ← **יידוע שחר ואליאל**.

### 10.3 דפוס נכון שכבר עובד — לחקות
בכפתור התשלום הידני **לא נחשף שום טוקן.** הארכיטקטורה מכוונת: **כל הקריאות עוברות דרך `/api/record/...` בסשן של המשתמש המחובר.** זהו **תקן הפרויקט לכל כפתור/ווידג'ט עתידי בפיירברי.**

---

## 11. אירועי אבטחה מתועדים (נוסף 03/08/2026)

| תאריך | אירוע | סטטוס טיפול |
|---|---|---|
| 26/07/2026 | **מפתח API של Make הודבק בצ'אט בטקסט גלוי** (chat_21). מקנה גישה מלאה לחשבון וכל הקונקשנים מאחוריו | 🔴 לא ידוע אם סובב. פעולות: מחיקה + יצירה מחדש · password manager · יידוע שחר ואליאל |
| 02/08/2026 | מפתח n8n + `tokenid` של Fireberry נחשפו (chat_03) | 🔴 פתוח |
| — | `pcfPowerlinkToken` נחשף (chat_04) | 🔴 פתוח |
| — | טוקן Fireberry מוטמע בתוך `Meetings_Reminders_FIXED_blueprint.json` | 🔴 **הקובץ הוא נכס מזוהם** |
| — | טוקן CloudChat גלוי בבלו-פרינט מודול 93 | 🔴 פתוח |
| — | GreenAPI `apiTokenInstance` נחשף (chat_20) | 🔴 פתוח |

**כלל מונע:** אם GreenAPI ייבחר כערוץ שליחה — הטוקן נכנס ל-URL של הצומת ⇒ ל-export של ה-workflow. **אסור לשלוח JSON של workflow בצ'אט או בוואטסאפ.**

---

## 12. ⚠️ סתירות פתוחות (נוסף 03/08/2026)

### 12.1 יום השקילה — חמישי מול ראשון
- **עמדה א' — יום חמישי.** מקור: המצגת שהוצגה ללקוחה + ציר הזמן של שחר וינברג (כל 6 השקילות בימי חמישי) + פרק 2 במסמך זה.
- **עמדה ב' — יום ראשון 09:00.** מקור: משימה 13.1 ב-ClickUp + **התרחיש שרץ בפועל**.
**בעלים: מייק.** **הסתירה מופיעה בארבעה נכסים** — `06_N8N_WORKFLOW_SPECS`, `04_LIVE_MAKE`, המצגת ללקוחה, ותוכנית דאטת ההדגמה. **חובה לעדכן את כולם באותה הכרעה.**

### 12.2 `pcfGroupid` מול `pcfGreenApiId` (`1068`)
- **עמדה א' (chat_20, 26/07):** `pcfGreenApiId` הוא הקנוני — אישור מייק ("הראשון").
- **עמדה ב' (chat_22):** מייק אמר "לא יודע — צריך לבדוק"; **מפרט WF-03 מפנה ל-`pcfGroupid`**.
**בעלים: מייק.** **בדיקה של 5 דקות:** לפתוח 2–3 מתוך 8 רשומות `1068` ולראות באיזה שדה יושב הפורמט `1203630xxxxx@g.us`. אחרי ההכרעה — לעדכן את WF-03, `03_LIVE_FIREBERRY.md` ו-`05_GAP_CHECKLIST.md`.

### 12.3 endpoint ו-rate limit של Fireberry
- **Endpoint:** `POST /api/v3/query` (chat_20, chat_17 — הוחלט למעבר בכל workflow חדש, **מותנה באימות בחשבון החי**) מול `POST /api/query` (chat_21, ופרק 8 במסמך זה).
- **Rate limit:** **100 בקשות/דקה לארגון** (chat_20, chat_21) מול **צינון של 10–15 דקות אחרי ~350 קריאות מטא-דאטה** (chat_26).
**בעלים: מייק.** להתייחס לשתי המגבלות כ**מגבלות נפרדות** עד לאימות. לתעד ב-`FIREBERRY_REST_PLAYBOOK.md`.

### 12.4 ספירת מחזורי הבוסט (`1007`) — 22 מול 74
- **עמדה א' — 22 מחזורים.** מקור: ספירת מלאי chat_08 (27–28/07/2026) + chat_16 + chat_25.
- **עמדה ב' — 74 מחזורים.** מקור: **אימות ישיר מול ה-API החי, chat_03, 02/08/2026** — וכולם מסתיימים ביום ראשון.
שתי הספירות רצו מול **אותו חשבון** בהפרש של שבוע.
**בעלים: מייק.** **אין לצטט אף אחד משני המספרים** עד ריצת ספירה אחת מכריעה (`GET` על `1007`).

### 12.5 גורל אובייקט `1005` — שלוש עמדות
- **chat_20 (26/07, 18:23–19:15Z):** `1005` הוא אובייקט ההרשמה — **יש להפעילו**; N6/N9 כותבים אליו.
- **chat_25:** מייק ענה "תשאיר מחזור בוסט" בתשובה לשאלה על `1005` — **דו-משמעי**; `1005` נשאר מחוץ ל-21 האובייקטים.
- **chat_27 (22–23/07):** `1005` **הופל** לטובת מודל one-to-many.
בנוסף: `4.pcfBoostLinked` הוא lookup ל-`1005` ⇒ **שדה זומבי**.
**בעלים: מייק.** 🔴 **להקפיא כל בנייה שנשענת על `1005` עד הכרעה חד-משמעית.**

### 12.6 הכרעת פלטפורמה — n8n מול Make
- **chat_26:** "אין תהליכים חדשים ב-Make, אבל מה שבנוי ועובד ב-Make נשאר."
- **chat_21:** היפוך אמצע-שיחה — כל אוטומציית הסטטוסים עוברת ל-**n8n**.
- **chat_20:** WF הצירוף לקבוצה נבנה ב-**n8n**.
- **chat_27:** כל העבודה בפועל נעשתה **ב-Make**.
**הניסוח המחייב שנקבע:** *"פיתוח חדש = n8n. תחזוקת קיים = Make, ידנית, ע"י מייק בלבד. קלוד לעולם לא כותב ל-Make דרך API."*
⚠️ **מה שעדיין חסר:** **קריטריון מוצהר** מתי בונים איפה, וטבלת "מה רץ איפה בפועל". **בעלים: מייק.**

### 12.7 מספר השלבים במשימת-העל `86c8zamc2`
**22 שלבים** (chat_02, 03/08) מול **20 שלבים** (chat_08, 27–28/07). לאמת מול ClickUp ולקבע מספר אחד בכל מקום שמצטט את המבנה. **בעלים: מייק.**

---

## 13. מצב החשבון החי — נקודת פתיחה לכל מי שממשיך

🔴 **נכון ל-26/07/2026, מצב החשבון החי הוא clean state תפעולי** — למעט שני שינויים מ-22–23/07: עדכון **`pcfPowerlinkToken`** ב-`1036` ותיקון קריטריון חיפוש ב-Make.
**בשש מתוך שמונה השיחות האחרונות לא בוצע שום שינוי בחשבונות החיים.** שיחה אחת (chat_22) כתבה **ל-ClickUp בלבד**.
**כל מי שממשיך — מתחיל משם.**
