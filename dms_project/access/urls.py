# access/urls.py
from django.urls import path
from . import views

app_name = 'access'

urlpatterns = [
    # Admin dashboard
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    
    # User management
    path('users/', views.user_list, name='user_list'),
    path('users/create/', views.create_user, name='create_user'),
    path('users/<int:user_id>/edit/', views.edit_user, name='edit_user'),
    path('users/<int:user_id>/permissions/', views.user_permissions, name='user_permissions'),
    
    # Role management
    path('roles/', views.role_list, name='role_list'),
    
    # Profile
    path('profile/', views.my_profile, name='my_profile'),
]