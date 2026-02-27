# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from documents.models import Document
# R-1.1 User Registration (Only Normal Users)
def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        
        # Check if passwords match
        if password != password2:
            messages.error(request, 'Passwords do not match')
            return render(request, 'accounts/register.html')
        
        # Check if username exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken')
            return render(request, 'accounts/register.html')
        
        # Check if email exists
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered')
            return render(request, 'accounts/register.html')
        
        # Create normal user (NOT admin)
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        
        messages.success(request, 'Registration successful! Please login.')
        return redirect('accounts:login')
    
    return render(request, 'accounts/register.html')

# R-1.2 User Login (Role-Based)
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        role = request.POST.get('role')  # admin or user
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Admin role selected but user is not admin
            if role == "admin" and not user.is_superuser:
                messages.error(request, "You are not authorized as Admin.")
                return redirect('accounts:login')
            
            # User role selected but user is admin
            if role == "user" and user.is_superuser:
                messages.error(request, "Please login as Admin.")
                return redirect('accounts:login')
            
            # Login successful
            login(request, user)
            messages.success(request, f'Welcome back, {username}!')
            
            # Redirect based on user type
            if user.is_superuser:
                return redirect('accounts:admin_dashboard')
            else:
                return redirect('accounts:dashboard')
        else:
            messages.error(request, 'Invalid username or password')
    
    return render(request, 'accounts/login.html')

# R-1.3 Logout
def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out successfully')
    return redirect('accounts:login')

# User Dashboard
@login_required
def dashboard_view(request):
    # Get document counts for the current user
    user_documents = Document.objects.filter(uploader=request.user)
    
    context = {
        'approved_count': user_documents.filter(status='approved').count(),
        'pending_count': user_documents.filter(status='pending').count(),
        'rejected_count': user_documents.filter(status='rejected').count(),
        'under_review_count': user_documents.filter(status='under_review').count(),
    }
    return render(request, 'accounts/dashboard.html', context)

# Admin Dashboard (Only Superuser)
@staff_member_required
def admin_dashboard_view(request):
    return render(request, 'accounts/admin_dashboard.html')