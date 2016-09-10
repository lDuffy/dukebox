#!/bin/bash

pip install -r requirements.txt
#psql -U postgres -h localhost -c "CREATE USER dukebox WITH PASSWORD 'password';"
#psql -U postgres -h localhost -c "ALTER USER dukebox CREATEDB;"
#psql -U postgres -h localhost -c "ALTER ROLE dukebox SUPERUSER;"
dropdb -U postgres -h localhost dukeboxdb
createdb -U postgres -h localhost -O dukebox dukeboxdb
#psql -U postgres -h localhost -d dukeboxdb -c "CREATE EXTENSION postgis;"
#psql -U postgres -h localhost -d dukeboxdb -c "CREATE EXTENSION postgis_topology;"
python manage.py makemigrations main
python manage.py migrate --noinput
python manage.py collectstatic --noinput
python manage.py runscript --traceback load_data
