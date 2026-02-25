# search/urls.py
from django.urls import path
from . import views

app_name = 'search'

urlpatterns = [
    path('', views.search_documents, name='search'),
    path('recent/', views.recent_documents, name='recent'),
]