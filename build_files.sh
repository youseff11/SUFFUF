echo "BUILD START"

# تثبيت المكتبات وتحديث pip
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt

# تشغيل collectstatic
python3 manage.py collectstatic --noinput --clear

echo "BUILD END"