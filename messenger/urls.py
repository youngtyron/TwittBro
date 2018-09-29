from django.urls import path
from . import views
# from .views import ChatList

app_name = 'messenger'

urlpatterns = [
    # path('chats/', ChatList.as_view(), name = 'chat_list'),
    path('chats/', views.chat_list, name = 'chat_list'),
    path('chat/<int:chat_id>/', views.chat, name = 'chat'),
    path('chat/<int:chat_id>/ajax_scroll_messages/', views.ajax_scroll_messages),
    path('chat/<int:chat_id>/ajax_message/', views.ajax_message, name = 'ajax_message'),
    path('chat/<int:chat_id>/ajax_read_message/', views.ajax_read_message, name = 'ajax_read_message'),
    # path('start_chat/<user_id>/', views.start_chat, name = 'start_chat'),
    path('create_chat/', views.create_chat, name = 'create_chat'),
    path('create_chat/ajax_make_chat/', views.ajax_make_chat, name = 'ajax_make_chat'),
]
