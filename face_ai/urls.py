from django.urls import path
from . import views

urlpatterns = [
    path('analyze-face/', views.ai_analyze_face, name='ai-analyze-face'),
    path('chat/', views.ai_chat_text, name='ai-chat-text'),
]
