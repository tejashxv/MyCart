from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib import messages
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
