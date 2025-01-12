from django.contrib import admin
from .models import *

admin.site.register(Products)
admin.site.register(Contact)
admin.site.register(Orders)
admin.site.register(OrderUpdate)

# Register your models here.
admin.site.site_header = "Tejash Administration"  # The header displayed at the top of the admin panel
admin.site.site_title = "Tejash Admin Portal"     # The title in the browser tab
admin.site.index_title = "Welcome to Tejash Admin Panel"  # The subtitle on the index page