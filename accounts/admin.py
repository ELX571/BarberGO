from django.contrib import admin
from django.utils.html import format_html
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Account

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'first_name', 'last_name', 'role_badge', 'phone_number', 'avatar_preview', 'is_active')
    list_display_links = ('id', 'username')
    search_fields = ('username', 'first_name', 'last_name', 'phone_number', 'email')
    list_filter = ('role', 'is_active', 'is_staff')
    readonly_fields = ('avatar_preview',)
    
    fieldsets = (
        ('Shaxsiy ma\'lumotlar', {
            'fields': ('avatar', 'avatar_preview', 'username', 'password', 'first_name', 'last_name')
        }),
        ('Aloqa va Manzil', {
            'fields': ('phone_number', 'email', 'city')
        }),
        ('Status va Rol', {
            'fields': ('role', 'is_active', 'is_staff', 'is_superuser')
        }),
        ('Ruxsatlar', {
            'fields': ('groups', 'user_permissions'),
            'classes': ('collapse',)
        }),
    )

    def avatar_preview(self, obj):
        if obj.avatar:
            return format_html('<img src="{}" style="width: 50px; height: 50px; border-radius: 50%; object-fit: cover; box-shadow: 0 2px 4px rgba(0,0,0,0.1);"/>', obj.avatar.url)
        return format_html('<div style="width: 50px; height: 50px; border-radius: 50%; background: #e2e8f0; display: flex; align-items: center; justify-content: center; color: #94a3b8; font-weight: bold;">{}</div>', obj.username[0].upper() if obj.username else "?")
    avatar_preview.short_description = "Avatar"

    def role_badge(self, obj):
        color = "#3b82f6" if obj.role == 'customer' else "#f97316"
        text = "Mijoz" if obj.role == 'customer' else "Sartarosh" if obj.role == 'barber' else obj.role
        return format_html('<span style="background: {}; color: white; padding: 3px 10px; border-radius: 12px; font-size: 12px; font-weight: 600;">{}</span>', color, text)
    role_badge.short_description = "Rol"

