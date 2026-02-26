# review/urls.py
from django.urls import path
from . import views

app_name = 'review'

urlpatterns = [
    # Reviewer dashboard
    path('', views.review_dashboard, name='dashboard'),
    
    # Review actions
    path('document/<int:doc_id>/review/', views.review_document, name='review_document'),
    path('document/<int:doc_id>/assign/', views.assign_reviewer, name='assign_reviewer'),
    path('document/<int:doc_id>/history/', views.review_history, name='history'),
    
    # User actions
    path('document/<int:doc_id>/resubmit/', views.resubmit_document, name='resubmit'),
]