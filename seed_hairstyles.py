import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from face_ai.models import Hairstyle

hairstyles = [
    {
        "name": "Classic Pompadour",
        "image_url": "/static/images/hairstyles/pompadour.jpg",
        "target_face_shapes": "Oval, Dumaloq, To'rtburchak",
        "description": "Yuzni uzunroq ko'rsatuvchi klassik uslub, tepasi hajmli va yonlari kalta."
    },
    {
        "name": "Textured French Crop",
        "image_url": "/static/images/hairstyles/french_crop.jpg",
        "target_face_shapes": "Olmos, Cho'ziq, Oval",
        "description": "Peshonani yopib turuvchi teksturali va zamonaviy uslub, keng peshonani yashirishga yordam beradi."
    },
    {
        "name": "Buzz Cut",
        "image_url": "/static/images/hairstyles/buzz_cut.jpg",
        "target_face_shapes": "To'rtburchak, Oval, Olmos",
        "description": "Erkaklar uchun juda qulay, kalta va qat'iy ko'rinish. Jag' chiziqlarini ta'kidlaydi."
    },
    {
        "name": "Classic Side Part",
        "image_url": "/static/images/hairstyles/side_part.jpg",
        "target_face_shapes": "Oval, Dumaloq, To'rtburchak, Yurak",
        "description": "Har qanday vaziyatga mos tushadigan klassik va jiddiy uslub."
    },
    {
        "name": "Textured Quiff",
        "image_url": "/static/images/hairstyles/quiff.jpg",
        "target_face_shapes": "Dumaloq, To'rtburchak, Oval",
        "description": "Sochni tepaga va orqaga qilib taraladigan hajmli zamonaviy turmak."
    },
    {
        "name": "Slicked Back Undercut",
        "image_url": "/static/images/hairstyles/slick_back.jpg",
        "target_face_shapes": "Oval, To'rtburchak, Yurak",
        "description": "Yonlari juda kalta (undercut) va tepasi orqaga silliq taralgan zamonaviy uslub."
    },
    {
        "name": "Messy Angular Fringe",
        "image_url": "/static/images/hairstyles/fringe.jpg",
        "target_face_shapes": "Dumaloq, Yurak, Oval, Cho'ziq",
        "description": "Oldingi qismi pastga tushib turuvchi biroz tartibsiz va yoshlarga xos uslub."
    },
    {
        "name": "Skin Fade with Textured Top",
        "image_url": "/static/images/hairstyles/mannequin_fade_1787470884347.jpg",
        "target_face_shapes": "Oval, Dumaloq, Olmos",
        "description": "Yonlari to'liq (skin) qirib olingan va tepasi teksturali tekis turmak."
    },
    {
        "name": "Classic Taper",
        "image_url": "/static/images/hairstyles/mannequin_classic_1787470904210.jpg",
        "target_face_shapes": "Oval, To'rtburchak, Yurak, Dumaloq",
        "description": "Yonlari va orqasi chiroyli qisqarib boruvchi doimiy klassik va xushbichim ko'rinish."
    },
    {
        "name": "Modern Mullet",
        "image_url": "/static/images/hairstyles/mannequin_modern_1787470923962.jpg",
        "target_face_shapes": "Oval, Cho'ziq, To'rtburchak",
        "description": "Oldi va yonlari kalta, orqa qismi uzun bo'lgan trenddagi zamonaviy mullet."
    }
]

for h in hairstyles:
    obj, created = Hairstyle.objects.get_or_create(
        name=h['name'],
        defaults={
            'image_url': h['image_url'],
            'target_face_shapes': h['target_face_shapes'],
            'description': h['description']
        }
    )
    if created:
        print(f"Qo'shildi: {h['name']}")
    else:
        print(f"Allaqachon mavjud: {h['name']}")

print("10 ta asosiy soch turmagi bazaga muvaffaqiyatli yuklandi!")
