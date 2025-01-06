from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
# Create your views here.

def profile(request):
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        Last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        user = User.objects.filter(Q(username=username) | Q(email=email))
        
        if user.exists():
            messages.error(request, 'Username or email already exists')
            return render(request, 'shop/profiles.html')
      
        user = User.objects.create(username=username, email=email,first_name=first_name, last_name=Last_name)
        user.set_password(password)
        user.save()
        messages.success(request,'registration successfully')
        
        
        
        
        
    return render(request, 'shop/profiles.html',{'user':User.objects.all()})


def identify_user_type(email_or_username):
    user = User.objects.filter(Q(username=email_or_username) | Q(email=email_or_username)).first()
    if user:
        if user.email == email_or_username:
            return "email"
        elif user.username == email_or_username:
            return "username"
    return "not_found"


def loginPage(request):
    if request.method == "POST":
        password = request.POST.get('password')
        email = request.POST.get("email")
        print(password,email)
        user = User.objects.filter(Q(username = email) | Q(email = email))
        verify = identify_user_type(email)
        if not user.exists():
            messages.error(request, "User not found")
            return redirect('/profile')
        if verify == "email":
            user = authenticate(email=email,password=password)
        elif verify == "username":
            user = authenticate(username=email,password=password)
        login(request, user)
        
        return redirect("/shop")
            
    return render(request, "shop/login.html")



def logoutPage(request):
    logout(request)
    return redirect("/shop")
        
            
    
