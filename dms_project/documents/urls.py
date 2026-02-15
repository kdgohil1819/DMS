# documents/urls.py
from django.urls import path
from . import views

app_name = 'documents'

urlpatterns = [
    path('upload/', views.upload_document, name='upload'),
    path('my-documents/', views.my_documents, name='my_documents'),
    path('<int:doc_id>/', views.document_detail, name='detail'),
    path('<int:doc_id>/download/', views.download_document, name='download'),
    path('<int:doc_id>/delete/', views.delete_document, name='delete'),
]