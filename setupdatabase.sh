#!/bin/bash
rm -f db.sqlite3
rm -r main/migrations
pip install -r requirements.txt
python manage.py syncdb --noinput

chown www-data:www-data .

python manage.py makemigrations
python manage.py migrate --noinput
python manage.py collectstatic --noinput
python manage.py runscript --traceback load_data
