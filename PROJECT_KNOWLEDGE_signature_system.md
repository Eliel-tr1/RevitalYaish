# Roital Yaish — Digital Signature System — Deep Technical Summary

> **עודכן 03/08/2026 — סקירת 26 שיחות הפרויקט.**

| # | מה שונה | מקור |
|---|---|---|
| 1 | §5 — בורר הערוצים (sms/email/whatsapp) בוטל. הערוץ קבוע: `send_method:"whatsapp"` hardcoded | chat_09 (28/07) |
| 2 | §8 — ה-Router התלת-ענפי והעדפת "SMS now" התהפכו. ענף וואטסאפ יחיד, SMS ירד מהשולחן | chat_09 (28/07) |
| 3 | הנספח הוחלף — הכפתור הנוכחי (28/07): 2 כפתורי כלים, הצגה + העתקה של קישור החתימה, בלי בורר ערוץ | chat_09 (28/07) |
| 4 | §4 סנריו B — סומן "מתועד אך לא מיושם": בפועל התגובה **לא** מחזירה `submission_url`; יעד = Query אחד | chat_09 (28/07) |
| 5 | payload השליחה צומצם ל-4 שדות בלבד אחרי rollback ארכיטקטוני | chat_09 (28/07) |
| 6 | `pcfSignatureStatus` — ערך `1` עבר רילייבל ל"ממתין לחתימה". **לא נוסף ערך 4** | chat_18 (26/07) |
| 7 | שער החתימה עבר מ-`pcfProductType` ל-`categorycode` (101 חוסם; 102 פתוח) | chat_12 |
| 8 | ההנחה ש"כל 9 החוזים מוגדרים כראוי" **הופרכה** — נפתחה משימה E3 | chat_27 (23/07) |
| 9 | גוצ'ת הפרסום ב-Tofsy הועלתה לראש המסמך כאזהרה מרכזית | chat_27 (23/07) |
| 10 | נוסף האינווריאנט "אין חתימה = אין תשלום"; חתימה נדרשת רק למסלולי ליווי — לא בוסט, לא ריטיינר | chat_07 + chat_11 |
| 11 | הפרדה מפורשת בין 1058 (תבניות/ניתוב) ל-1038 (מסמכים חתומים) + שרשרת הניתוב המלאה | chat_25 |
| 12 | תועדו 4 שדות החתימה על אובייקט 4: `pcfSignatureStatus`, `pcfcfDocLink`, `pcfFormLink`, `pcfFormFilled` | chat_25 |
| 13 | §9 אבטחה — מרשם רוטציה מורחב (5 מפתחות), סייג תזמון, והבהרה על חשיפת ה-webhook URLs | chat_09 + chat_20–27 |
| 14 | נוסף אימות שטח 28/07 עם הערכים המדויקים שנשלחו | chat_09 (28/07) |
| 15 | נוסף פירוק מלא של סנריו C (מודולים 1/4/5/7, retry 3×30 דק', DLQ, autoCommit) | chat_27 (23/07) |
| 16 | כפתור "שליחת חתימה" **הוסר ממסך הסליקה** — נקודת כניסה יחידה = הכפתור בכרטיס | chat_12 |
| 17 | תועדה המגבלה הארכיטקטונית: כפתור iframe מסוגל להשיג רק `opportunity_id` מה-URL של ההורה | chat_09 (28/07) |
| 18 | נוספה משימת ניקוי: 16 שורות legacy ב-1058 (חסום ב-dry-run) | chat_25 |
| 19 | נוסף סיכון פתוח: sandbox של iframe עלול לבלוע `target="_blank"` | chat_09 (28/07) |
| 20 | הפער הפתוח היחיד מנוסח מחדש: שליחה אוטומטית של הקישור בוואטסאפ **טרם נבנתה** | chat_09 + chat_27 |

---

**Audience:** Claude-to-Claude (project knowledge). A future Claude with zero prior context should be able to read this and resume work immediately.
**Status:** Documents flow is LIVE end-to-end. Two tasks open (auto-send channel; webhook-publish verification on all 9 contracts).
**Region:** Make eu2. **Last updated:** 2026-08-03 (previous: 2026-07-23).

---

## 🔴 קרא את זה קודם — הגוצ'ה שעלתה יום עבודה

**וובהוק מוגדר ≠ וובהוק פעיל.**

ב-Tofsy אפשר להגדיר וובהoק על חוזה, לראות אותו בממשק, ולקבל מהלקוחה "הטופס התקבל בהצלחה" — **ובכל זאת שום POST לא נשלח.** הסיבה: Tofsy שומרת עריכות במצב **טיוטה** עד שלוחצים **"פרסום שינויים"** בראש בונה הטפסים. חוזה שלא פורסם **לא יורה, בלי שום שגיאה ובלי שום סימן**.

זה בדיוק מה ששבר את חוזה **"תזונה אונליין"** (`6a5641eed0e96a63644ad0a3`) ב-23/07/2026. החוזה האח "מנטורית אישית" היה מפורסם ועבד — מה שהאריך את הדיבאג.

**דרישת האימות (משימה E3 — בעלים: מייק) — טרם בוצעה:**
לעבור על **כל 9 החוזים, אחד-אחד**, ולוודא בכל אחד שלושה דברים:
1. הוובהוק מוגדר תחת הגדרות טופס ← אינטגרציות
2. **"שליחת מסמך PDF"** מסומן
3. **השינויים פורסמו** (אין "פרסום שינויים"/"בטל שינויים" דולקים)

בנוסף: שליחת בדיקה אמיתית ל-1–2 חוזים נוספים. **זו משימת התשואה הגבוהה ביותר בפרויקט** — כחצי שעה עבודה, סוגרת כשל שקט שאין לו שום התרעה (chat_22).

⚠️ שים לב: instance שכבר נשלח (`fill.tofsy.co.il/{url_code}`) ונוצר **לפני** הפרסום **לא יורה רטרואקטיבית** — לפרסם, ואז לשלוח קישור חתימה **חדש** ולחתום עליו.

---

## 0. What this system is

A digital-signature pipeline for Roital Yaish (online women's wellness / weight-loss coaching). The sales process is phone-based: a rep calls a customer who finished a "Boost" cohort, closes on a program + price, and — **before charging** — must get the customer to sign the contract for that program. This system automates: pick the right contract by product → generate a personalized signing link with the deal anchored inside it → (customer signs) → file the signed PDF back and flip status.

**Order is sign-then-pay.** Payment (Grow) is explicitly OUT of scope for this build; it comes after signature and is a separate future workstream.

Three systems: **Fireberry** (CRM, source of truth, where the rep works), **Make** (eu2, execution layer, holds all credentials server-side), **Tofsy** (`my.tofsy.co.il`, digital signatures).

---

## 1. Two architectural invariants (do not break)

**A. The anchor.** Every sent document has the Opportunity id injected into a hidden field (`Opportunityid`). It returns on the signed webhook, which is how the receive scenario knows which deal was signed. Matching is NOT by phone/name (can be duplicate/wrong). This is the reason the contracts MUST be **two-step** forms — only two-step supports API pre-fill before the recipient opens the form.

**B. No client-side tokens.** The Fireberry button holds NO token and calls NO system directly. It sends an opportunity id to Make; all fetching happens server-side in Make. A button holding a Fireberry token exposes full CRM read/write/delete to anyone who opens dev tools.

**C. אין חתימה = אין תשלום.** *(נוסף 03/08/2026 — chat_07, chat_12, chat_26)*
שער החתימה **חוסם סליקה**. אי אפשר להעביר תשלום על מסלול ליווי לפני שהחוזה נחתם.
**היקף החובה:** חתימה נדרשת **רק למסלולי ליווי**. **בוסט וריטיינר אינם דורשים חתימה כלל** (chat_11).
**מקור האמת לשער:** `categorycode` של המוצר — ראו §2א.

**D. מגבלת ה-iframe.** *(נוסף 03/08/2026 — chat_09)*
כפתור iframe בפיירברי מסוגל להשיג **רק את `opportunity_id`**, ורק מה-URL של ההורה:
```js
function getOpportunityId(){
  try{ return window.parent.location.pathname.split('/').filter(Boolean).pop(); }
  catch(e){ return null; }
}
```
כל מזהה CRM אחר (`customer_id`, `product_id`, `document_id`) **חייב להישלף בצד השרת**. ההנחה שהם "מגיעים בוובהוק הראשון" נבדקה בשטח ב-28/07 והופרכה — סנריו הטעינה (A) מחזיר רק `{recommended_id, product_name, catalog}`. **מסקנת התכן: שאילתה אחת בצד Make זולה יותר מחוזה נתונים שביר בין שני וובהוקים.** כלל זה חל על כל כפתור עתידי בפרויקט.

---

## 2. Data model — Fireberry

Query endpoint: `POST https://api.fireberry.com/api/query`, header `tokenid`. Result array is named **`Data`** (Make UI labels it "Array" — do not write `DataArray`). Native Make app **Powerlink** (`app#powerlink`) is installed and preferred over raw HTTP for Query/Update/Create Object (managed connection, no per-module token). HTTP is used only where free-form JSON is needed.

### Opportunity — object 4 (תהליך מכירה), PK `opportunityid`
| Field (label) | system name | notes |
|---|---|---|
| סטטוס מסמך חתימה | `pcfSignatureStatus` | PickList: ~~`1`=נשלח~~ ⛔ מיושן (הוחלף 03/08/2026) → **`1`=ממתין לחתימה · `2`=נחתם · `3`=בוטל** |
| לינק למסמך האחרון | `pcfcfDocLink` | send: signing link; receive: overwritten with signed `pdf_url` |
| קישור לטופס | `pcfFormLink` | קיים על אובייקט 4, לא היה באפיון (chat_25) |
| הטופס מולא | `pcfFormFilled` | קיים על אובייקט 4, לא היה באפיון (chat_25) |
| מוצר ראשי מיועד | `pcfProduct` | Lookup → Product(14). Drives contract selection |
| שבועות מתנה | `pcfWeeksGift` | Injected as `Gift`. Values **1/2/3/4** (updated from 10/20/30/40) |
| לקוח | `accountid` | Lookup → Account(1) |

> **`pcfSignatureStatus` — הכרעה סופית (26/07/2026, chat_18, החלטה D1).**
> הערך `1` עבר **רילייבל** מ"נשלח" ל**"ממתין לחתימה"**. הערכים `2` ו-`3` לא נגעו.
> ⛔ **לא נוסף ערך `4`.** אם מסמך/מפרט אחר מורה להוסיף ערך 4 — הוא מיושן ויש לתקנו. הנימוק: ערך 4 היה יוצר שני ערכים לאותו מצב וכל תרחיש Make היה חייב לבדוק "1 או 4". רילייבל = אפס שינוי ב-Make, אפס דאטה שנשברת, הפיך.
> ערכי המערכת בפועל: **`1`=ממתין לחתימה · `2`=נחתם · `3`=בוטל.**

### Account — object 1 (לקוח), PK `accountid`
`accountname`, `telephone1`, `emailaddress1`.

### Product — object 14 (מוצר), PK `productid`
`pcfRelevantForm` — Lookup → catalog(1058). The link that translates product → contract.
שדות ליבה נוספים בשאילתת מוצרים: `productid`, `name`, `categorycode`, `statuscode`, `itemprice`.

> 🔴 **תנאי סף לכל הדגמה חיה (chat_08):** לוודא ש-`pcfRelevantForm` מקושר נכון על המוצר שמדגימים — בפרט **"תוכנית ליווי 12 שבועות"**. בלי הקישור הזה הדגמת החתימה החיה נופלת במקום.

### Catalog — object 1058 (רשימת מסמכים לחתימה), PK `customobject1058id`
`name`, `pcfformid` (Tofsy form id), `pcfformactive` (PickList כן/לא — only כן shows in the button), `pcfdefultplatform`.
**State:** 9 rows active (the two-step contracts). 16 legacy rows set inactive.

### Document — object 1038 (מסמך), signed-doc filing
`name`, `pcfLinkToDocument` (signed PDF url), `pcfLinkedSale` (→ opportunity), `pcfaccountid` (→ account), `pcfdocsigned` (PickList). This object pre-existed in the template with all needed fields — nothing was created here.

### 1058 מול 1038 — שני דברים שונים לגמרי *(נוסף 03/08/2026 — chat_25)*

| | **1058 — רשימת מסמכים לחתימה** | **1038 — מסמך** |
|---|---|---|
| מה זה | **תבניות וניתוב** — איזה חוזה שייך לאיזה מוצר | **המסמכים החתומים בפועל** |
| נוצר ע"י | אדם (מטמיע/עודד) | סנריו C, אוטומטית בקבלת חתימה |
| שדות | שם · `pcfformid` · פעיל כן/לא · ערוץ שליחה ברירת מחדל | `name` · `pcfLinkToDocument` · `pcfLinkedSale` · `pcfaccountid` · `pcfdocsigned` |

**שרשרת הניתוב המלאה:**
`מוצר(14) → pcfRelevantForm → שורה ב-1058 → pcfformid → API טופסי`

**הערך התפעולי של 1058 (למה לא למחוק אותו):** בלעדיו ה-`form_id` מוטמע קשיח ב-Make, וכל חוזה חדש דורש נגיעה בסנריו. איתו — שורה בטבלה + קישור מוצר, **ועודד יכול לעשות זאת לבד, בלי מטמיע.**

**משימת ניקוי פתוחה:** 16 שורות legacy ב-1058 מסומנות "לא פעיל". מייק: "תנקה". **טרם בוצע** — חסום ב-dry-run על `Product.pcfRelevantForm` ועל קישורים נכנסים מ-1038. אין למחוק בלי ה-dry-run.

### 2א. שער החתימה — מקור אמת *(נוסף 03/08/2026 — chat_12)*

**ההכרעה (מייק, chat_12): שער החתימה נקבע לפי `categorycode` של המוצר.**

| `categorycode` | קטגוריה | חוסם סליקה ללא חתימה? |
|---|---|---|
| `101` | תוכנית ליווי | ✅ **כן — מיושם** |
| `102` | תוכנית המשך | ⚠️ **לא הוכרע** |

~~השער נקבע לפי `pcfProductType` (`2` = פרימיום)~~ ⛔ מיושן (הוחלף 03/08/2026). המימוש ב-chat_11 השתמש ב-`pcfProductType = 2`; ההכרעה המאוחרת יותר ב-chat_12 קבעה `categorycode`. **המימוש בפועל של הכפתור עובד לפי `categorycode`.**

> ⚠️ **סתירה פתוחה — קטגוריה 102 ("תוכנית המשך")**
> **עמדה א':** רק `101` חוסם — כך זה מיושם היום בכפתור התשלום הידני.
> **עמדה ב':** גם "תוכנית המשך" היא מסלול ליווי ולכן אמורה לדרוש חתימה. קיימים **שני חוזי המשך פעילים ב-Tofsy** ("המשך ליווי מנטורית אישית", "המשך ליווי תזונה אונליין") — עצם קיומם תומך בעמדה זו.
> **מקור:** chat_12. השאלה נשאלה **3 פעמים ולא נענתה.**
> **בעלים: מייק / רויטל.** התיקון עצמו הוא הוספת `"102"` לשורה אחת בקוד — החלטה של דקה.

> ⚠️ **סתירה פתוחה — שני מקורות אמת לשער החתימה**
> `categorycode` (מה שנבנה בפועל, chat_12) מול `pcfProductType` (מה ש-WF-01 באפיון מגדיר, chat_11).
> כל עוד שניהם חיים — מוצר יחליק בפער ויעבור סליקה בלי חתימה.
> **מקור:** chat_11 (26/07) מול chat_12. **בעלים: מייק.** ההמלצה: לקבע `categorycode` ולסמן את `pcfProductType` כ-deprecated בכל מפרט.

### 2ב. נקודות כניסה לשליחה לחתימה *(נוסף 03/08/2026 — chat_12)*

**נקודת כניסה יחידה: כפתור "שליחת מסמך לחתימה" בכרטיס תהליך המכירה.**

~~מסך הסליקה כולל כפתור "שליחת חתימה" שקורא לסנריו B~~ ⛔ מיושן (הוחלף 03/08/2026).
בגרסה הראשונה של כפתור התשלום הידני היה כפתור "שליחת חתימה" במסך הסליקה שקרא לסנריו B ב-Make — **הוא הוסר.** מסך החסימה בסליקה כיום רק **מפנה** לכפתור החתימה הנפרד בכרטיס; הוא אינו נקודת כניסה.

---

## 3. Tofsy — the contracts

### The 9 two-step contracts (form_id)
| Contract | form_id |
|---|---|
| 5 שבועות | `6a56202dd0e96a63644993f4` |
| 6 שבועות | `6a563f18d0e96a63644a8e2c` |
| 8 שבועות | `6a563f72d0e96a63644a9140` |
| 12 שבועות | `6a563fb7d0e96a63644a9515` |
| 17 שבועות | `6a564047d0e96a63644a9e7b` |
| 22 שבועות | `6a56409bd0e96a63644aadc0` |
| 28 שבועות | `6a5640d2d0e96a63644aba58` |
| תקנון המשך ליווי מנטורית אישית | `6a564124d0e96a63644ac5c3` |
| תקנון המשך ליווי תזונה אונליין | `6a5641eed0e96a63644ad0a3` |

All are two-step, created by duplication (so field ids are identical across all). Price/duration are static contractual text per contract (NOT injectable fields — that's why there's one contract per program, not a unified form). "Gift weeks" bonus blocks are static content shown by display-condition on the `Gift` value.

> **למה לא טופס אחד עם שדות משתנים** *(נוסף 03/08/2026 — chat_25)*
> המחיר ומשך התוכנית הם **טקסט חוזי סטטי בגוף החוזה בטופסי**, לא שדות שניתן להזריק. חוזה שאומר **"5,660 ₪ עבור 22 שבועות"** חייב להיות מסמך נפרד מחוזה שאומר **"1,975 ₪ עבור 5 שבועות"**. זו מגבלה משפטית-טכנית, לא בחירת עיצוב — ולכן 9 חוזים ולא אחד.

> ~~All 9 have the receive webhook configured.~~ ⛔ מיושן (הוחלף 03/08/2026)
> **ההנחה הזו הופרכה ב-23/07/2026 (chat_27).** חוזה "תזונה אונליין" היה **מוגדר עם וובהוק אך לא פורסם** ולכן לא ירה מעולם. נכון להיום **לא אומת** שכל 9 החוזים תקינים — ראו הפרק האדום בראש המסמך ומשימה E3.

> ⚠️ **PUBLISH GOTCHA (verified 2026-07-23).** Configuring the receive webhook in a form's אינטגרציות is NOT enough — Tofsy keeps edits in a DRAFT state until you click **"פרסום שינויים"** (publish changes) at the top of the form builder. An unpublished webhook does not fire: the customer can sign and Tofsy shows "הטופס התקבל בהצלחה", but no POST is sent to Make. Symptom = Make receive scenario has zero executions AND an empty webhook Queue, while the form builder shows the webhook configured correctly. If you see "פרסום שינויים"/"בטל שינויים" lit on the form, changes are pending → publish. Also note: an already-sent instance (`fill.tofsy.co.il/{url_code}`) created before publishing will NOT fire retroactively — publish, then send a FRESH signing link and sign that. (This exact issue hit "תזונה אונליין" `6a5641eed0e96a63644ad0a3`; the sibling "מנטורית אישית" was already published and worked.)

**OUT OF CURRENT SCOPE — 6 מסמכים בשימוש ללא גרסת דו-שלבי** ולכן לא ניתנים לשליחה דרך המערכת עד שישוכפלו כדו-שלביים (**פער פתוח, לא באג**): סיום התקשרות · אישור הקפאת התהליך · קבוצה שקטה · 5+שבוע מתנה · 7 שבועות 2 · 8+2 שבועות.

### Injection field map — matched by field NAME, not id
The create endpoint matches on the field's `name` attribute (verified empirically; contradicts Tofsy's own doc example which used ids). All injected as Field type = Text.
| name (injection key) | internal id | source |
|---|---|---|
| `Opportunityid` | `textbox_1784029420890` | opportunity id — THE ANCHOR (hidden via display-condition + not in PDF) |
| `Full_Name` | `textbox_1784031547798` | `accountname` |
| `email` | `email_1784031580404` | `emailaddress1` |
| `phone` | `phone_1784031655418` | `telephone1` |
| `date` | `date_1784031691681` | today (`formatDate(now;"YYYY-MM-DD")`) |
| `Gift` | `textbox_1784035060123` | `pcfWeeksGift`, values 1/2/3/4, empty→0 |
| `id` | `id_1784031613217` | ת"ז — sent empty, customer completes; empty is fine |
| `Product_id` | `textbox_1784035005644` | product id (optional) |
| `signature_1` / `signature_2` | — | customer signs; NEVER injected |

### Tofsy endpoints (auth = JWT)
- **אימות:** `POST https://my.tofsy.co.il/api/auth/login` — body JSON `{email, api_key}` → `token` (24h).
- `GET https://my.tofsy.co.il/api/forms` — Bearer. Lists forms. (Note: `/api/fill/forms` does NOT list.)
- `GET https://my.tofsy.co.il/api/fill/forms/{id}/schema` — Bearer. Returns all fields + ids.
- **יצירת טופס:** `POST https://my.tofsy.co.il/api/fill/forms/{formId}/create` — Bearer, **`multipart/form-data` — לא JSON**, two-step only → returns `url_code`.
- **קישור לנמענת:** `https://fill.tofsy.co.il/{urlcode}` — מקור ה-`url_code` הוא תגובת `/create`.
- **וובהוקים דורשים מנוי PRO.**
- **Tofsy does NOT send the link via API.** The API ends at `url_code`. Sending to the customer is on us (the open task, §8).

### Receive webhook payload (per Tofsy docs + verified)
Fires when the customer submits after signing. Keys are by field **name** (so anchor returns as `Opportunityid`). Includes all filled fields, `signature_1/2` (boolean/1), the signed PDF under `pdf` (base64) AND a direct `pdf_url` (preferred for filing — a link, not a heavy blob). Configured per form under הגדרות טופס ← אינטגרציות: content-type `application/json`, method POST, "שליחת מסמך PDF" checked. **Must be PUBLISHED (§3 publish gotcha), not just configured.** No API for this — manual per form; every new contract must have it set.

---

## 4. The three Make scenarios (eu2)

All must be **ON** (not Run once). Make work is **manual, by Mike only** — Claude never writes to Make via API.

### Scenario A — Load list · webhook `c3lcf9yf35xfngvxmv1xhw28i3cmi2p2`
1. Custom webhook — receives `opportunity_id`.
2. HTTP POST `api.fireberry.com/api/query` (headers tokenid + content-type + accept), body `{objecttype:1058, fields:"name,pcfformid,pcfformactive,pcfdefultplatform", query:"", page_size:50, page_number:1}`.
3. Webhook response 200, body `{"recommended_id":"","product_name":"","catalog": {{2.data}} }`. Button filters active client-side.

> **מאומת 28/07 (chat_09):** התגובה של סנריו A מחזירה **רק** `{recommended_id, product_name, catalog}`. היא **אינה** מחזירה `customer_id` / `product_id` / `document_id`.

### Scenario B — Send · webhook `53w7nb0ktyb42h5ymsfwmokpp2r6ovdf`

> 🟡 **מתועד אך לא מיושם במלואו (סומן 03/08/2026 — chat_09, 28/07).**
> שתי אי-התאמות מול השטח:
> **(א)** בפועל התגובה **לא** מחזירה `submission_url`, למרות שסעיף 9 למטה טוען שכן. הכפתור כבר קורא את השדה — בלעדיו אין קישור במסך ההצלחה. 🔴 **חוסם. בעלים: מייק.**
> **(ב)** ההחלטה החדשה (chat_09, החלטה 5) היא לצמצם את **4 מודולי ה-Query ל-Query אחד** על objecttype 4 לפי `opportunityid`, ולשלוף ממנו את ה-lookups של הלקוח והמוצר. 🟡 חוב טכני, לא חוסם. **בעלים: מייק.**
> התיאור להלן הוא המצב **המתועד** — לא בהכרח מה שרץ עכשיו.

1. Custom webhook — `opportunity_id`, `form_id` (empty=default), `form_label`, `send_method`.
2. Powerlink Query Object 4 where `opportunityid = {webhook.opportunity_id}`, fields `accountid, pcfProduct, pcfWeeksGift`.
3. Powerlink Query Object 1 where `accountid = {2.accountid}`, fields `accountname, telephone1, emailaddress1`.
4. Powerlink Query Object 14 where `productid = {2.pcfProduct}`, fields `pcfRelevantForm`. **Continue-when-no-results ON.**
5. Powerlink Query Object 1058 where `customobject1058id = {4.pcfRelevantForm}`, fields `name, pcfformid`. **Continue-when-no-results ON.**
6. HTTP Tofsy login → token.
7. HTTP Tofsy create — POST, multipart/form-data, `Authorization: Bearer {6.token}`. **URL picks manual vs product-default in one expression:**
   `https://my.tofsy.co.il/api/fill/forms/{{ifempty(2.form_id; 6.Data[].pcfformid)}}/create`
   (module numbering is illustrative; in the live scenario the catalog-query module is the one exposing `pcfformid`). Injects the 7 fields from the map above (empty-safe values).
8. Powerlink Update Object 4, id = webhook `opportunity_id`: `pcfSignatureStatus=1` (**"ממתין לחתימה"**), `pcfcfDocLink` = signing link.
9. Webhook response 200: `{"response":"success","submission_url":"https://fill.tofsy.co.il/{url_code}"}` — **דרוש, לא מיושם.**

*(An earlier Router that split manual vs product was replaced by the `ifempty` expression in step 7 — one line, no module duplication. If a leftover Router exists it can be deleted.)*

**לוגיקת בחירת המסמך (chat_09, החלטה 7):** `form_id` לא ריק → משתמשים בו כמו שהוא; אחרת → המסמך המקושר למוצר. **רק מקרה "ברירת מחדל" דורש שליפה.**
**כלל Fireberry:** שדות lookup בתוצאת Query על אובייקט 4 יש להוציא כ-`pcfX` (ה-id, לא ה-name).

**פורמט התגובה הנדרש מסנריו B (מודול אחרון, Webhook Response):**
```
Status: 200
Content-Type: application/json
Body:
{
  "response": "success",
  "submission_url": "https://fill.tofsy.co.il/{{url_code}}"
}
```

### Scenario C — Receive · webhook `7g2xvjmgulpqoic8ai69e5sfm60vp4n7`
Named **"קבלת מסמך טופסי"** / **"Signed Document from Tofsy"** in Make. Verified running end-to-end 2026-07-23, and re-verified module-by-module against the blueprint in chat_27 — **identical to this documentation, no drift.**

**פירוק מלא (4 מודולים — מספור הבלופרינט: 1/4/5/7):**

| מודול | פעולה | פירוט |
|---|---|---|
| **1** | וובהוק "קבלת טופס מטופסי" (instant) | payload בשימוש: `Opportunityid` (העוגן), `pdf_url`, `Full_Name`, `date` |
| **4** | חיפוש תהליך מכירה (קריאה בלבד) | אובייקט **4**, לפי `opportunityid = {{Opportunityid}}`. מטרה: שליפת `accountid` + אימות קיום העסקה. **מושך את כל שדות העסקה בשביל `accountid` אחד** — בזבזני אך תקין; אופטימיזציה לא דחופה (הכרעת מייק, chat_27) |
| **5** | עדכון תהליך מכירה | אובייקט 4, `objectid = {{Opportunityid}}` → `pcfSignatureStatus = 2` ("נחתם") + `pcfcfDocLink = {{pdf_url}}` (**דורס** את קישור החתימה בקישור ל-PDF החתום) |
| **7** | יצירת רשומה - מסמך | אובייקט **1038**, 5 שדות: `name = {{Full_Name}} {{date}}` · `pcfLinkToDocument = {{pdf_url}}` · `pcfLinkedSale = {{Opportunityid}}` · `pcfaccountid = {{4.accountid}}` · `pcfdocsigned = 1` |

**מה הסנריו לא עושה:** לא נוגע ב-Account, לא ב-1051 (ליווי), לא מפעיל תשלום, **ולא שולח שום דבר ללקוחה.**
**עמידות:** לכל 3 מודולי פיירברי retry אוטומטי — **3 ניסיונות, כל 30 דקות**. DLQ פעיל (Incomplete executions) + autoCommit.

**Debugging a "nothing arrived" report — the decisive isolation test:** check the receive scenario's **webhook Queue** (Webhooks → the hook → Queue) AND its History together. Empty Queue + no execution + scenario ON = Tofsy never sent → it's a Tofsy-side problem (publish gotcha §3, or the form's integration missing). Items in Queue + no execution = scenario was OFF → turn ON to drain. Tofsy's own "הטופס התקבל בהצלחה" screen only means Tofsy received the signature; it does NOT mean a webhook was POSTed.

---

## 5. The button (Fireberry iframe on the Opportunity card)

**גרסה נוכחית: 28/07/2026.** ארטיפקט: `send_document_button.html`.

Reads the opportunity id from the parent URL path. On open, calls Scenario A and populates the dropdown with active catalog rows (sorted, Hebrew). Default option = "המסמך של העסקה" (sends empty `form_id`; Make resolves by product). If load fails, falls back to default-only gracefully (15s timeout). Both webhook URLs are hardcoded at the top of the script.

### מה השתנה ב-28/07

**~~Channel selector: sms / email / whatsapp (sends `send_method`)~~ ⛔ מיושן (הוחלף 03/08/2026).**
אין בורר ערוצים בכלל. הערוץ **קבוע: `send_method: "whatsapp"` hardcoded בקוד.** במקום הבורר יושב טקסט סטטי:
`<p class="hint" style="margin-top:14px">הקישור לחתימה יישלח ללקוחה בוואטסאפ.</p>`

**payload השליחה — 4 שדות בלבד:**
```json
{
  "opportunity_id": "<מה-URL של כרטיס העסקה>",
  "form_id": "<אידי טופס שנבחר, ריק = ברירת מחדל>",
  "form_label": "<שם הטופס>",
  "send_method": "whatsapp"
}
```
> **הערת rollback:** בסיבוב ביניים (28/07 07:08) הורחב ה-payload ל-7 שדות עם `customer_id` / `product_id` / `document_id`. **בוטל ב-rollback ארכיטקטוני מלא** אחרי שמייק הראה בשטח שכל השלושה חוזרים **ריקים**. ראו אינווריאנט D בסעיף §1.

**בלוק "כלים נוספים" — 2 כפתורי מתאר (outline):**
| כפתור | יעד |
|---|---|
| מדריך להוספת מסמך | `https://drive.google.com/file/d/1R8l-39t34BISUun7Ii_ncjpO9CWANoFf/view?usp=drive_link` |
| הוספת מסמך | `https://app.fireberry.com/app/views/1058` |

שניהם `<a target="_blank" rel="noopener noreferrer">` ולא `window.open` — **בכוונה:** ניווט ולא pop-up, כדי לא לגעת ב-JS הקיים ולהקטין סיכוי לחסימת sandbox. סגנון **מתאר** ולא מילוי — כדי לא להתחרות ויזואלית ב-"שליחה לחתימה" שהיא הפעולה הראשית.

**מסך ההצלחה — נבנה מחדש:**
1. `✓ הטופס נשלח בהצלחה!`
2. `<a target="_blank" rel="noopener noreferrer">לחצי כאן לכניסה למסמך</a>`
3. **שורת העתקה:** `<input class="copy-url" readonly>` (`direction:ltr; text-align:left`) + כפתור "העתקה" שמתחלף ל-"הועתק ✓" למשך 1500ms (`navigator.clipboard.writeText` עם fallback).

**פלטת העיצוב — לשימור בכל שינוי עתידי:**
`--rose:#b06a82` · `--rose-dark:#955a6e` · `--cream:#f7f2ee` · `--line:#e4dcdf` · `--ink:#3a2f33` · `--muted:#8a7c81` · `--ok:#3f7d62` · `--err:#a8434f` · פונט `'Segoe UI',Tahoma,Arial,sans-serif` · `dir="rtl"`.

### אימות שטח — 28/07/2026 (chat_09)
שליחה אמיתית שעברה נכון end-to-end מהכפתור לוובהוק:
```
opportunity_id  d94f6e1e-2a66-4c5c-a4c7-fe70dfc2dbb7
form_id         6a564047d0e96a63644a9e7b   ← "17 שבועות"
form_label      17 שבועות
send_method     whatsapp
```
ה-`form_id` תואם בדיוק את טבלת 9 החוזים ב-§3. **הבחירה הידנית מהרשימה עובדת נכון.**

### חוזה ה-API של הכפתור
- `LOAD_WEBHOOK_URL` = `https://hook.eu2.make.com/c3lcf9yf35xfngvxmv1xhw28i3cmi2p2` (סנריו A) — timeout 15000ms דרך `AbortController`.
- `SEND_WEBHOOK_URL` = `https://hook.eu2.make.com/53w7nb0ktyb42h5ymsfwmokpp2r6ovdf` (סנריו B) — timeout 20000ms.
- פענוח הקטלוג: `data.catalog` עשוי לחזור כמחרוזת → `JSON.parse`; ואז `cat.data.Data || cat.data.DataArray`.
- סינון פעילים: `String(r.pcfformactivename || r.pcfformactive || '').trim() === 'כן' || === '1'`.
- ערך ה-option = `r.pcfformid`, טקסט = `r.name`, מיון `localeCompare(...,'he')`.

### 🔴 חוסמים על הכפתור (בעלים: מייק)
1. **סנריו B חייב להחזיר `submission_url`** ב-Webhook Response עם `Content-Type: application/json`. הכפתור כבר קורא את השדה — בלעדיו מסך ההצלחה לא מציג קישור. **זה באג בצד Make, לא בכפתור.**
2. **ה-HTML המעודכן טרם הוטמע בפועל ב-Fireberry.** לא אושר בשיחה שהודבק. עד שיודבק — כל האמור בסעיף זה תיאורטי.

### 🟡 סיכונים פתוחים
- **sandbox של iframe:** אם Fireberry מריצה את ה-iframe עם sandbox שחוסם pop-ups, `target="_blank"` עלול להיבלע. **לא נבדק.** Fallback מתוכנן: `window.open`. יש לבדוק על כרטיס תהליך מכירה אמיתי.
- **עמידות:** אם סנריו הטעינה נכשל, הכפתור עדיין עובד — אבל רק עם "ברירת מחדל". מומלץ (לא חובה) להשאיר Query אחד בסנריו השליחה כרשת ביטחון כשהשדות ריקים.
- **הרשאות סרטון המדריך בדרייב** — הקישור הוא `?usp=drive_link`; לוודא צפייה לכל מי שנכנס מהכפתור. בעלים: רויטל / מייק.

---

## 6. Critical technical learnings (all verified empirically; each caused a failure before it was understood)

**Tofsy**
- **A configured webhook must be PUBLISHED, not just saved.** Edits sit in draft until "פרסום שינויים"; unpublished = no POST fires even though the customer signs and Tofsy shows success. Already-sent instances created pre-publish don't fire retroactively — publish, then resend a fresh link. (Full detail: הפרק האדום בראש המסמך + §3. This burned ~a day of debugging on 2026-07-23.)
- `/create` works ONLY on two-step forms; one-step returns `Form is not 2-step`. Form type is set at creation and cannot be converted — must recreate. (Watch for legacy one-step lookalikes with near-identical names, e.g. a "מנטורית אישית עתליה" חד-שלבי — do not send those.)
- **וובהוקים ב-Tofsy דורשים מנוי PRO.** בלי PRO אין קליטה חזרה — כל הפייפליין נעצר אחרי החתימה.
- **`/create` מקבל `multipart/form-data` בלבד — לא JSON.** שליחת JSON נכשלת.
- The recipient link `fill.tofsy.co.il/{url_code}` is a sent INSTANCE, not the form template; you cannot map it back to a template from the code alone. The form_id lives in the builder URL (`form-builder/{form_id}`) and in Scenario B's create-module URL (`/forms/{form_id}/create`).
- Filling a form via the builder's "תצוגת מילוי" preview does NOT trigger integrations. Only a real signed submit through the recipient link fires the webhook.
- **Injection matches by field `name`, not internal widget id.** Injecting by id returns empty `form_data` silently.
- **A multipart field sent with no `value` key at all (missing, not empty-string) corrupts the ENTIRE submission** — all fields come back empty. Always send every field with a value; use `ifempty(...; "")`.
- URL query-param prefill (`?field=value`) does NOT work.
- Tofsy does not send via API; the in-UI send screen is manual only.
- Duplicating a form preserves field ids → same injection map works on all 9. A form built from scratch gets new ids and breaks the scenario.

**Fireberry**
- Query result array is `Data`, not `DataArray`.
- `"fields": "*"` fails with a server error; enumerate explicit field names.
- Prefer the native Powerlink Make app over raw HTTP.
- Enable "Continue the route when the module returns no results" on the product/catalog queries — otherwise an opportunity without a linked product halts the whole run, even when the rep picked a contract manually.
- **גוצ'ת ה-403** *(נוסף 03/08/2026 — chat_27)*: השוואת שדה מזהה (`customobject1036id` וכו') לערך שאינו GUID (למשל `1`) **מפילה את שרת פיירברי ומחזירה `[403] RunTimeError`** — לא 400. השגיאה מטעה ונראית כמו בעיית הרשאות. תיקון: להשוות לפי `name`, או להדביק GUID מלא. ל-fallback שקט: `00000000-0000-0000-0000-000000000000` + "Continue when no results".

**Make**
- Always map from the tree, never type `{{n.field}}` by hand → typing yields `references non-existing module` when the module number differs.
- Formulas don't nest: `{{ifempty({{3.x}}; "0")}}` is wrong; correct is `{{ifempty(3.x; "0")}}`.
- Run once answers a single call; live use requires the scenario ON.
- JSON string values on one line; a newline inside a string → `Bad control character`.
- **`fields` ריק = כל השדות** — תקין ועובד, אך בזבזני. שם החיבור ב-Make: **"Revital - New"**.

---

## 7. Current state

**Working (verified end-to-end):** button (גרסת 23/07 — גרסת 28/07 טרם הוטמעה); scenarios A/B/C; anchor injection + return; status ממתין לחתימה→נחתם; signed-doc filing to 1038; manual contract override via `ifempty`; catalog trimmed to the 9 active. **Verified again 2026-07-23** on "תזונה אונליין" after publishing its (previously unpublished) webhook — full C-scenario ran green, opportunity flipped to נחתם with signed pdf link. סנריו C אומת שוב מול הבלופרינט ב-chat_27 — זהה לתיעוד.

**~~9 two-step contracts with webhooks~~ ⛔ מיושן (הוחלף 03/08/2026)** — 9 החוזים קיימים ודו-שלביים, אבל **תקינות הוובהוק בכולם לא אומתה** (chat_27). ראו E3.

**פתוח:**
| # | פריט | בעלים | חוסם? |
|---|---|---|---|
| 1 | **שליחה אוטומטית של קישור החתימה ללקוחה בוואטסאפ — טרם נבנתה.** הקישור חוזר למסך הנציגה ונשלח ידנית. אין מודול ב-Make שצורך את `send_method` | מייק | 🔴 הפער המרכזי של המערכת |
| 2 | **E3 — אימות פרסום הוובהוק על כל 9 החוזים** (מוגדר · PDF מסומן · פורסם) + שליחת בדיקה ל-1–2 | מייק | 🔴 כשל שקט |
| 3 | סנריו B חייב להחזיר `submission_url` | מייק | 🔴 |
| 4 | הטמעת ה-HTML של גרסת 28/07 בכפתור בפיירברי | מייק / אליאל | 🔴 |
| 5 | צמצום 4 מודולי Query בסנריו B ל-Query אחד | מייק | 🟡 חוב טכני |
| 6 | הכרעה: קטגוריה 102 דורשת חתימה? | מייק / רויטל | 🟡 |
| 7 | ניקוי 16 שורות legacy ב-1058 (אחרי dry-run) | מייק | 🟡 |
| 8 | שכפול 6 המסמכים החסרים כדו-שלביים | מייק / רויטל | 🟡 מחוץ לסקופ הנוכחי |
| 9 | בדיקת sandbox — `target="_blank"` בכפתורי הכלים | מייק | 🟡 |
| 10 | **E2 — רוטציית טוקנים** (ראו §9) | מייק | 🔴 לפני פרודקשן |

---

## 8. Open task spec — auto-send channel

> ~~Add a Router on `send_method` with three branches (`sms` / `email` / `whatsapp`)~~ ⛔ מיושן (הוחלף 03/08/2026)
> ~~Mike's stated preference: SMS now, bot later~~ ⛔ מיושן (הוחלף 03/08/2026)
>
> **ההעדפה התהפכה (chat_09, 28/07). ההחלטה הנוכחית: וואטסאפ בלבד. SMS ירד מהשולחן.**
> **אין צורך ב-Router — ענף אחד.** הכפתור שולח `send_method:"whatsapp"` קבוע; אין ערך אחר שיכול להגיע.

**המפרט הנוכחי — ענף יחיד:**
הוסף אחרי מודול ה-`create` בסנריו B מודול אחד שולח, שמעביר את `https://fill.tofsy.co.il/{url_code}` ל-`telephone1` של הלקוחה בוואטסאפ.

**ספק — סתירה שיש להכריע לפני בנייה:**
- **CloudChat** — הוכרז כערוץ שליחת ההודעות ללקוחות (chat_13). מערכת מסמכי החתימה בקלאודצ'אט הוגדרה כ**תבנית האב לשכפול** לכל צינור הודעות חדש.
- **GreenAPI** — ירד מהתמונה כערוץ הודעות; נשאר **לניהול קבוצות בלבד** (`getContacts`, `getGroupData`, יצירת קבוצה, נעילה).

**המזהים בקלאודצ'אט** *(chat_13 — verbatim)*:
| פריט | מזהה |
|---|---|
| שדה משתמש `document_link_after_sign` (text) | `f201689v15852771` |
| פלואו `send_form_after_sign_flow` | `f201689s4376835` |
| תבנית `send_form_after_sign_template_v2` (APPROVED, he) | — |

**מגבלות ואזהרות:**
- **פורמט טלפון:** GreenAPI דורש `972501234567@c.us`; Fireberry שומר `0501234567` — נדרשת המרה.
- 🔒 **אם ייבחר GreenAPI ישיר — הטוקן נכנס ל-URL של הצומת ⇒ נכנס ל-export של ה-workflow.** אסור לשלוח את ה-JSON בצ'אט או בוואטסאפ. שיקול אבטחה שמשפיע על הכרעת הערוץ.
- לחסום בשגיאה ברורה כשללקוחה אין טלפון.
- `pcfSmsName` ב-1036 עדיין `"Vitrue"` ולא "רויטל" — 🔴 לתקן לפני שליחה ראשונה ללקוחות אמיתיות (chat_27).

> ⚠️ **סתירה פתוחה — שדה "ערוץ ברירת מחדל" ב-1058**
> **עמדה א':** האובייקט 1058 מכיל שדה `pcfdefultplatform` ("ערוץ ברירת מחדל — WhatsApp / SMS"), והוא מופיע גם באישור הלייאאוט של מערכת החתימות (chat_07).
> **עמדה ב':** ההחלטה התפעולית (chat_09, 28/07) היא **וואטסאפ בלבד**; הכפתור אפילו לא קורא את השדה.
> **ההכרעה התפעולית עד להודעה חדשה:** השדה קיים באובייקט אך **אין להשתמש ב-SMS**. הערוץ היחיד הוא וואטסאפ.
> **מקור:** chat_07 מול chat_09 (28/07). **בעלים: מייק.**

---

## 9. Security — מרשם רוטציה

**מה תקין בארכיטקטורה:**
- כתובות שני ה-webhooks של Make **מוטמעות hardcoded ב-HTML** של הכפתור וגלויות לכל מי שפותח dev tools ב-Fireberry. **זה מקובל.**
- **אין בקוד הכפתור `tokenid` של Fireberry ואין `api_key` של Tofsy.** האינווריאנט "No client-side tokens" (§1B) **נשמר**. חשיפת URLs — כן; חשיפת טוקנים — לא.
- ה-API Token של פיירברי יושב בשדה **`pcfPowerlinkToken`** על אובייקט 1036 ("הגדרת משתמש", רשומה יחידה `name="1"`). הוא מקנה **קריאה/כתיבה/מחיקה מלאה על כל ה-CRM** ⇒ **server-side בלבד (Make)**, לעולם לא בכפתורים, קוד צד-לקוח או טפסים. עיקרון קשיח בפרויקט.

**🔴 E2 — רוטציית טוקנים. חמישה מפתחות, לא שלושה. אף רוטציה לא אומתה כבוצעה.**

| # | מפתח | סטטוס |
|---|---|---|
| 1 | Fireberry `tokenid` | ⚠️ נחשף בצ'אט — לרוטציה |
| 2 | Make API | ⚠️ נחשף בצ'אט — לרוטציה (גישה מלאה לחשבון וכל הקונקשנים מאחוריו) |
| 3 | Tofsy `api_key` | ⚠️ נחשף בצ'אט — לרוטציה |
| 4 | GreenAPI `apiTokenInstance` | ⚠️ נחשף בצ'אט — לרוטציה |
| 5 | CloudChat API key | ⚠️ נחשף בצ'אט — לרוטציה |

**⚠️ לעולם אין לרשום ערך טוקן במסמך — בשום מסמך בפרויקט.**

**⏱️ תזמון — לא עכשיו, ולא כ"ניצחון מהיר".** רוטציה **שוברת את כל חיבורי Make** עד שמעדכנים אותם. אם מישהו בונה במקביל, דברים ייפלו לו בלי שיבין למה. יש לתזמן **חלון מתואם**, ורצוי אחרי סיום הטסטים.

**צ'קליסט חובה אחרי הרוטציה — שלושה מקומות:**
1. החיבורים ב-Make (**"Revital - New"**)
2. ה-credential ב-n8n (`Fireberry — tokenid`, Header Auth)
3. השדה **`pcfPowerlinkToken`** ברשומה של 1036

---

## 10. Maintenance procedures

- **Add a contract:** duplicate an existing two-step contract (never from scratch) → edit text → set the receive webhook in אינטגרציות + סמן **"שליחת מסמך PDF"** → **click "פרסום שינויים" to publish (else the webhook never fires — see the red section at the top)** → add a catalog row (1058) with its `pcfformid` + `pcfformactive = כן` → link the product via `pcfRelevantForm`.
- **Signed doc not coming back?** Run the §4 isolation test (webhook Queue + History). Most common cause = the form's webhook was configured but **not published**; second = the wrong/one-step form was sent.
- **Remove from list:** set `pcfformactive` = לא on the catalog row.
- **Change price/terms:** edit the contract text in Tofsy (price/duration are static contractual text, not fields) → **publish changes**.
- **Change a webhook url:** receive webhook is per-form (manual, all 9, **publish after**); load/send webhooks are in the button code only.
- **כלל פרויקט:** אין לגעת ב-Make דרך Claude Code / API. **כל שינוי ב-Make הוא ידני, של מייק בלבד.** פיתוח חדש נבנה ב-n8n; תחזוקת הקיים נשארת ב-Make.

---

## נספח — הכפתור, גרסת 28/07/2026

> **החלף את הנספח הישן.** ~~הקוד הקודם בנספח היה גרסת 23/07 עם `<select id="methodSelect">` ואופציית SMS~~ ⛔ מיושן (הוחלף 03/08/2026).
>
> 🔴 **חוסם לפני שהכפתור יעבוד במלואו:**
> **(א)** סנריו B חייב להחזיר `submission_url` בגוף התגובה — אחרת שורת הקישור וההעתקה במסך ההצלחה נשארות ריקות.
> **(ב)** ה-HTML חייב להיות **מוטמע בפועל בפיירברי ע"י מייק** — לא אושר בשום שיחה שההדבקה בוצעה.
>
> ⚠️ הקוד להלן משוחזר מהתיאור המפורט ב-chat_09. **מקור האמת הוא הארטיפקט `send_document_button.html` מ-28/07** — לאמת מולו לפני הדבקה.

```html
<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>שליחת מסמך לחתימה</title>
<style>
  :root{--rose:#b06a82;--rose-dark:#955a6e;--cream:#f7f2ee;--line:#e4dcdf;
        --ink:#3a2f33;--muted:#8a7c81;--ok:#3f7d62;--err:#a8434f}
  *{box-sizing:border-box}
  body{font-family:'Segoe UI',Tahoma,Arial,sans-serif;background:var(--cream);
       color:var(--ink);margin:0;padding:24px 16px;display:flex;justify-content:center}
  .card{width:100%;max-width:440px;background:#fff;border:1.5px solid var(--rose);
        border-radius:16px;padding:26px 24px 22px;box-shadow:0 8px 28px rgba(176,106,130,.12)}
  .card h1{font-size:20px;font-weight:700;color:var(--rose);margin:0 0 4px;text-align:center}
  .sub{font-size:13px;color:var(--muted);text-align:center;margin:0 0 20px}
  label{display:block;font-size:13.5px;font-weight:600;margin:16px 0 6px}
  select{width:100%;padding:11px 12px;font-size:14px;font-family:inherit;color:var(--ink);
         background:#fff;border:1px solid var(--line);border-radius:9px;appearance:none;cursor:pointer}
  select:focus{outline:none;border-color:var(--rose);box-shadow:0 0 0 3px rgba(176,106,130,.15)}
  .hint{font-size:11.5px;color:var(--muted);margin-top:5px}
  button{width:100%;margin-top:24px;padding:13px;font-size:15px;font-weight:700;font-family:inherit;
         color:#fff;background:var(--rose);border:none;border-radius:10px;cursor:pointer;transition:background .15s}
  button:hover{background:var(--rose-dark)}
  button:disabled{opacity:.55;cursor:default}
  #status{margin-top:18px;font-size:14px;text-align:center;min-height:20px;line-height:1.5}
  .err{color:var(--err)}
  .success-big{margin-top:22px;padding:20px 16px;background:#eef6f1;border:1.5px solid var(--ok);border-radius:14px}
  .success-big .check{display:block;font-size:40px;line-height:1;margin-bottom:8px}
  .success-big .big{display:block;font-size:23px;font-weight:800;color:var(--ok)}
  .success-big a{display:inline-block;margin-top:8px;font-size:15px;color:var(--rose);font-weight:700}
  .spin{display:inline-block;width:14px;height:14px;border:2px solid var(--line);border-top-color:var(--rose);
        border-radius:50%;animation:s .7s linear infinite;vertical-align:-2px;margin-left:6px}
  @keyframes s{to{transform:rotate(360deg)}}

  /* ===== נוסף 28/07: הצגת קישור החתימה עם העתקה ===== */
  .copy-row{display:flex;gap:8px;margin-top:12px}
  .copy-url{flex:1 1 auto;padding:9px 10px;font-size:12.5px;font-family:inherit;
            border:1px solid var(--line);border-radius:8px;background:#fff;color:var(--ink);
            direction:ltr;text-align:left}
  .copy-btn{flex:0 0 auto;width:auto;margin-top:0;padding:9px 14px;font-size:13px;
            background:var(--ok);border-radius:8px}
  .copy-btn:hover{background:#356b54}

  /* ===== נוסף 27/07: כלים נוספים (2 כפתורי מתאר) ===== */
  .tools{margin-top:20px;padding-top:18px;border-top:1px solid var(--line);
         display:flex;flex-direction:column;gap:10px}
  .tools-title{font-size:12.5px;font-weight:600;color:var(--muted);margin:0 0 2px}
  .btn-tool{display:flex;align-items:center;justify-content:center;gap:8px;
            width:100%;margin-top:0;padding:12px;font-size:13.5px;font-weight:500;
            color:var(--rose);background:#fff;border:1.5px solid var(--rose);
            border-radius:10px;text-decoration:none}
  .btn-tool:hover{background:#fdf7f9}
  .btn-tool svg{flex:0 0 auto}
</style>
</head>
<body>
  <div class="card">
    <h1>שליחת מסמך לחתימה</h1>
    <p class="sub">בחרי מסמך ולחצי שליחה</p>

    <label for="formSelect">טופס לחתימה:</label>
    <select id="formSelect">
      <option value="" selected>ברירת מחדל — המסמך של העסקה</option>
    </select>
    <p class="hint" id="formHint">טוען את רשימת המסמכים <span class="spin"></span></p>

    <!-- 28/07: בורר הערוצים הוסר. הערוץ קבוע — וואטסאפ. -->
    <p class="hint" style="margin-top:14px">הקישור לחתימה יישלח ללקוחה בוואטסאפ.</p>

    <button id="sendBtn" type="button">שליחה לחתימה</button>
    <div id="status"></div>

    <!-- נוסף 27/07: 2 כפתורים -->
    <div class="tools">
      <p class="tools-title">כלים נוספים</p>
      <a class="btn-tool" target="_blank" rel="noopener noreferrer"
         href="https://drive.google.com/file/d/1R8l-39t34BISUun7Ii_ncjpO9CWANoFf/view?usp=drive_link">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M8 5v14l11-7z"/></svg>
        מדריך להוספת מסמך
      </a>
      <a class="btn-tool" target="_blank" rel="noopener noreferrer"
         href="https://app.fireberry.com/app/views/1058">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8l-6-6zm-1 9h3v2h-3v3h-2v-3H8v-2h3V8h2v3z"/></svg>
        הוספת מסמך
      </a>
    </div>
  </div>
<script>
  const LOAD_WEBHOOK_URL = "https://hook.eu2.make.com/c3lcf9yf35xfngvxmv1xhw28i3cmi2p2";
  const SEND_WEBHOOK_URL = "https://hook.eu2.make.com/53w7nb0ktyb42h5ymsfwmokpp2r6ovdf";

  const $ = id => document.getElementById(id);
  function getOpportunityId(){
    try{ return window.parent.location.pathname.split('/').filter(Boolean).pop(); }
    catch(e){ return null; }
  }
  const opportunityId = getOpportunityId();
  function setStatus(html,cls){const s=$('status');s.className=cls||'';s.innerHTML=html;}

  async function fetchT(url,opts,ms){
    const c=new AbortController();
    const t=setTimeout(()=>c.abort(),ms||15000);
    try{ return await fetch(url,Object.assign({},opts,{signal:c.signal})); }
    finally{ clearTimeout(t); }
  }

  async function loadCatalog(){
    try{
      const res = await fetchT(LOAD_WEBHOOK_URL,{
        method:'POST',headers:{'Content-Type':'application/json'},
        body:JSON.stringify({opportunity_id:opportunityId})
      },15000);
      if(res.status!==200) throw new Error('status');
      const data = await res.json();

      let cat = data.catalog;
      if(typeof cat==='string'){ try{cat=JSON.parse(cat);}catch(e){cat={};} }
      const dd = (cat && cat.data) ? cat.data : {};
      const rows = dd.Data || dd.DataArray || [];
      const active = rows.filter(r => {
        const v = String(r.pcfformactivename || r.pcfformactive || '').trim();
        return v==='כן' || v==='1';
      });
      if(!active.length) throw new Error('empty');

      const sel=$('formSelect');
      active.sort((a,b)=>String(a.name||'').localeCompare(String(b.name||''),'he'));
      active.forEach(r=>{
        if(!r.pcfformid) return;
        const o=document.createElement('option');
        o.value=r.pcfformid;
        o.textContent=r.name||r.pcfformid;
        sel.appendChild(o);
      });
      $('formHint').textContent='"ברירת מחדל" שולחת את המסמך המקושר למוצר. אפשר לבחור מסמך אחר מהרשימה.';
    }catch(err){
      $('formHint').innerHTML='לא ניתן היה לטעון את רשימת המסמכים. תישלח ברירת המחדל (המסמך של העסקה).';
    }
  }

  function showSuccess(url){
    const s=$('status');
    s.className='success-big';
    let html='<span class="check">✓</span><span class="big">הטופס נשלח בהצלחה!</span>';
    if(url){
      html += `<br><a href="${url}" target="_blank" rel="noopener noreferrer">לחצי כאן לכניסה למסמך</a>`;
      html += `<div class="copy-row">
                 <input class="copy-url" id="copyUrl" readonly value="${url}">
                 <button class="copy-btn" id="copyBtn" type="button">העתקה</button>
               </div>`;
    }
    s.innerHTML=html;
    const cb=$('copyBtn');
    if(cb){
      cb.addEventListener('click',()=>{
        const val=$('copyUrl').value;
        const done=()=>{cb.textContent='הועתק ✓';setTimeout(()=>cb.textContent='העתקה',1500);};
        if(navigator.clipboard && navigator.clipboard.writeText){
          navigator.clipboard.writeText(val).then(done).catch(()=>{ $('copyUrl').select(); document.execCommand('copy'); done(); });
        }else{
          $('copyUrl').select(); document.execCommand('copy'); done();
        }
      });
    }
  }

  async function send(){
    const btn=$('sendBtn');
    if(!opportunityId){
      setStatus('לא נמצא מזהה עסקה. פתחי את הכפתור מתוך כרטיס תהליך מכירה.','err');
      return;
    }
    const opt=$('formSelect').selectedOptions[0];
    // 28/07: payload = 4 שדות בלבד. send_method קבוע.
    const payload={
      opportunity_id: opportunityId,
      form_id: $('formSelect').value,
      form_label: opt ? opt.textContent : '',
      send_method: 'whatsapp'
    };
    btn.disabled=true; setStatus('שולח את הטופס <span class="spin"></span>');
    try{
      const res=await fetchT(SEND_WEBHOOK_URL,{
        method:'POST',headers:{'Content-Type':'application/json'},
        body:JSON.stringify(payload)
      },20000);
      if(res.status!==200){
        setStatus(`השליחה נכשלה (קוד ${res.status}). נסי שוב.`,'err');
        btn.disabled=false; return;
      }
      let body={}; try{ body=await res.json(); }catch(e){}
      if(body.response==='success' || res.status===200){
        // דורש submission_url מסנריו B — טרם מיושם ב-Make
        showSuccess(body.submission_url || '');
        btn.style.display='none';
      }else{
        setStatus(`השליחה נכשלה (${body.response||'שגיאה'}). נסי שוב.`,'err');
        btn.disabled=false;
      }
    }catch(err){
      setStatus('השליחה נכשלה — בעיית תקשורת. נסי שוב.','err');
      btn.disabled=false;
    }
  }

  $('sendBtn').addEventListener('click',send);
  loadCatalog();
</script>
</body>
</html>
```
