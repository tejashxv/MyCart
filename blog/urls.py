from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("",views.index,name="BlogIndex"),
    path("blogpost",views.blogpost,name="BlogPost"),
]
