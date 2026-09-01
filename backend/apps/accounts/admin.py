from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from apps.accounts.models import User

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['email', 'first_name', 'last_name', 'role', 'is_staff', 'is_active']
    list_filter = ['role', 'is_staff', 'is_active']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role', 'profile_image', 'phone')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('role', 'profile_image', 'phone', 'email')}),
    )
    ordering = ['email']

admin.site.register(User, CustomUserAdmin)
