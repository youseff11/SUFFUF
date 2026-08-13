# SUFFUF — Modernization Notes

تم تحديث الواجهة الأمامية لموقع SUFFUF مع الحفاظ على صفحات Django والمسارات والبيانات الديناميكية الموجودة.

## ما تم تحديثه

أُعيد بناء القالب الأساسي والصفحات الرئيسية وصفحات من نحن والخدمات والمشروعات وتفاصيل الخدمة والتواصل ضمن هوية **Editorial Engineering**. تستخدم الواجهة كحليًا عميقًا، نحاسيًا محروقًا، أسطحًا ورقية، تخطيطًا غير متماثل، خطوطًا حديثة، وحركة خفيفة تحافظ على أولوية المحتوى.

أضيف تبديل اللغة بين العربية والإنجليزية من الواجهة نفسها، مع تغيير اتجاه الصفحة وحقول النماذج والـ placeholders. كما أضيف تبديل الوضع الفاتح والداكن مع حفظ الاختيار في `localStorage`.

تمت إضافة صور صناعية مولدة خصيصًا إلى `static/images/` لاستخدامها في البطل، بطاقات المشروعات، والصور الاحتياطية. الصور الموجودة في قاعدة البيانات تظل مستخدمة عندما تكون متاحة.

## التشغيل

من داخل مجلد المشروع:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install django pillow
python manage.py migrate
python manage.py runserver
```

## التحقق

تم تشغيل `python manage.py check` و`python manage.py test` وفحص JavaScript بواسطة `node --check static/js/site.js`. كما تم اختبار HTTP للمسارات `/`, `/about/`, `/services/`, `/projects/`, `/contact/` و`/services/industrial-piping/`، وكلها أعادت الحالة `200`.

## ملاحظة حول الترجمة

النصوص البنيوية والتحكمات أصبحت ثنائية اللغة. أما النصوص القادمة من قاعدة البيانات، مثل أسماء الخدمات ووصفها وأسماء المشروعات، فتظل كما هي لأن النموذج الحالي لا يحتوي حقول ترجمة مستقلة لها.


postgresql://neondb_owner:npg_6xYVKUGNRbo4@ep-weathered-base-aylvwqpb-pooler.c-5.us-east-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require

cQwgde3dXo_PdY9GP8UruArs6LU