from django.contrib import admin
from .models import Hairstyle

@admin.register(Hairstyle)
class HairstyleAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'target_face_shapes', 'has_image', 'created_at')
    search_fields = ('name', 'target_face_shapes')
    list_filter = ('category', 'target_face_shapes')
    
    def has_image(self, obj):
        return bool(obj.image or obj.image_url)
    has_image.boolean = True
    has_image.short_description = "Rasm bormi?"
