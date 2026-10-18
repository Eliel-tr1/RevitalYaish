// ============================================================================
// WF-20 · צומת 1 — נירמול וסיווג ה-webhook שהתקבל מגרואו
// ============================================================================
// כל הלוגיקה כאן טהורה (LOGIC) כדי שניתן יהיה לבדוק אותה מחוץ ל-n8n.
// ============================================================================

// ==== CONFIG ====
const CFG = {
  // 🔴 עלייה לאוויר 19/08/2026 באישור אליאל — הכתיבה פתוחה לכל הלקוחות.
  //    להחזרה למצב בדיקה: DRY_RUN = true. אז רק החשבונות שברשימות
  //    LIVE_TEST_PHONES / LIVE_TEST_ACCOUNT_IDS ימשיכו להיכתב.
  DRY_RUN: false,
  VAT_PERCENT: 18,                     // אחוז מע"מ
  N8N_BASE: 'https://n8n.srv964196.hstgr.cloud',
  FIREBERRY_BASE: 'https://api.fireberry.com',
  // האם ליצור "תיעוד תשלום" כבר בהקמת הוראת קבע.
  // האפיון של אליאל אומר שלא — החיוב הראשון מגיע בנפרד כאירוע חיוב.
  CREATE_DOC_ON_STANDING_ORDER_SETUP: false,
  // וורקפלואו הקמת המוצרים בפיירברי — טרם נוצר. השארת נקודת חיבור.
  // 🔗 סיום תשלום מוצלח מפעיל את WF-22 — הראוטר של התהליכים המקצועיים.
  PRODUCT_SETUP_WEBHOOK_URL: 'https://n8n.srv964196.hstgr.cloud/webhook/pro-setup-roital',
  DEFAULT_TASK_PRIORITY: 5,            // גבוהה
  DEFAULT_TASK_TYPE: 5,                // מכירה
  DEFAULT_TASK_STATUS: 1,              // פתוח
  EMPTY_GUID: '00000000-0000-0000-0000-000000000000',

  // ── 🔴 חשבונות בדיקה מורשים לכתיבה בפועל ─────────────────────────────
  // כל תשלום ששייך לאחד מאלה ירוץ *מלא* — הרשומות ייווצרו בפיירברי —
  // גם כאשר DRY_RUN=true. כל שאר הלקוחות נשארים בתצוגה מקדימה בלבד.
  // הוגדר לבקשת אליאל 19/08/2026 כדי לראות את התוצאה בפועל על חשבון סער.
  LIVE_TEST_PHONES: [],                                  // 12/09 — לייב לכולם, רשימת הבדיקה רוקנה
  // 🔴 20/08 — רשומת הלקוחה של סער נמחקה לצורך טסט מאפס. המזהה כאן יתעדכן
  //    לרשומה החדשה ברגע שתיווצר. הוא נחוץ במיוחד לוובהוק החשבונית, שאינו
  //    נושא טלפון כלל ולכן מזוהה רק דרך הלקוחה שברשומת התשלום.
  LIVE_TEST_ACCOUNT_IDS: [],
  // 🔴 זיהוי לפי **שם הלקוחה** — שורד מחיקה ויצירה מחדש של רשומת הלקוחה.
  //    נחוץ במיוחד לוובהוק החשבונית, שאינו נושא טלפון ולכן מזוהה רק דרך
  //    הלקוחה שברשומת התשלום. (נוסף 20/08 אחרי מחיקת רשומת הבדיקה.)
  LIVE_TEST_ACCOUNT_NAMES: [],

  // 🔴 חשבונית שלא ניתן לשייך לאף תשלום — תמיד רצה בפועל, ופותחת משימה בלבד.
  // הסיבה: ה-payload של החשבונית מכיל שלושה שדות ואין בו לקוחה, ולכן היא לא
  // יכולה לעבור את רשימת ההיתר. בלי זה המסמך נעלם בשקט. המשימה אינה רשומה
  // כספית ולכן בטוחה גם ללקוחות אמיתיות.
  ALWAYS_LIVE_UNMATCHED_INVOICE: true,

  // ── 🔴🔴 שיוך לפי קרבת זמן — הוסר לחלוטין ב-20/08/2026 ────────────────
  //    הכלל, בלי יוצא מן הכלל ובלי מתג:
  //        שיוך של תשלום או של מסמך חשבונאי נעשה אך ורק לפי מזהה חד-ערכי.
  //    אין חלון זמן · אין "המועמד היחיד" · אין "האחרון שנוצר" · אין ניחוש לפי סכום.
  //    (רקע: חשבונית של לקוחה אחת שויכה לתשלום של לקוחה אחרת.)

  // תווית סוג המסמך לפי קידומת מספר המסמך. ברירת המחדל כשאין התאמה.
  DOC_TYPE_DEFAULT: 'מסמך חשבונאי',
  // סוג המסמך נגזר מסדרת המספור של גרואו. אומת ע"י אליאל 19/08/2026
  // מתוך פתיחת המסמכים עצמם.
  DOC_TYPE_BY_PREFIX: {
    '49': 'חשבונית מס/קבלה',   // מסמך משולב — נפוץ בתשלום בודד
    '25': 'חשבונית מס',        // הראשון מבין הזוג בפריסת תשלומים
    '50': 'קבלה',              // השני מבין הזוג
    '60': 'חשבונית זיכוי',     // 🔴 טעון אימות מול אליאל — נצפה בזיכוי 20/08
  },

  // 🔴 מספרי הטלפון של העסק עצמו, כפי שהם מודפסים על גבי המסמכים.
  //    הם מסוננים מזיהוי הטלפון ב-PDF, אחרת נזהה את רויטל כלקוחה.
  DOC_OWN_PHONES: ['0524153323'],

  // האם לקרוא את ה-PDF של המסמך כדי לחלץ ממנו טלפון ומספר מסמך מקורי
  PARSE_DOCUMENT_PDF: true,

  // 🔴 המתנה לפני שיוך מסמך, בשניות.
  //    גרואו שולחת את הרכישה בשני פורמטים; רק השני נושא את מזהה העסקה
  //    שמשלים את רשומת התשלום. וובהוק החשבונית מגיע לעיתים ביניהם.
  //    אומת חי 23/08 — פער של שנייה עד 6 שניות. 25 שניות = פי 4 מרווח,
  //    ועדיין בתוך הטיימאאוט המקובל של וובהוק כך שגרואו לא תשלח שוב.
  //    0 = בלי המתנה.
  INVOICE_SYNC_WAIT_SECONDS: 25,

  // 🔴 רישום סכום הזיכוי על רשומת התשלום. אושר ע"י אליאל 20/08/2026.
  //    נכתב **רק** כשהתשלום זוהה מתוך מספר המסמך המודפס בזיכוי, והסכום נקרא.
  WRITE_REFUND_ON_CREDIT: true,

  // 🔴 מסמך שלא ניתן לשייך — האם בכל זאת ליצור לו רשומה בפיירברי?
  //    true  = הרשומה נוצרת בלי שיוך + משימה לשיוך ידני (ברירת המחדל).
  //    false = משימה בלבד, המסמך לא נשמר בשום מקום.
  CREATE_UNMATCHED_DOCUMENT: true,

  // בחירת תהליך המכירה:
  //   true  = רק תהליך מכירה פתוח שהמוצר שלו זהה למוצר שנרכש; אין כזה —
  //           נפתח תהליך מכירה חדש. (הכרעת אליאל 14/09/2026:
  //           "זה אמור להתלות על המוצר שנבחר במעמד הסליקה")
  //   false = תהליך המכירה הפתוח העדכני ביותר, בלי קשר למוצר (התנהגות 19/08)
  // 🔴 לפני 14/09 הדגל היה false, ולכן רכישת ליווי של לקוחה עם ליד בוסט פתוח
  //    נתלתה על ליד הבוסט — ו-WF-22 דרס בו את המוצר וסגר אותו.
  SALE_MATCH_BY_PRODUCT: true,

  // 🔴 15/09/2026 — הכרעת אליאל: תהליכי המכירה מסודרים לפי **קטגוריית המוצר**
  //    (בוסט / פרימיום / המשך), לא לפי המוצר המדויק. כשמתקבל תשלום ויש תהליך
  //    מכירה פתוח **מאותה קטגוריה** — משייכים אליו, גם אם המוצר שונה, ומעדכנים
  //    בו את המוצר לפי מה שנסלק בפועל. לא פותחים תהליך חדש.
  //    דוגמה: ליד פתוח על "תוכנית המשך אונליין" + תשלום על "תוכנית המשך אישית"
  //    ⇒ אותו תהליך מכירה, המוצר מתעדכן לאישית.
  SALE_MATCH_BY_CATEGORY: true,

  // 🔴 15/09/2026 — חיפוש תהליך מכירה גם בין ה**סגורות**.
  // בלי זה כל חיוב הו"ק חוזר (שמגיע אחרי שהעסקה כבר "נסגרה בהצלחה") פתח
  // עסקה חדשה, וזה בדיוק המקור לכפילויות שאוחדו. הסטטוס של העסקה הסגורה
  // לא משתנה — רק נתלים עליה.
  SALE_MATCH_INCLUDE_CLOSED: true,

  // 🔴 16/09/2026 — ליד פתוח בלי מוצר קולט את הרכישה במקום שתיפתח עסקה חדשה.
  SALE_MATCH_EMPTY_LEAD: true,

  // מרווח בין תשלומים בפריסה, בחודשים. גרואו לא שולח את תאריכי החיוב
  // העתידיים — הם נגזרים מתאריך התשלום הראשון. (החלטת אליאל 19/08/2026)
  INSTALLMENT_INTERVAL_MONTHS: 1,

  // חיוב הוראת קבע שאין לו רשומת הוראה בפיירברי — האם ליצור אותה רטרואקטיבית.
  // true = הכסף נרשם ונפתחת משימת אימות. false = משימה בלבד, בלי רשומה כספית.
  // 🔴 כבוי מ-19/08 בהוראת אליאל, עד לאחר מעבר הנתונים מה-CRM הישן (04–05/09).
  //    ב-GROW יש 238 הוראות קבע פעילות ו-330 פריסות אשראי פתוחות שהוקמו לפני
  //    שהמערכת הזו עלתה. המיגרציה תיצור להן רשומות תשלום מה-CRM הישן.
  //    אם הריפוי העצמי היה דלוק, כל חיוב שנכנס בינתיים היה יוצר רשומה
  //    רטרואקטיבית שהמיגרציה תשכפל. במקום זה — משימה בלבד, בלי רשומה כספית.
  //    ⚠️ להדליק בחזרה אחרי שהמיגרציה הושלמה ואומתה.
  //    ⚠️ הודלק מחדש 20/08 בהוראת אליאל ("אני לא רוצה שזה יאבד ולא ירשם"),
  //    עם מפתח איחוד ודאי: pcfID = מזהה ההו"ק בגרואו. במעבר הנתונים יש לאחד
  //    לפי המפתח הזה ולא ליצור רשומה שנייה.
  SELF_HEAL_STANDING_ORDER: true,

  // 🔴 סימון לרשומות שנוצרו רטרואקטיבית מתוך חיוב — כדי שיהיה אפשר לאתר
  //    ולאחד אותן במעבר הנתונים.
  RETRO_PREFIX: '[רטרו — לאיחוד במעבר] ',

  // 🔴 מקורות תשלום שמעידים שההוראה **הוקמה עכשיו** ולא נגבתה ע"י המנוע.
  //    אומת חי 20/08: הקמה חדשה מגיעה עם paymentSource="Payment Links",
  //    בעוד חיוב חוזר של הוראה קיימת מגיע עם "מערכת חיצונית".
  STANDING_ORDER_SETUP_SOURCES: ['payment links', 'עמוד תשלום', 'payment page'],

  // 🔴 הו"ק שהוקמה **ידנית מתוך מערכת גרואו** (בק-אופיס), ולא דרך עמוד תשלום.
  //    גרואו שולחת אותה בדיוק כמו חיוב חוזר — paymentSource="מערכת חיצונית" —
  //    ולכן היא זוהתה עד 14/09/2026 כחיוב של הוראה ותיקה, ושרשרת הקמת המוצר
  //    לא רצה. המבחין היחיד והאמין: **מזהה ההו"ק אינו מוכר לפיירברי**.
  //    אומת על 250 ריצות: 30 חיובים ותיקים הגיעו כולם עם "ריצת הוראת קבע",
  //    ו-5 הקמות מהבק-אופיס הגיעו כולן עם "מערכת חיצונית". הפרדה מלאה.
  STANDING_ORDER_BACKOFFICE_SOURCES: ['מערכת חיצונית'],

  // 🔴 מספר התשלומים ברשומת הוראת קבע.
  // האפיון ביקש 0, אבל **פיירברי קורס** כשמגיעים 0 יחד עם סכום:
  // השדה המחושב "כל תשלום לפני מע\"מ" מחלק את הסכום במספר התשלומים,
  // וחלוקה באפס מחזירה "An internal error has occured" (HTTP 400).
  // אומת בבידוד 19/08. null = לא לשלוח את השדה כלל (הוא נשאר ריק, וזה נכון
  // סמנטית — להוראת קבע אין מספר תשלומים ידוע מראש).
  // 🔴 "מספר תשלומים = 0" בגוף יצירה (POST) + סכום ⇒ פיירברי מחזיר 400
  //    (השדה המחושב "כל תשלום לפני מע\"מ" מחלק באפס).
  //    **אותו ערך בעדכון (PUT) עובר תקין.** לכן ההוראה נוצרת בלי השדה,
  //    ומיד אחריה פעולת עדכון כותבת בו 0. אליאל אישר 19/08 שהשדה המחושב
  //    לא חייב להתחשב — העיקר שהערך יופיע.
  STANDING_ORDER_PAYMENTS_COUNT: 1,
  STANDING_ORDER_COUNT_VIA_UPDATE: true,
  // 🔴 שיוך חיוב לתיעוד תשלום נעשה **אך ורק לפי מזהה**. כלל קשיח, בלי מתג:
  //    לא נמצא מזהה תואם ⇒ לא נוגעים בשום רשומה, נפתחת משימה.

  // ── מזהי GROW נוספים למוצר ────────────────────────────────────────────
  // לחלק מהמוצרים יש בגרואו יותר ממזהה אחד (מוצר כפול / כמה עמודי מכירה).
  // כאן ממפים מזהה שמגיע בוובהוק → הערך שיושב ב-pcfpaymentpageid בפיירברי.
  // אומת חי 19/08: הבוסט נסלק דרך מוצר 618998 / עמוד 3753502,
  // בעוד שבפיירברי רשומים 618977 / עמוד 3753607. שניהם "עמוד מכירה בוסט".
  // ריק — 19/08/2026 תוקן הנתון עצמו: pcfpaymentpageid של "סדנה בוסט"
  // עודכן מ-618977 ל-618998, שהוא מזהה המוצר שגרואו שולח בפועל.
  // הטבלה נשארת כמנגנון למקרה שיתגלה מוצר עם יותר ממזהה אחד.
  PRODUCT_ID_ALIASES: {},

  // ── מיפוי שמות מוצרים מהמערכת הישנה → מזהה מוצר בפיירברי ──────────────
  // במערכת הישנה שמות המוצרים בגרואו לא זהים לשמות בקטלוג החדש, ולכן
  // ההתאמה לפי טוקנים נכשלה והתשלום נשאר בלי מוצר. אליאל מסר את המיפוי
  // הידני, 15/09/2026. ההשוואה היא על **מחרוזת מלאה מנורמלת** (בלי
  // מקפים/גרשיים/רווחים כפולים) — לא "מכיל", כדי ש-"ליווי" לבדו לא יבלע
  // כל שם אחר.
  PRODUCT_NAME_ALIASES: {
    'ליווי תזונה אונליין רגיל': '58A4D4F9-5921-4BFC-BA8E-518877FAA375',          // תוכנית המשך אונליין
    'ליווי תזונה אונליין מנטורית אישית': 'D2CE0670-275A-4EF9-96BA-167F5CA053D6', // תוכנית המשך אישית
    'ליווי אונליין מנטורית אישית': '58A4D4F9-5921-4BFC-BA8E-518877FAA375',       // תוכנית המשך אונליין
    'ליווי': '58A4D4F9-5921-4BFC-BA8E-518877FAA375',                             // תוכנית המשך אונליין
  },

  // ── מפתחות הוובהוק של גרואו → סוג האירוע ──────────────────────────────
  // גרואו שולח בכל payload את מפתח הוובהוק שדרכו הוא נשלח. זהו מקור הניתוב
  // הראשון והמהימן ביותר — עדיף על ניחוש לפי מבנה ה-payload.
  // הוגדרו ע"י אליאל בחשבון של רויטל, 19/08/2026.
  WEBHOOK_KEYS: {
    'a3e4507c-1c47-c26b-2abb-c1dbdc894825': 'INVOICE',          // הפקת חשבונית
    '49e11133-7633-db07-e030-51addc8bc5aa': 'RECURRING_FAILED', // הוראת קבע שנכשלה
    'c7c0105e-ac70-969a-bea3-16ac05f64ea9': 'PAYMENT',          // כל העסקאות חוץ מהו"ק
    '9a6e5e82-e4a8-370c-d701-1a6838c8dbdb': 'STANDING_ORDER',   // הו"ק — הקמה וחיובים
  },
};

// ==== LOGIC (pure) ====
function LOGIC(ctx) {
  const cfg = ctx.cfg;
  const items = ctx.items || [];
  const first = items[0] ? items[0].json : {};

  // --- 1. חילוץ ה-payload מכל העטיפות האפשריות ---
  let raw = (first && first.body !== undefined) ? first.body : first;
  if (typeof raw === 'string') {
    try { raw = JSON.parse(raw); } catch (e) { /* נשאר מחרוזת */ }
  }
  if (Array.isArray(raw)) raw = raw[0] || {};
  if (!raw || typeof raw !== 'object') raw = {};

  // גרואו — מערכת paymentLinks עוטפת ב-{err,status,data}
  const isWrapped = Object.prototype.hasOwnProperty.call(raw, 'data') &&
                    raw.data && typeof raw.data === 'object' && !Array.isArray(raw.data);
  const d = isWrapped ? raw.data : raw;

  // --- 2. עזרים ---
  const S = (v) => (v === undefined || v === null) ? '' : String(v).trim();
  const num = (v) => {
    if (v === undefined || v === null || v === '') return 0;
    const n = parseFloat(String(v).replace(/[^\d.\-]/g, ''));
    return isNaN(n) ? 0 : n;
  };
  const round2 = (n) => Math.round((Number(n) + Number.EPSILON) * 100) / 100;
  // הנטו נשמר בארבע ספרות — פיירברי מחשב ממנו מחדש את הסכום כולל מע"מ.
  const round4 = (n) => Math.round((Number(n) + Number.EPSILON) * 10000) / 10000;

  function normPhone(p) {
    let digits = S(p).replace(/\D/g, '');
    if (!digits) return '';
    if (digits.startsWith('972')) digits = '0' + digits.slice(3);
    else if (digits.startsWith('00972')) digits = '0' + digits.slice(5);
    if (digits.length === 9 && !digits.startsWith('0')) digits = '0' + digits;
    return digits;
  }

  // גרואו שולח dd/MM/yy (וגם d/M/yy). מחזיר ISO עם סיומת Z (פיירברי שומר שעה מקומית עם Z).
  function growDateToISO(s) {
    const t = S(s);
    if (!t) return '';
    const m = t.match(/^(\d{1,2})\/(\d{1,2})\/(\d{2,4})$/);
    if (m) {
      let [, dd, mm, yy] = m;
      let year = parseInt(yy, 10);
      if (yy.length === 2) year += 2000;
      const p = (x) => String(parseInt(x, 10)).padStart(2, '0');
      return `${year}-${p(mm)}-${p(dd)}T00:00:00Z`;
    }
    const dt = new Date(t);
    if (!isNaN(dt.getTime())) return dt.toISOString().replace(/\.\d{3}Z$/, 'Z');
    return '';
  }

  const nowISO = ctx.now || new Date().toISOString().replace(/\.\d{3}Z$/, 'Z');
  const todayISO = nowISO.slice(0, 10) + 'T00:00:00Z';

  // --- 3. סיווג סוג האירוע ---
  // הערה קריטית: לגרואו ארבעה מבנים שונים לחלוטין.
  //   INVOICE           = {transactionCode, invoiceNumber, invoiceUrl}  (3 שדות בלבד)
  //   RECURRING_FAILED  = snake_case {regular_payment_id, error_message, charges_attempts, ...}
  //   RECURRING_CHARGE  = שטוח, עם directDebitId / paymentSource="ריצת הוראת קבע"
  //   PAYMENT           = paymentLinks (עטוף ב-data) או legacy/API שטוח
  const hasInvoiceFields = !!(S(raw.invoiceUrl) || S(raw.invoiceNumber) || S(d.invoiceUrl) || S(d.invoiceNumber));
  const hasPayerFields   = !!(S(d.fullName) || S(d.payerPhone) || S(d.sum) || S(d.paymentSum));
  const isFailedRecur    = !!(S(raw.regular_payment_id) || S(raw.charges_attempts) || S(raw.error_message));

  const paymentTypeRaw  = S(d.paymentType);
  const paymentSource   = S(d.paymentSource);
  const directDebitId   = S(d.directDebitId) || S(d.recurringDebitId) || S(raw.regular_payment_id);
  const isStandingLabel = /הוראת\s*קבע/.test(paymentTypeRaw) || /הוראת\s*קבע/.test(S(d.transactionType));
  const isRecurRun      = /ריצת\s*הוראת\s*קבע/.test(paymentSource);
  // 🔴 האם ההוראה הוקמה ברגע זה (לקוחה עברה בעמוד תשלום) או שזהו חיוב חוזר
  //    שמנוע גרואו הריץ. זה ההבדל בין "רכישה חדשה" ל"חיוב של הוראה ותיקה".
  const setupSources    = (cfg.STANDING_ORDER_SETUP_SOURCES || []).map((x) => String(x).toLowerCase());
  const isSetupSource   = !isRecurRun && !!paymentSource &&
                          setupSources.indexOf(paymentSource.toLowerCase()) !== -1;
  const boSources       = (cfg.STANDING_ORDER_BACKOFFICE_SOURCES || []).map((x) => String(x).toLowerCase());
  const isBackOfficeSource = !isRecurRun && !isSetupSource && !!paymentSource &&
                          boSources.indexOf(paymentSource.toLowerCase()) !== -1;

  // ── מקור ניתוב ראשון: מפתח הוובהוק שגרואו שולח ──
  const webhookKey = S(d.webhookKey) || S(d.webhook_key) || S(raw.webhookKey) || S(raw.webhook_key);
  const keyedType = webhookKey ? (cfg.WEBHOOK_KEYS[webhookKey] || null) : null;
  const keyWarnings = [];
  if (webhookKey && !keyedType) {
    keyWarnings.push(`מפתח הוובהוק ${webhookKey} אינו מוכר — הסיווג נעשה לפי מבנה ה-payload. יש להוסיף אותו ל-WEBHOOK_KEYS.`);
  }
  if (!webhookKey) {
    keyWarnings.push('ה-payload הגיע בלי מפתח וובהוק — הסיווג נעשה לפי מבנה ה-payload בלבד.');
  }

  let eventType, classifiedBy = 'webhookKey';
  if (keyedType === 'INVOICE') {
    eventType = 'INVOICE';
  } else if (keyedType === 'RECURRING_FAILED') {
    eventType = 'RECURRING_FAILED';
  } else if (keyedType === 'STANDING_ORDER') {
    // אותו מפתח משרת גם הקמה וגם חיוב חודשי — ההפרדה לפי סימני חיוב חוזר
    eventType = (isRecurRun || directDebitId) ? 'RECURRING_CHARGE' : 'STANDING_ORDER_SETUP';
  } else if (keyedType === 'PAYMENT') {
    // המפתח מוגדר "כל העסקאות חוץ מהו״ק". אם בכל זאת הגיעה הו״ק — ה-payload גובר,
    // כי יצירת הו״ק כתשלום רגיל היא שגיאה כספית ולא רק שגיאת סיווג.
    if (isRecurRun || (directDebitId && isStandingLabel)) {
      eventType = 'RECURRING_CHARGE';
      keyWarnings.push('הוובהוק "כל העסקאות חוץ מהו״ק" קיבל חיוב הוראת קבע — הסיווג תוקן לפי ה-payload.');
    } else if (isStandingLabel) {
      eventType = 'STANDING_ORDER_SETUP';
      keyWarnings.push('הוובהוק "כל העסקאות חוץ מהו״ק" קיבל הקמת הוראת קבע — הסיווג תוקן לפי ה-payload.');
    } else {
      eventType = 'PAYMENT';
    }
  } else {
    // ── נפילה: סיווג לפי מבנה ה-payload ──
    classifiedBy = 'heuristic';
    if (isFailedRecur)                        eventType = 'RECURRING_FAILED';
    else if (hasInvoiceFields && !hasPayerFields) eventType = 'INVOICE';
    else if (isRecurRun || (directDebitId && isStandingLabel && !isWrapped && !S(d.productData))) eventType = 'RECURRING_CHARGE';
    else if (isStandingLabel)                 eventType = 'STANDING_ORDER_SETUP';
    else if (hasPayerFields)                  eventType = 'PAYMENT';
    else                                      eventType = 'UNKNOWN';
  }

  // חיוב ראשון של הוראת קבע מגיע כאירוע "תשלום רגיל" ולא כאירוע recurring (מתועד בפלייבוק).
  // לכן STANDING_ORDER_SETUP מכסה גם אותו.

  // --- 4. הצלחה / כישלון ---
  // paymentLinks: status="שולם" / statusCode="2".  legacy/recurring: אין שדה סטטוס כלל —
  // גרואו יורה את הוובהוק רק על הצלחה, ולכשל יש וובהוק נפרד. לכן היעדר סטטוס = הצלחה.
  const statusLabel = S(d.status);
  const statusCode  = S(d.statusCode);
  let isSuccess;
  if (eventType === 'RECURRING_FAILED') isSuccess = false;
  else if (statusLabel || statusCode)   isSuccess = (statusLabel === 'שולם' || statusCode === '2');
  else                                  isSuccess = true;

  // --- 5. סכומים ---
  const grossTotal = round2(num(d.sum) || num(d.paymentSum) || num(raw.sum) || 0);
  const vatDiv     = 1 + (cfg.VAT_PERCENT / 100);
  const netTotal   = round4(grossTotal / vatDiv);
  const periodicalGross = round2(num(d.periodicalPaymentSum) || 0);
  const firstPayGross   = round2(num(d.firstPaymentSum) || 0);

  // --- 6. מספר תשלומים ---
  // ⚠️ גוצ'ה: paymentLinks שולח allPaymentsNum (עם s), legacy שולח allPaymentNum (בלי s).
  // ⚠️ גוצ'ה: גרואו שולח "0" כמספר תשלומים בעסקה בודדת. "0" הוא truthy במחרוזת — || נכשל.
  const allRaw = (d.allPaymentsNum !== undefined && d.allPaymentsNum !== '') ? d.allPaymentsNum
               : (d.allPaymentNum !== undefined && d.allPaymentNum !== '') ? d.allPaymentNum : '';
  let installmentsTotal = parseInt(S(allRaw), 10);
  if (!installmentsTotal || installmentsTotal < 1) installmentsTotal = 1;
  // ⚠️ אומת חי 19/08: `paymentsNum` אינו אינדקס התשלום הנוכחי אלא **מספר החיובים
  // המחזוריים שאחרי הראשון**. עסקה ב-4 תשלומים שלחה allPaymentsNum=4, paymentsNum=3.
  const periodicalCountRaw = S(d.paymentsNum);
  const periodicalCount = periodicalCountRaw === '' ? 0 : (parseInt(periodicalCountRaw, 10) || 0);

  // --- 7. אמצעי תשלום (פיקליסט פיירברי 1039/1018.pcfPaymentType) ---
  // ⚠️ אין להסתמך על d.paymentType של גרואו — מתועד שהוא שלח "2" על עסקת ויזה ודאית.
  const cardSuffix = S(d.cardSuffix) || S(raw.card_suffix);
  const cardBrand  = S(d.cardBrand);
  const descBlob   = [S(d.description), S(d.paymentDesc), S(d.transactionType), paymentTypeRaw].join(' ');
  let fbPaymentType;
  if (eventType === 'STANDING_ORDER_SETUP') fbPaymentType = 7;          // הוראת קבע
  else if (cardSuffix || cardBrand)         fbPaymentType = 1;          // אשראי
  else if (/ביט|bit/i.test(descBlob))       fbPaymentType = 6;          // העברה ב Bit
  else if (/העברה\s*בנקאית/.test(descBlob)) fbPaymentType = 2;
  else                                      fbPaymentType = 1;          // ברירת מחדל — אשראי

  // --- 8. מוצרים ---
  // price_mark="1" = שורת הנחה/קופון — חובה לסנן.
  const productRows = Array.isArray(d.productData) ? d.productData : [];
  const realProducts = productRows.filter((p) => S(p && p.price_mark) !== '1');
  const primaryProduct = realProducts.find((p) => S(p.product_id) && S(p.product_id) !== '0') || realProducts[0] || null;
  // ── קופון / הנחה ────────────────────────────────────────────────────
  // גרואו מסמן שורת הנחה ב-price_mark="1". השם הוא שם הקופון והמחיר הוא
  // סכום ההנחה. כשגרואו לא מפרט שורה כזו — ההנחה נגזרת מהפרש בין מחיר
  // המחירון של שורות המוצר לבין הסכום שנגבה בפועל.
  const discountRows = productRows.filter((p) => S(p && p.price_mark) === '1');
  const lineTotal = (r) => num(r && r.price) * (num(r && r.quantity) || 1);
  const listedTotal = round2(realProducts.reduce((a, r) => a + lineTotal(r), 0));
  let couponCode = discountRows.length ? S(discountRows[0].name) : '';
  let couponDiscount = discountRows.length
    ? round2(discountRows.reduce((a, r) => a + Math.abs(lineTotal(r)), 0))
    : 0;
  let couponSource = discountRows.length ? 'שורת הנחה מגרואו' : '';
// הנחה נגזרת — רק אם גרואו לא פירט שורת הנחה, ויש פער אמיתי מול המחירון
  if (!couponDiscount && listedTotal > 0 && grossTotal > 0 && listedTotal - grossTotal > 0.01) {
    couponDiscount = round2(listedTotal - grossTotal);
    couponSource = 'חושב מהפרש מול מחיר המחירון';
  }
  const growProductId   = primaryProduct ? S(primaryProduct.product_id) : '';
  const growProductName = primaryProduct ? S(primaryProduct.name) : '';
  // מזהה עמוד/קישור התשלום בגרואו. בחשבון של רויטל היו בעבר ערכים מסוג זה
  // בשדה pcfpaymentpageid, ולכן מחפשים את המוצר לפי שני המפתחות במקביל.
  const growProcessId   = S(d.paymentLinkProcessId) || S(d.processId);

  // --- 9. מזהים ---
  const transactionId   = S(d.transactionId);
  const transactionCode = S(d.transactionCode) || S(raw.transactionCode);
  const asmachta        = S(d.asmachta);
  const invoiceNumber   = S(raw.invoiceNumber) || S(d.invoiceNumber);
  const invoiceUrl      = S(raw.invoiceUrl) || S(d.invoiceUrl) || S(raw.invoiceURL) || S(d.invoiceURL);
  // מזהה שיוצג כ"מזהה חיוב" ברשומה. עדיפות למזהה המספרי של גרואו.
  const chargeId = transactionId || transactionCode || asmachta;

  // ── מפתח האידמפוטנטיות ─────────────────────────────────────────────────
  // 🔴 אומת חי 19/08/2026: אותה עסקה מגיעה פעמיים בשני פורמטים שונים —
  //    paymentLinks (דרך Make) עם transactionId בלבד, ו-legacy (ישירות מגרואו)
  //    עם transactionCode בלבד. **asmachta זהה בשניהם** ולכן היא המפתח היחיד
  //    שמונע יצירת שתי רשומות תשלום על אותו כסף.
  const idemKeyBase = eventType === 'INVOICE'
    ? `GROW-INV-${invoiceNumber || transactionCode}`
    : `GROW-${asmachta || transactionId || transactionCode}`;

  const phone = normPhone(d.payerPhone || raw.phone || d.phone);

  return [{
    json: {
      _cfg: cfg,
      _raw: raw,
      _d: d,

      eventType,
      isSuccess,
      isWrapped,

      // אבחון ניתוב
      webhookKey,
      webhookKeyLabel: keyedType || '',
      classifiedBy,
      keyWarnings,

      // צד לקוח
      phone,
      fullName: S(d.fullName) || S(raw.payer_name),
      email: S(d.payerEmail) || S(raw.email),

      // כספים
      grossTotal, netTotal, periodicalGross, firstPayGross,
      vatPercent: cfg.VAT_PERCENT,

      // פריסה
      installmentsTotal, periodicalCount,

      // אמצעי
      fbPaymentType, cardSuffix, cardBrand,

      // מוצר
      growProductId, growProductName, growProcessId,
      couponCode, couponDiscount, couponSource, listedTotal,
      // תיאור העסקה / שם עמוד המכירה — מקור ההתאמה האחרון כשאין productData כלל
      // (הפורמט הישיר של גרואו לא נושא מוצרים, רק paymentDesc).
      descriptionText: S(d.paymentDesc) || S(d.description),
      productCount: realProducts.length,

      // מזהים
      transactionId, transactionCode, asmachta, directDebitId, chargeId,
      paymentSource, isSetupSource, isBackOfficeSource, isRecurRun,
      invoiceNumber, invoiceUrl,
      identifyParam: S(d.identifyParam) || S(raw.identifyParam),
      idemKeyBase,

      // תאריכים
      paymentDateISO: growDateToISO(d.paymentDate) || todayISO,
      nowISO, todayISO,

      // שגיאת חיוב חוזר
      failureMessage: S(raw.error_message),
      chargeAttempts: S(raw.charges_attempts),

      // ריצה
      executionUrl: ctx.executionUrl || '',
      DRY_RUN: cfg.DRY_RUN,
    },
  }];
}

// ==== N8N BINDING ====
const __ctx = {
  cfg: CFG,
  items: $input.all(),
  now: new Date().toISOString().replace(/\.\d{3}Z$/, 'Z'),
  executionUrl: `${CFG.N8N_BASE}/workflow/${$workflow.id}/executions/${$execution.id}`,
};
return LOGIC(__ctx);
