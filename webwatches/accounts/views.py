from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages

def accounts_home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password:
            user = User.objects.create_user(username=username, password=password)
            user.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect('accounts_home')
        else:
            messages.error(request, "Passwords do not match.")
    return render(request, 'register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login successful.")
            return redirect('watches:homepage')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'login.html')

def custom_logout(request):
    # Log out the user
    logout(request)
    # Redirect to the homepage (you can adjust this to your actual homepage URL)
    return redirect('watches:homepage')