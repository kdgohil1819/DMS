# accounts/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required


# Registration (Only Normal Users)
def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password != password2:
            messages.error(request, 'Passwords do not match')
            return render(request, 'accounts/register.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken')
            return render(request, 'accounts/register.html')

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


# Role-Based Login (Admin & User)
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        role = request.POST.get('role')  # admin or user

        user = authenticate(request, username=username, password=password)

        if user is not None:

            # If Admin selected but user is not superuser
            if role == "admin" and not user.is_superuser:
                messages.error(request, "You are not authorized as Admin.")
                return redirect('accounts:login')

            # If User selected but user is admin
            if role == "user" and user.is_superuser:
                messages.error(request, "Please login as Admin.")
                return redirect('accounts:login')

            login(request, user)

            if user.is_superuser:
                return redirect('accounts:admin_dashboard')
            else:
                return redirect('accounts:dashboard')

        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'accounts/login.html')


# Logout
def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out successfully')
    return redirect('accounts:login')


# User Dashboard
@login_required
def dashboard_view(request):
    return render(request, 'accounts/dashboard.html')


# Admin Dashboard (Only Superuser)
@staff_member_required
def admin_dashboard_view(request):
    return render(request, 'accounts/admin_dashboard.html')