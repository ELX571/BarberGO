from django.contrib import admin
from django.utils.html import format_html
from .models import Notifications

@admin.register(Notifications)
class NotificationsAdmin(admin.ModelAdmin):
    list_display = ('id', 'receptions', 'short_title', 'is_read_badge', 'created_at')
    list_display_links = ('id', 'receptions')
    search_fields = ('title', 'description', 'receptions__username')
    list_filter = ('is_read', 'created_at')

    def short_title(self, obj):
        return obj.title[:40] + '...' if len(obj.title) > 40 else obj.title
    short_title.short_description = "Sarlavha"

    def is_read_badge(self, obj):
        if obj.is_read:
            return format_html('<span style="color: #10b981; font-weight: bold;">✓ O\'qilgan</span>')
        return format_html('<span style="color: #ef4444; font-weight: bold;">! Yangi</span>')
    is_read_badge.short_description = "Holati"
