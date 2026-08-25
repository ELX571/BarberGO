from django.contrib import admin
from django.utils.html import format_html
from .models import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'barber', 'status_badge', 'endpoint_time', 'created_at')
    list_display_links = ('id', 'customer')
    search_fields = ('customer__username', 'barber__username', 'description')
    list_filter = ('status', 'endpoint_time', 'created_at')
    readonly_fields = ('image_preview', 'created_at', 'updated_at')
    
    fieldsets = (
        ('Buyurtma ishtirokchilari', {
            'fields': ('customer', 'barber')
        }),
        ('Buyurtma holati va vaqti', {
            'fields': ('status', 'endpoint_time')
        }),
        ('Qo\'shimcha ma\'lumotlar', {
            'fields': ('description', 'image', 'image_preview')
        }),
        ('Tizim', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 100px; border-radius: 8px;"/>', obj.image.url)
        return "Rasm yo'q"
    image_preview.short_description = "Rasm (Preview)"

    def status_badge(self, obj):
        colors = {
            'pending': '#f59e0b',
            'accepted': '#10b981',
            'canceled': '#ef4444'
        }
        color = colors.get(obj.status, '#6b7280')
        return format_html('<span style="background: {}; color: white; padding: 4px 12px; border-radius: 12px; font-weight: bold; font-size: 12px;">{}</span>', color, obj.get_status_display())
    status_badge.short_description = "Status"
