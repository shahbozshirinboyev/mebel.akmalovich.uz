from django.contrib import admin
from django.contrib.auth.models import Group
from .models import User

# Guruhlarni (Groups) admin panelidan olib tashlash
admin.site.unregister(Group)

# User modelini panelga qo'shish
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'first_name', 'last_name', 'phone_number', 'is_worker', 'is_staff', 'is_active', 'is_superuser', 'last_login', 'date_joined')