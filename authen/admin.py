from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, ProImage


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "age",
        "gender",
        "is_staff",
        "is_active",
    )
    search_fields = ("username", "email", "first_name", "last_name")
    fieldsets = UserAdmin.fieldsets + (
        ("Additional information", {"fields": ("age", "phone", "gender", "dob")}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Additional information", {"fields": ("age", "phone", "gender", "dob")}),
    )


@admin.register(ProImage)
class ProImageAdmin(admin.ModelAdmin):
    list_display = ("user", "Proimage")
    search_fields = ("user__username", "user__email")
