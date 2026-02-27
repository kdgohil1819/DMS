# DMS
Document Management System
this is first project for python
and django
we implemented an login/register page
with server
I've added default values to the new fields (file_size, file_type, tags) so migrations will be smooth for everyone.
# update 2
We've integrated to MySQL from SQLite.

# Before pull
Set Up MySQL Database
in phpmyAdmin
create database dms_db
collection  utf8mb4_unicode_ci
after database..
create user
user_name:dms_user
hostname:localhost
password:Dms@2024secure
check "Grant all privileges"
# After pull
Activate virtual enviroment
venv\Scripts\activate

Install all required packages
pip install -r requirements.txt
Run Migrations:
python manage.py migrate

for style run this command:
python manage.py collectstatic

  then create superuser for server access;
  python manage.py createsuperuser

  then run server:
  python manage.py runserver

  backing up data from SQLite:
  python manage.py dumpdata --natural-foreign --natural-primary -e contenttypes -e auth.Permission --indent 4 | Set-Content datadump.json -Encoding UTF8

  