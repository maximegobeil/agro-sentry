from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser
import os
from django.conf import settings

if getattr(settings, 'ADMIN_ENABLED', False):
    @admin.register(CustomUser)
    class CustomUserAdmin(UserAdmin):
        add_form = CustomUserCreationForm
        form = CustomUserChangeForm
        model = CustomUser
        list_display = ('email', 'first_name', 'last_name',
                        'is_staff', 'is_active',)
        list_filter = ('is_staff', 'is_active',)
        fieldsets = (
            (None, {'fields': ('email', 'password')}),
            ('Personal info', {'fields': ('first_name',
            'last_name')}),
            ('Permissions', {'fields': ('is_staff',
            'is_active', 'groups', 'user_permissions')}),
        )
        add_fieldsets = (
            (None, {
                'classes': ('wide',),
                'fields': ('email', 'first_name', 'last_name', 'password1', 'password2', 'is_staff', 'is_active')}
            ),
        )
        search_fields = ('email', 'first_name', 'last_name')
        ordering = ('email',)
