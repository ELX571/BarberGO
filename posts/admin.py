from django.contrib import admin
from django.utils.html import format_html
from .models import Post, Comment

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'user', 'like_count_display', 'image_preview', 'created_at')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'description', 'user__username', 'user__first_name')
    list_filter = ('created_at', 'updated_at')
    readonly_fields = ('image_preview', 'video_preview', 'created_at', 'updated_at')
    filter_horizontal = ('likes',)
    
    fieldsets = (
        ('Asosiy Ma\'lumotlar', {
            'fields': ('user', 'title', 'description')
        }),
        ('Media Fayllar (Rasm & Video)', {
            'fields': ('image', 'image_preview', 'video', 'video_preview')
        }),
        ('Interaktiv', {
            'fields': ('likes',),
            'classes': ('collapse',)
        }),
        ('Tizim ma\'lumotlari', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 80px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);"/>', obj.image.url)
        return "Rasm yo'q"
    image_preview.short_description = "Rasm (Preview)"

    def video_preview(self, obj):
        if obj.video:
            return format_html('<video src="{}" style="max-height: 150px; border-radius: 8px;" controls></video>', obj.video.url)
        return "Video yo'q"
    video_preview.short_description = "Video (Preview)"
    
    def like_count_display(self, obj):
        return format_html('<span style="color: #ea580c; font-weight: bold;">❤️ {}</span>', obj.likes.count())
    like_count_display.short_description = "Likes"


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'parent_post', 'short_text', 'created_at')
    search_fields = ('text', 'user__username', 'parent_post__title')
    list_filter = ('created_at',)
    
    def short_text(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text
    short_text.short_description = "Komment matni"

