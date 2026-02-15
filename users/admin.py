from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):

    model = CustomUser

    fieldsets = UserAdmin.fieldsets + (
        ("Additional Info", {"fields": ("user_code", "role")}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Additional Info", {"fields": ("user_code", "role")}),
    )

    list_display = ("username", "user_code", "role", "is_active")

admin.site.register(CustomUser, CustomUserAdmin)
