from django.urls import path

from .views import chat_page, ChatHistoryView, MyChatRoomsView, ChatMessageUploadView, start_chat_view

urlpatterns = [
    path('rooms/', MyChatRoomsView.as_view(), name='my-rooms'),
    path('start/<int:user_id>/', start_chat_view, name='start-chat'),
    path('<int:order_id>/messages/', ChatHistoryView.as_view(), name='chat-history'),
    path('<int:order_id>/upload/', ChatMessageUploadView.as_view(), name='chat-upload'),
    path('<int:order_id>/', chat_page, name='chat-page-room'),
    path('', chat_page, name='chat-page'),
]