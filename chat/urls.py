from django.urls import path

from .views import chat_page, ChatHistoryView, MyChatRoomsView

urlpatterns = [
    path('rooms/', MyChatRoomsView.as_view(), name='my-rooms'),
    path('<int:order_id>/messages/', ChatHistoryView.as_view(), name='chat-history'),
    path('<int:order_id>/', chat_page, name='chat-page-room'),
    path('', chat_page, name='chat-page'),
]