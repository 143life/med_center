from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models.user import User


class CustomUserAdmin(UserAdmin):
    list_display = ("username", "email", "role", "is_staff")
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Персональная информация", {"fields": ("email",)}),
        ("Права доступа", {"fields": ("role", "is_staff", "is_active")}),
    )


admin.site.register(User, CustomUserAdmin)
