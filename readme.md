# SyncMe

`Open University of Israel, Workshop in Computer Communications, 2023`

`By Guy Strauss (207253899)`


## תוכן עניינים
 - [הקדמה](##הקדמה)

## הקדמה
התוכנה SyncMe מטרתה סינכרון של תיקיות וקבצים בין מספר בלתי מוגבל של מחשבי קצה. תוך כדי שמירה על יעילות, מהירות והרמטיות המידע בין כולם.
לאחר הגדרת התיקייה שאנו רוצים לגבות. התוכנה רצה ברגע ועושה את כל הפעולות הנ״ל מבלי לפגוע בחווית המשתמש. ותסכנרן בזמן אמת את כל השינויים הנעשים ע״י המשתמש(ים). השינויים הנתמכים הם:
1. יצירה, מחיקה, עדכון של תוכן קבצים ותיקיות
2. שינוי שם לקבצים
> [!important]
יש שימוש רב במושגים משתמשים, מחשבים ועמדות קצה. לצורך ההברה. הנחת הבסיס בפרויקט זה שעבור מספר כלשהו של מחשבים (או עמדות קצה) מספר המשתמשים הוא אחד - אותו משתמש עובד מכמה מחשבים שונים
## דרישות קדם
### צד שרת
המכונה צריכה לתמוך בהרצת `docker` (כלומר, יש לוודא שהמעבד תומך ב-hypervisor)
### צד לקוח
`python3.10`
## בחינת פתרונות אפשריים
לפני פיתוח הפיתרון המוצא. חיפשתי מספר דרכים לפתור את הבעיה של סנכרון קבצים, אציג כעת כמה דוגמאות ומה היתרונות והחסרונות של כל דוגמא
> [!note]
> כאשר אנו מדברים על פתרונות עיקריים. כמובן שאנו מדברים על מימושים אלגוריתמיים/ מימוש שהוא חינמי.
### How to Implement Dropbox
כאשר ניצבת לפנינו בעיה מורכבת. שפיתרונה תומן בתוכו את פירוק הבעיה לכמה בעיות קטנות יותר. חיפוש באינרנט וניתוח פתרונות של אנשים אחרים יכול לעזור לנו מאוד בלהבין את מורכות הבעיה וכיצד לפתור אותה.
כתבה מצוינת שנותנת כמה רבדים שונים לבעיה וגישות לפיתרון הינה הכתבה [הזאת](https://systemdesignprimer.com/dropbox-system-design/).
אני ממליץ בחום לקרוא לפני המשך קריאת המסמך הזה. שכן היא תתרום להבנה ותכניס אתכם לעולם הבעיה והלך הרוח
### Rsync
מחיפוש מהיר באינטרנט, הדבר הראשון אשר הבחנתי בוא הוא הכלי rsync. לפי עמוד ה-manual שלו:
> Rsync is a fast and extraordinarily versatile file copying tool. It can copy locally, to/from another host over any remote shell, or to/from a remote rsync daemon. It offers a large number of options that control every aspect of its behavior and permit very flexible specification of the set of files to be copied.
[Linux Man Page](https://linux.die.net/man/1/rsync)

על פניו. נראה שזהו פיתרון מתקבל על הדעת. תומך בסינון של סנכרון ספציפי של קבצים. תומך ב-peer to peer.
אך לאחר בחינה מעמיקה של הפיתרון. הגעתי למסקנות הבאות
1. הסנכרון אינו קורה באופן תמידי, רק כאשר משתמשים בפקודה - אינו עולה בקנה אחד עם הדרישות שהגדרנו במבוא
2. הסכנרון הוא רק בין שתי עמדות קצה, ולא מספר רב של מחשבים
על אף שהפיתרון הכולל אינו מתאים. הרעיון מאחורי האלגוריתם להעברת הקבצים נמצא מתאים למידותי הפרויקט. על כך יורחב ב[פרוטוקול](##פרוטוקול)


## איך הפרויקט בנוי
### מבנה הפרויקט
פיתוח צד השרת וצד הלקוח נעשו באותו ה-`repository`. היו לכך כמה סיבות מרכזיות.
1. פרוטוקול הפרויקט תחת התיקייה protos. ככה שגם ללקוח וגם לשרת מאוד קל להתממשק מולם. ואין צורך לוודא שכל repo בעצמו מחזיק בגרסה הכי חדשה ומעודכנת
2. כחלק מהתליך הפיתוח. אני משתמש בpytest על מנת לבצע unit testing וintegration testing בין כל רכיבי המערכת. repo אחד מאוד מקל בבדיקת המרכיבים
### CI/CD
> [!note]
> אם אינכם בקיעים בCI/CD יש קודם לכל לקרוא את על כך [פה](https://resources.github.com/ci-cd/)

בשביל לחסוך זמן. כל פעם שנדחף קוד חדש ל-main. בdocker image הכי עדכני נבנה באופן אוטומטי. בנוסף, כל הבדיקות של הפרויקט רצות
## הוראות שימוש
### הקמת השרת
### צד לקוח
## ארכיטקטורת הפיתרון
### פרוטוקול
### צד שרת
### צד לקוח
## פערים במצב הקיים
