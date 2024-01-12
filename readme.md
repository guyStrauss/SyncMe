# SyncMe

`Open University of Israel, Workshop in Computer Communications, 2023`

`By Guy Strauss (207253899)`


## תוכן עניינים
 - [הקדמה](##הקדמה)

## סרטון קצר

https://github.com/guyStrauss/SyncMe/assets/11578138/023f96ba-ca6e-4eb1-b938-a8f0f970b8f0



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
יש שתי דרכים להקמת השרת:
1. הראשונה היא הרצה מקומית על המחשב (קרי, הרצה `mongo-db` על המחשב והרצת השרת באמצעות `python`)
2. השניה (**והמועדפת**) היא שימוש ב-`docker-compose`
#### הרצה מקומית
1. התקינו בדרך המועדפת עליכם את ה-`service` של `mongo-db` (אל דאגה, נסקור את מטרתו ב-ארכיטקטורת הפיתרון) וודאו שהוא מאזין על הפורט 27017
2. הריצו `python -m venv venv` וודאו שאתם עובדים ב-context של ה-`virtual intetrprator`
3. הריצו `pip install -r requirements.txt`
4. הריצו את `file_sync_servicer`
#### הרצה באמצעות docker-compose
1. הריצו `docker-compose up -d`
### צד לקוח
1.  `<python client/main <DIRECTORY_TO_WATCH`
## ארכיטקטורת הפיתרון
### צד שרת
#### כללי
צד הרשת הוא stateless. משמע אין משמעות לסדר הפניות. משום שהשרת מושך את הנתונים שהוא מחזיר מבסיסי הנתונים שיתוארו בהמשך.
> [!important]
> בעת הסקירה, נתייחס למבני הנתונים בעוד רכיב שמופרד מלוגיקת השרת
#### סקירה כללית
![sync-me_overview drawio (1)](https://github.com/guyStrauss/SyncMe/assets/11578138/ab6b0d68-5346-42db-9382-13e365ba3f8b)

כי שניתן לראות בדיאגרמה, צד השרת מסתמך על שני שרתים. אחד מבוסס קבצים בשביל לשמור את הקבצים עצמם. והשני בשביל לשמור את המידע הנוסף. נסביר בהרחבה כל אחד מהרכיבים
#### File Database
![storage_database py](https://github.com/guyStrauss/SyncMe/assets/11578138/dadc238b-896f-4249-a1c3-559ae1f41939)



מטרת מבני נתונים זה הוא לשמור את הקבצים. עבור כל לקוח במערכת. נוצר קובץ zip שבתוכו כל הקבצים של הלקוח, שמם של הקבצים הוא ערך ה-sha256 שלהם. מבני הנתונים תומך בקריאה ובכתיבה גם לחלקים של קובץ ולא לכולו.
#### Metadata Database
![metadata_database](https://github.com/guyStrauss/SyncMe/assets/11578138/06ef4716-5297-4d4d-9222-0239e25cd4e1)




מטרת הרכיב הזה היא לשמור את כל המידע שלא קשור לתוכן הקובץ. כיום המימוש הוא מעל mongo-db משום שהוא עובד בצורה נוחה מאוד עם jsons (מה שpydantic מוציא). אך אין זאת בעיה בכלל להחליף את מבנה הנתונים הקיים באחר כל עוד שומרים על מימוש כל הפונקציות הנ״ל
##### Medatada Database Entry
כל רשומה מחזיקה בתוכה את מבנה הנתונים הבא
![inserted_file_metadata](https://github.com/guyStrauss/SyncMe/assets/11578138/7d68e700-1e5c-45e3-86e8-f324d2f700c4)
![file_part_hash](https://github.com/guyStrauss/SyncMe/assets/11578138/b5e91aa3-672e-4293-b88e-fabe5a31e63a)



> [!important]
> השדה הכי חשוב פה `version`. ככה אנו יודעים להשוות עם הלקוח למי יש את הקובץ העדכני ביותר ולהסתנכרן לפי השינויים הרלוונטים
השדה `id` מציין את מספר הזהות של הרשומה, ולא של המשתמש. והרשימה `hash_list` מכילה את ערך פונקציית הריבוב עבור בלוקים של הקובץ ( 250kb)
#### File Sync Servicer
![file_sync_servicer](https://github.com/guyStrauss/SyncMe/assets/11578138/a88e58d4-8dd3-4cef-bbbe-e2da549570a1)
עכשיו, לאחר הסקירה של שני הרכיבים. השלישי קל להסברה. הוא פשוט מחבר בין שניהם.

### צד לקוח
צד הלקוח הוא קצת יותר מורכב. משום שהוא צריך לשמור טבלה משלו עבור עץ התיקיות. נציד סרטוט סמכטי של אופן פעולתו. ואז נדון בהרחבה על כל רכיב
![image](https://github.com/guyStrauss/SyncMe/assets/11578138/6304f084-4893-4397-a8ed-4a3d11c1290b)

ה-Watcher קורא לDispatcher
#### Internal DB
מאחורי הקלעים, יש שימוש בספרייה `tinyDb` ספריית פייתון נהדרת לדברים כאלה. נציד את כל הפונקציות שמבנה הנתונים תומך בו
![internal_db](https://github.com/guyStrauss/SyncMe/assets/11578138/1016163c-3c57-4539-a8d2-81128e5959db)
##### Schema
```python
{'id': file_id, 'name': file_name, 'hash': file_hash, 'timestamp': file_timestamp,
             "version": version}
```
#### Watcher
לולאה שרצה כל 10 שניות, ואחראית על ״דיווח״ שינוים ל-dispatcher.
##### Algorithem
![image](https://github.com/guyStrauss/SyncMe/assets/11578138/8cc0415a-7c3b-4dad-b088-0511a5c616c4)


#### Dispatcher
אחראי על קבלת הוראה חדשה מהwatcher. ולעשות אותה.
![dispatcher](https://github.com/guyStrauss/SyncMe/assets/11578138/2127690b-a2a3-4464-ad55-b991fa761d1a)

### פרוטוקול
מימוש הפרוטוקל נעשה באמצעות `grpc`. למי שלא בקיא. הנה כמה משפטים מעמוד הפרויקט הראשי
> In gRPC, a client application can directly call a method on a server application on a different machine as if it were a local object, making it easier for you to create distributed applications and services

[GRPC Intro](https://grpc.io/docs/what-is-grpc/introduction/)

כלומר, עלינו רק להגדיר מהם הפונקציות. ובאמצעות grpc ו[protobuf](https://grpc.io/docs/what-is-grpc/introduction/)
#### הגדרת הפרוטוקול
להתרשמות מהגדרת הפרוטוקול. ניתן להסתכל בקובץ [הזה](/protos/file_sync.proto) אך בגדול, מוגדרות שם כל שמות הפוקנציות ב file sync servicer


### סמכת זרימה בין הרשת ללקוח
הסרטוט הבא מתאר סמכת זרימה סטנדרטית.
![image](https://github.com/guyStrauss/SyncMe/assets/11578138/56f0fd4a-7558-4b89-b385-f0a6014f507d)

### בדיקות
#### צד שרת
##### ServicerTests

| Name                          | Purpose                                                        |
|-------------------------------|----------------------------------------------------------------|
| `test_upload_file`            | Tests the uploading of a file to the server.                   |
| `test_get_file`               | Validates retrieval of a specific file from the server.        |
| `test_does_file_exist`        | Checks if a file exists on the server.                         |
| `test_file_doesnt_exist`      | Verifies that a non-existent file is correctly identified.     |
| `test_check_version`          | Tests version checking of a file on the server.                |
| `test_check_version_doesnt_exist` | Checks behavior when a version doesn't exist.              |
| `test_delete_file`            | Tests the deletion of a file from the server.                  |
| `test_delete_file_doesnt_exist` | Ensures correct handling of deleting a non-existent file.   |
| `test_get_files`              | Tests retrieval of a list of files from the server.            |
| `test_sync_file`              | Tests the synchronization of a file with the server.           |
| `test_sync_file_eof`          | Tests file synchronization with EOF changes.                   |
| `test_sync_file_start`        | Placeholder (no implementation).                               |
| `test_update_name`            | Tests updating the name of a file on the server.               |
| `test_sync_file_server`       | Tests file synchronization from the server.                    |

##### TestStorage

| Name                     | Purpose                                                       |
|--------------------------|---------------------------------------------------------------|
| `test_upload`            | Tests uploading a file to storage.                            |
| `test_get_file`          | Verifies retrieval of a file from storage.                    |
| `test_get_file_offset`   | Tests getting a file from storage with a specific offset.     |
| `test_get_file_hashes`   | Validates retrieval of file hashes from storage.              |
| `test_delete_file`       | Tests deletion of a file from storage.                        |
| `test_sync_file`         | Tests synchronization of a file with changes in storage.      |

##### MongoTests

| Name                    | Purpose                                                         |
|-------------------------|-----------------------------------------------------------------|
| `test_insert`           | Tests inserting file metadata into the database.                |
| `test_update`           | Tests updating file metadata in the database.                   |
| `test_get_all_metadata` | Tests retrieval of all metadata records for a user.             |
| `test_update_hashes`    | Tests updating file part hashes in the metadata.                |
| `test_get_metadata`     | Validates retrieval of specific file metadata from the database.|
| `test_delete`           | Tests deletion of metadata from the database.                   |



#### צד לקוח
בדיקות נעשו בצורה ידנית.
## פערים במצב הקיים
