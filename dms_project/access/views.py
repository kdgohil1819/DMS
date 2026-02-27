# access/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Count, Q
from .models import UserProfile
from documents.models import Document

# Helper functions for role checking
def is_admin(user):
    return user.is_authenticated and (user.is_superuser or (hasattr(user, 'profile') and user.profile.role == 'admin'))

def is_manager(user):
    return user.is_authenticated and (user.is_staff or (hasattr(user, 'profile') and user.profile.role in ['admin', 'manager']))

def is_reviewer(user):
    return user.is_authenticated and (user.is_staff or (hasattr(user, 'profile') and user.profile.role in ['admin', 'manager', 'reviewer']))

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    """Admin dashboard with system overview"""
    
    # Statistics
    total_users = User.objects.count()
    total_documents = Document.objects.count()
    pending_reviews = Document.objects.filter(status='pending').count()
    
    # Recent users
    recent_users = User.objects.select_related('profile').order_by('-date_joined')[:5]
    
    # Document statistics by status
    doc_stats = {
        'pending': Document.objects.filter(status='pending').count(),
        'under_review': Document.objects.filter(status='under_review').count(),
        'approved': Document.objects.filter(status='approved').count(),
        'rejected': Document.objects.filter(status='rejected').count(),
    }
    
    context = {
        'total_users': total_users,
        'total_documents': total_documents,
        'pending_reviews': pending_reviews,
        'recent_users': recent_users,
        'doc_stats': doc_stats,
    }
    return render(request, 'access/admin_dashboard.html', context)

@login_required
@user_passes_test(is_admin)
def user_list(request):
    """List all users with their roles"""
    users = User.objects.select_related('profile').all().order_by('-date_joined')
    
    # Filter by role if specified
    role_filter = request.GET.get('role', '')
    if role_filter:
        users = users.filter(profile__role=role_filter)
    
    context = {
        'users': users,
        'role_filter': role_filter,
        'roles': UserProfile.ROLE_CHOICES,
    }
    return render(request, 'access/user_list.html', context)

@login_required
@user_passes_test(is_admin)
def edit_user(request, user_id):
    """Edit user details and role"""
    user = get_object_or_404(User, id=user_id)
    profile, created = UserProfile.objects.get_or_create(user=user)
    
    if request.method == 'POST':
        # Update user basic info
        user.email = request.POST.get('email', user.email)
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.is_active = request.POST.get('is_active') == 'on'
        user.save()
        
        # Update profile
        profile.role = request.POST.get('role', profile.role)
        profile.department = request.POST.get('department', '')
        profile.phone = request.POST.get('phone', '')
        profile.bio = request.POST.get('bio', '')
        profile.save()
        
        messages.success(request, f'User {user.username} updated successfully!')
        return redirect('access:user_list')
    
    context = {
        'edit_user': user,
        'profile': profile,
        'roles': UserProfile.ROLE_CHOICES,
    }
    return render(request, 'access/edit_user.html', context)

@login_required
@user_passes_test(is_manager)
def create_user(request):
    """Create a new user (manager/admin only)"""
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role', 'user')
        
        # Create user
        user = User.objects.create_user(username=username, email=email, password=password)
        
        # Set role via profile
        profile = user.profile
        profile.role = role
        profile.save()
        
        messages.success(request, f'User {username} created successfully!')
        return redirect('access:user_list')
    
    context = {
        'roles': UserProfile.ROLE_CHOICES,
    }
    return render(request, 'access/create_user.html', context)

@login_required
@user_passes_test(is_admin)
def user_permissions(request, user_id):
    """Manage specific permissions for a user"""
    user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        # Update staff status
        user.is_staff = request.POST.get('is_staff') == 'on'
        user.is_superuser = request.POST.get('is_superuser') == 'on'
        user.save()
        
        messages.success(request, f'Permissions updated for {user.username}')
        return redirect('access:user_list')
    
    context = {
        'perm_user': user,
    }
    return render(request, 'access/user_permissions.html', context)

@login_required
@user_passes_test(is_admin)
def role_list(request):
    """View and manage roles"""
    # Count users per role
    role_stats = []
    for role_code, role_name in UserProfile.ROLE_CHOICES:
        count = UserProfile.objects.filter(role=role_code).count()
        role_stats.append({
            'code': role_code,
            'name': role_name,
            'count': count,
        })
    
    context = {
        'role_stats': role_stats,
    }
    return render(request, 'access/role_list.html', context)
@login_required
def my_profile(request):
    """View and edit own profile"""
    user = request.user
    
    # Get or create profile
    try:
        profile = user.profile
    except:
        # Create profile if it doesn't exist
        profile = UserProfile.objects.create(user=user)
    
    if request.method == 'POST':
        # Update profile
        profile.department = request.POST.get('department', '')
        profile.phone = request.POST.get('phone', '')
        profile.bio = request.POST.get('bio', '')
        profile.save()
        
        messages.success(request, 'Profile updated successfully!')
        return redirect('access:my_profile')
    
    context = {
        'profile': profile,
    }
    return render(request, 'access/my_profile.html', context)