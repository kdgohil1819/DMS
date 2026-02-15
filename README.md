# DMS
Document Management System
this is first project for python
and django
we implemented an login/register page
with server
I've added default values to the new fields (file_size, file_type, tags) so migrations will be smooth for everyone.

Please run these commands after pulling:
git pull origin main
python manage.py migrate

If you had existing documents, run this to update their file sizes:
python manage.py shell
from documents.models import Document
for doc in Document.objects.all():
    if doc.file and doc.file_size == 0:
        doc.file_size = doc.file.size
        doc.save()
        print(f"Fixed: {doc.title}")
exit()