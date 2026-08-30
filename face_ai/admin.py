from django.contrib import admin
from django.utils.html import format_html
from .models import Hairstyle

@admin.register(Hairstyle)
class HairstyleAdmin(admin.ModelAdmin):
    list_display = ('image_preview', 'name', 'category', 'target_face_shapes', 'created_at')
    list_display_links = ('image_preview', 'name')
    search_fields = ('name', 'target_face_shapes', 'description')
    list_filter = ('category', 'target_face_shapes')
    readonly_fields = ('image_preview_large',)
    
    fieldsets = (
        ('Asosiy Ma\'lumotlar', {
            'fields': ('name', 'category', 'target_face_shapes', 'description')
        }),
        ('Rasm yuklash', {
            'fields': ('image', 'image_url', 'image_preview_large')
        })
    )

    def image_preview(self, obj):
        url = obj.get_image_url()
        if url:
            return format_html('<img src="{}" style="width: 50px; height: 50px; border-radius: 8px; object-fit: cover; box-shadow: 0 2px 4px rgba(0,0,0,0.1);"/>', url)
        return format_html('<div style="width: 50px; height: 50px; border-radius: 8px; background: #e2e8f0; display: flex; align-items: center; justify-content: center; color: #94a3b8; font-size: 20px;"><i class="fas fa-cut"></i></div>')
    image_preview.short_description = "Rasm"

    def image_preview_large(self, obj):
        url = obj.get_image_url()
        if url:
            return format_html('<img src="{}" style="max-width: 300px; max-height: 300px; border-radius: 12px; box-shadow: 0 4px 10px rgba(0,0,0,0.1);"/>', url)
        return "Rasm yo'q"
    image_preview_large.short_description = "Joriy Rasm"
