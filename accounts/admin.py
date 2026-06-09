from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'role', 'telephone', 'region']
    list_filter = ['role', 'region']
    fieldsets = UserAdmin.fieldsets + (
        ('Informations COFINANCE CI', {'fields': ('role', 'telephone', 'region', 'adresse', 'date_naissance', 'piece_identite', 'photo')}),
    )