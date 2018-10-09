from django.urls import path
from . import views

app_name = 'messenger'

urlpatterns = [
    path('chats/', views.chat_list, name = 'chat_list'),
    path('chat/<int:chat_id>/', views.chat, name = 'chat'),
    path('chat/<int:chat_id>/add_member/', views.add_member, name='add_member'),
    path('chat/<int:chat_id>/add_member/ajax_add_member/', views.ajax_add_member),
    path('chat/<int:chat_id>/ajax_scroll_messages/', views.ajax_scroll_messages),
    path('chat/<int:chat_id>/ajax_message/', views.ajax_message, name = 'ajax_message'),
    path('chat/<int:chat_id>/ajax_read_message/', views.ajax_read_message, name = 'ajax_read_message'),
    path('chat/<int:chat_id>/ajax_change_chat_name/', views.ajax_change_chat_name),
    path('chat/<int:chat_id>/ajax_change_chat_avatar/', views.ajax_change_chat_avatar),
    path('chat/<int:chat_id>/ajax_update_chat/', views.ajax_update_chat),
    path('chat/<int:chat_id>/ajax_drop_chat/', views.ajax_drop_chat),
    path('create_chat/', views.create_chat, name = 'create_chat'),
    path('create_chat/ajax_make_chat/', views.ajax_make_chat, name = 'ajax_make_chat'),
]
