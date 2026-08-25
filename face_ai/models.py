from django.db import models

class Hairstyle(models.Model):
    CATEGORY_CHOICES = (
        ('classic', 'Klassik'),
        ('modern', 'Zamonaviy'),
        ('fade', 'Fade uslubi'),
        ('kids', 'Bolalar uchun'),
        ('other', 'Boshqa'),
    )

    name = models.CharField(max_length=150, verbose_name="Soch turmagi nomi")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='modern', verbose_name="Kategoriya")
    
    # ImageField orqali Django Admin paneldan rasm yuklash imkoniyati
    image = models.ImageField(upload_to='hairstyles/', verbose_name="Rasm (Admin paneldan yuklang)", blank=True, null=True)
    
    # Eski URL tizimi uchun (API'dan tushgan yoki fayl emas link bo'lganlar uchun)
    image_url = models.CharField(max_length=500, verbose_name="Rasm URL manzili (ixtiyoriy)", blank=True, null=True)
    
    target_face_shapes = models.CharField(max_length=250, verbose_name="Mos keluvchi yuz shakllari", help_text="Masalan: Oval, Dumaloq, Olmos")
    description = models.TextField(verbose_name="Tavsifi (Nima uchun mos va izoh)")
    created_at = models.DateTimeField(auto_now_add=True)

    def get_image_url(self):
        """Agar ImageField da rasm bo'lsa uni, yo'qsa urlni qaytaradi"""
        if self.image:
            return self.image.url
        return self.image_url

    def __str__(self):
        return self.name
