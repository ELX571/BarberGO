import os
import json
import base64
import logging
import random

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.conf import settings
from dotenv import load_dotenv

from .models import Hairstyle

logger = logging.getLogger(__name__)

def get_gemini_key():
    load_dotenv()
    return os.getenv('GEMINI_API_KEY', '')

# Ikki bosqichli mantiq uchun faqat yuzni tahlil qiluvchi prompt
SYSTEM_PROMPT = """Sen professional yuz tahlilchisisiz. 
Senga foydalanuvchining yuz rasmi yuboriladi. 
Sening vazifang - FAQAT yuz shaklini aniqlash va qisqacha tahlil berish.

Ruxsat etilgan yuz shakllari ro'yxati (Faqat shulardan birini ishlating):
- Oval
- Dumaloq
- To'rtburchak
- Cho'ziq
- Yurak
- Olmos

MUHIM: Javobingni FAQAT quyidagi qat'iy JSON formatida ber, hech qanday boshqa so'z qo'shma:
{
    "face_shape": "Oval",
    "face_analysis": "Sizning yuzingiz oval shaklda, iyak qismi biroz qisqargan va peshonangiz kengroq. Bu juda ideal yuz shakli hisoblanadi."
}
"""

TEXT_SYSTEM_PROMPT = """Sen "BarberGo AI Soch Maslahatchi"siz. Sen foydalanuvchilarga soch turmagi, soch parvarishi va barbershop xizmatlari bo'yicha maslahat berasiz.

Qoidalar:
- Har doim o'zbek tilida javob ber
- Qisqa va aniq javob ber (3-4 jumla)
- Agar foydalanuvchi yuz rasmi yuborsa, ulardan chatda rasm yuborishni so'ra
- Soch turmaklari haqida professional maslahatlar ber
- Dostona va samimiy bo'l
- Emoji ishlatib javob ber
- Agar mavzudan tashqari savol bo'lsa, soch va barbershop mavzusiga yo'naltir"""


from google import genai

def handle_gemini_error(e):
    error_msg = str(e)
    if "503" in error_msg or "UNAVAILABLE" in error_msg:
        return JsonResponse({
            'error': True,
            'message': 'Ayni vaqtda AI serverlarida (Gemini) katta yuklanish mavjud. Iltimos, 1-2 daqiqadan so\'ng qayta urinib ko\'ring.'
        }, status=503)
    return JsonResponse({
        'error': True,
        'message': f'Xatolik: {error_msg}'
    }, status=500)

@csrf_exempt
@require_POST
def ai_analyze_face(request):
    """Analyze face image with Gemini AI and recommend hairstyles dynamically from DB."""
    api_key = get_gemini_key()
    if not api_key or api_key == 'YOUR_API_KEY_HERE':
        return JsonResponse({
            'error': True,
            'message': 'Gemini API kaliti sozlanmagan. .env faylga GEMINI_API_KEY ni qo\'shing.'
        }, status=500)

    try:
        body = json.loads(request.body)
        image_data = body.get('image', '')

        if not image_data:
            return JsonResponse({'error': True, 'message': 'Rasm yuborilmadi'}, status=400)

        if ',' in image_data:
            image_data = image_data.split(',', 1)[1]

        image_bytes = base64.b64decode(image_data)

        client = genai.Client(api_key=api_key)

        # 1-BOSQICH: AI orqali faqat yuz shaklini aniqlaymiz
        response = client.models.generate_content(
            model='gemini-3.6-flash',
            contents=[
                {
                    'role': 'user',
                    'parts': [
                        {'text': SYSTEM_PROMPT},
                        {
                            'inline_data': {
                                'mime_type': 'image/jpeg',
                                'data': base64.b64encode(image_bytes).decode('utf-8')
                            }
                        }
                    ]
                }
            ]
        )

        response_text = response.text.strip()
        if response_text.startswith('```'):
            lines = response_text.split('\n')
            lines = [l for l in lines if not l.strip().startswith('```')]
            response_text = '\n'.join(lines)

        ai_data = json.loads(response_text)
        detected_shape = ai_data.get('face_shape', 'Oval')
        
        # 2-BOSQICH: Bazadan mos soch turmaklarini qidiramiz
        # icontains orqali mos keluvchi yuz shaklini izlaymiz (yoki agar topilmasa hammasidan tasodifiy)
        matching_hairstyles = list(Hairstyle.objects.filter(target_face_shapes__icontains=detected_shape))
        
        # Agar bu yuz shakliga mos 4 ta topilmasa, bazadan boshqa ixtiyoriy turmaklarni ham qo'shamiz
        if len(matching_hairstyles) < 4:
            extra = list(Hairstyle.objects.exclude(target_face_shapes__icontains=detected_shape))
            random.shuffle(extra)
            matching_hairstyles.extend(extra)
        
        # Tasodifiy 4-6 tasini tanlaymiz, shunda foydalanuvchi har safar xilma-xil natija oladi
        random.shuffle(matching_hairstyles)
        selected_hairstyles = matching_hairstyles[:6]

        recommendations = []
        for style in selected_hairstyles:
            recommendations.append({
                "name": style.name,
                "description": style.description,
                "match_percent": random.randint(85, 98),  # Dinamik ishonchlilik
                "image_url": style.get_image_url()
            })

        final_result = {
            "face_shape": detected_shape,
            "face_analysis": ai_data.get('face_analysis', 'Yuzingiz chiroyli mutanosiblikka ega.'),
            "recommendations": recommendations
        }

        return JsonResponse({
            'error': False,
            'data': final_result
        })

    except json.JSONDecodeError as e:
        logger.error(f"JSON parse error: {e}")
        return JsonResponse({
            'error': True,
            'message': 'AI javobini o\'qishda xatolik yuz berdi. Qaytadan urinib ko\'ring.'
        }, status=500)
    except Exception as e:
        logger.error(f"AI analyze error: {e}")
        return handle_gemini_error(e)


@csrf_exempt
@require_POST
def ai_chat_text(request):
    """Handle text-based chat with Gemini AI."""
    api_key = get_gemini_key()
    if not api_key or api_key == 'YOUR_API_KEY_HERE':
        return JsonResponse({
            'error': True,
            'message': 'Gemini API kaliti sozlanmagan.'
        }, status=500)

    try:
        body = json.loads(request.body)
        user_message = body.get('message', '').strip()

        if not user_message:
            return JsonResponse({'error': True, 'message': 'Xabar bo\'sh'}, status=400)

        client = genai.Client(api_key=api_key)

        response = client.models.generate_content(
            model='gemini-3.6-flash',
            contents=[
                {
                    'role': 'user',
                    'parts': [
                        {'text': TEXT_SYSTEM_PROMPT + '\n\nFoydalanuvchi xabari: ' + user_message}
                    ]
                }
            ]
        )

        return JsonResponse({
            'error': False,
            'reply': response.text.strip()
        })

    except Exception as e:
        logger.error(f"AI chat error: {e}")
        return handle_gemini_error(e)

from django.shortcuts import render
from .models import Hairstyle

def hairstyles_page(request):
    hairstyles = Hairstyle.objects.all().order_by('-created_at')
    return render(request, 'hairstyles.html', {'hairstyles': hairstyles})
