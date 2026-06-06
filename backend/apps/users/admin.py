from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from apps.users.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['id', 'username', 'email', 'nickname', 'role', 'status', 'created_at']
    list_filter = ['role', 'status']
    search_fields = ['username', 'email', 'nickname']
    ordering = ['-created_at']
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('个人信息', {'fields': ('email', 'nickname', 'avatar', 'bio')}),
        ('权限', {'fields': ('role', 'status', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('社交链接', {'fields': ('github_url', 'website_url')}),
        ('时间信息', {'fields': ('last_login_at', 'created_at', 'updated_at')}),
    )
    readonly_fields = ['created_at', 'updated_at', 'last_login_at']
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'role', 'status'),
        }),
    )
