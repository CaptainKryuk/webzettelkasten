from django.contrib import admin
from .models import User
from django.contrib.auth import admin as auth_admin
# Register your models here.

@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    list_display = ("username", "is_superuser",)
    search_fields = ("username",)
    fieldsets = (("User", {"fields": ("username", "email", "first_name", "last_name", "password")}),)
