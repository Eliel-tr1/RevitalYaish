# איך מוציאים את פרטי ה-Zoom S2S — 4 דקות

> צריך להיכנס עם **המשתמש שהוא Owner או Admin** בחשבון הזום של רויטל. משתמש רגיל לא רואה את המסך הזה.

## שלב 1 · יצירת האפליקציה

1. להיכנס ל-**https://marketplace.zoom.us** ולהתחבר עם חשבון הזום של רויטל.
2. בתפריט העליון מימין: **Develop → Build App**.
3. לבחור **Server-to-Server OAuth** → **Create**.
4. שם האפליקציה: `Vitrue · Fireberry Webinar Sync` → **Create**.

## שלב 2 · שלושת הערכים שאני צריך

מיד אחרי היצירה נפתח מסך **App Credentials**. שם יושבים בדיוק שלושת הערכים:

| מה שכתוב במסך | מה זה אצלי |
|---|---|
| **Account ID** | `ZOOM_ACCOUNT_ID` |
| **Client ID** | המשתמש ב-credential |
| **Client Secret** | הסיסמה ב-credential |

לחיצה על **Copy** ליד כל אחד. אלה שלושתם.

## שלב 3 · Information (חובה, אחרת אי אפשר להפעיל)

למלא **Company Name** ו-**Developer Contact Name + Email**. כל ערך תקין מתקבל.

## שלב 4 · Scopes — החלק שאם מפספסים אותו הכל נכשל

**Scopes → + Add Scopes**, ולסמן:

**Webinar**
- `View all user Webinars` / `webinar:read:admin`
- אם הממשק מציג הרשאות מפורטות (granular) — לסמן את כל אלה:
  `webinar:read:webinar:admin` · `webinar:read:list_registrants:admin` ·
  `webinar:read:list_past_instances:admin` · `webinar:read:list_absentees:admin`

**Report**
- `View report data` / `report:read:admin`
- ובגרסה המפורטת:
  `report:read:webinar:admin` · `report:read:list_webinar_participants:admin` ·
  `report:read:list_webinar_qa:admin` · `report:read:list_webinar_polls:admin`

> ⚠️ **`report` הוא הקריטי.** בלעדיו אין נוכחות, אין משך, אין כלום — רק שמות הוובינרים.

## שלב 5 · הפעלה

**Activation → Activate your app**. חייב להיות ירוק.

## שלב 6 · מזהה הוובינר

מספר בן 10–11 ספרות. שתי דרכים:
- **מהלינק** של הוובינר: `https://zoom.us/j/`**`88012345678`**`?pwd=…` — החלק המודגש.
- **מהממשק**: zoom.us → Webinars → הוובינר → `Webinar ID`.

להוריד רווחים ומקפים. `880 1234 5678` → `88012345678`.

## מה לשלוח לי

```
ZOOM_ACCOUNT_ID  = ...
ZOOM_CLIENT_ID   = ...
ZOOM_SECRET      = ...
ZOOM_WEBINAR_ID  = ...
```

---

## שתי בדיקות שכדאי לעשות תוך כדי

**1. זה בכלל Webinar ולא Meeting?**
בתפריט הצד של zoom.us — אם יש **Webinars** בנפרד מ-**Meetings**, יש רישיון וובינר. אם יש רק Meetings, מה שרץ ברביעי הוא פגישה רגילה, ואז אין `registrants`, אין `absentees` ואין Q&A. תגיד לי ואני מסיט את ה-workflow למסלול ה-Meetings.

**2. ההרשמה בזום דלוקה?**
בהגדרות הוובינר → **Registration**. אם היא כבויה — נקבל שמות מוקלדים בלבד, וחצי מהמשתתפות לא יזוהו כלקוחות. **ההמלצה שלי: להדליק, ולהוסיף שאלה מותאמת "טלפון נייד".** המנוע כבר יודע לקרוא אותה ולהצליב מול הלקוחה. מסך ההרשמה לא מוסיף חיכוך ללקוחה, כי הלינק האישי שנשלח לה עוקף אותו.
