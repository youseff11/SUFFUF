echo "BUILD START"

# 1. تثبيت المكتبات في المسار الحالي
python3 -m pip install -r requirements.txt

# 2. إنشاء المجلد يدويًا تحسبًا لأي شيء
mkdir -p staticfiles_build/static

# 3. تشغيل collectstatic
python3 manage.py collectstatic --noinput --clear

echo "BUILD END"