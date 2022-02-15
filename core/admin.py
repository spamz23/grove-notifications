"""
Register models into Django Admin Dashboard
"""
from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass
