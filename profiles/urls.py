from django.contrib import admin
from django.urls import path
from .  import views,models


urlpatterns = [
    path("", views.profile, name="profiles"),
    path("login/", views.loginPage, name="loginPage"),
    path("logout/", views.logoutPage, name="logoutPage"),
    path("account/", views.account, name="account"),
    
    
]
