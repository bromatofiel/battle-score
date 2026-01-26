from core.admins import BaseAdmin
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Client, Profile


@admin.register(User)
class CustomUserAdmin(UserAdmin, BaseAdmin):
    list_display = ("email", "username", "is_staff", "is_active", "date_created")
    list_filter = ("is_staff", "is_active")
    search_fields = ("email", "username")
    ordering = ("email",)
    readonly_fields = BaseAdmin.readonly_fields + ("public_id", "uid")


@admin.register(Profile)
class ProfileAdmin(BaseAdmin):
    list_display = ("user", "pseudo", "date_created")
    search_fields = ("user__email", "user__username", "pseudo")


@admin.register(Client)
class ClientAdmin(BaseAdmin):
    list_display = ("name", "user", "vat_number", "date_created")
    search_fields = ("name", "user__email", "user__username", "vat_number")
    list_filter = ("user",)
