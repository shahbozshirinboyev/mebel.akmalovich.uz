from django.contrib import admin
from django.contrib.auth.models import Group
from .models import User
from core.admin_mixins import PreserveFiltersAdminMixin
from django.utils.html import format_html
from datetime import datetime

admin.site.unregister(Group)

@admin.register(User)
class UserAdmin(PreserveFiltersAdminMixin, admin.ModelAdmin):

    list_display = (
        'id',
        'username',
        'first_name',
        'last_name',
        'phone_number',
        'is_superuser',
        'is_active',
        'is_staff',
        'is_worker',
        'is_manager',
        'date_joined',
        'last_login',
    )
    search_fields = ('username', 'first_name', 'last_name', 'phone_number')
    list_filter = ()

    # Hide these fields from the add/edit forms
    exclude = ('last_login', 'groups', 'email', 'date_joined')

    # Display fields without sections
    fields = (
        'username',
        'password',
        'first_name', 
        'last_name',
        'phone_number',
        'is_active',
        'is_staff',
        'is_superuser',
        'is_worker',
        'is_manager',
        'user_permissions',
    )

    class Media:
        css = {
            'all': ('/static/admin/css/custom_admin.css',)
        }