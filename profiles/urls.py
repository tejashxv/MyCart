from django.contrib import admin
from django.urls import path
from .  import views,models


urlpatterns = [
    path("", views.profile, name="profiles"),
]
