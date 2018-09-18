"""newpro URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from .views import e_handler404, e_handler500, MyPasswordResetConfirmView
from django.conf.urls.static import  static
from . import views
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetCompleteView

# from django.views.generic import RedirectView



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.first_page, name = 'first_page'),
    path('profiles/', include('profiles.urls', namespace = 'profiles')),
    path('mywall/', views.mywall, name ='mywall'),
    path('news/', views.news, name = 'news'),
    path('news/ajax_scroll_news/', views.ajax_scroll_news),
    path('news/ajax_comment_from_news/', views.ajax_comment_from_news),
    path('news/ajax_comment_comment_from_news/', views.ajax_comment_comment_from_news),
    path('news/ajax_post_delete_from_news/', views.ajax_post_delete_from_news),
    path('news/ajax_repost_from_news/', views.ajax_repost_from_news),
    path('search/', views.search, name = 'search'),
    path('post/', include('posts.urls', namespace = 'posts')),
    path('login/', views.login_user, name = 'login'),
    path('password/reset/', PasswordResetView.as_view(), name = 'password_reset'),
    path('password/reset/done/', PasswordResetDoneView.as_view(), name = 'password_reset_done'),
    path('password/reset/<uidb64>/<token>/', MyPasswordResetConfirmView.as_view(), name = 'password_reset_confirm'),
    path('password/reset/complete/', PasswordResetCompleteView.as_view(), name = 'password_reset_complete'),
    path('logout/', views.logout_user, name='logout'),
    path('registration/', views.registration, name = 'registration'),
    path('create_profile/', views.create_profile, name = 'create_profile'),
    path('change_password/', views.change_password, name = 'change_password'),
    path('edit_profile/', views.edit_profile, name = 'edit_profile'),
    path('delete_user_confirm/', views.delete_user_confirm, name = 'delete_user_confirm'),
    path('delete_user_action/', views.delete_user_action, name= 'delete_user_action'),
    path('<int:user_id>/', views.wall, name = 'wall'),
    path('<int:user_id>/ajax_scroll_wall/', views.ajax_scroll_wall),
    path('<int:user_id>/ajax_post/', views.ajax_posting, name ='ajax_post'),
    path('<int:user_id>/ajax_like/', views.ajax_like, name ='ajax_like'),
    path('<int:user_id>/ajax_status/', views.ajax_status, name ='ajax_status'),
    path('<int:user_id>/ajax_give_access/', views.ajax_give_access, name = 'ajax_give_access'),
    path('<int:user_id>/ajax_black_book/', views.ajax_black_book, name = 'ajax_black_book'),
    path('news/ajax_status_from_news/', views.ajax_status_from_news, name ='ajax_status_from_news'),
    path('news/ajax_like_from_news/', views.ajax_like_from_news, name ='ajax_like_from_news'),
    path('<int:user_id>/ajax_repost/', views.ajax_repost, name ='ajax_repost'),
    path('<int:user_id>/ajax_simple_subscribe/', views.ajax_simple_subscribe, name ='ajax_simple_subscribe'),
    path('<int:user_id>/ajax_simple_unsubscribe/', views.ajax_simple_unsubscribe, name ='ajax_simple_unsubscribe'),
    path('<int:user_id>/ajax_post_delete/', views.ajax_post_delete, name ='ajax_post_delete'),
    path('<int:user_id>/ajax_write/', views.ajax_write, name ='ajax_write'),
    path('like/', include('likes.urls', namespace = 'likes')),
    path('avatarize/', views.avatarize, name = 'avatarize'),
    path('notifications/', views.notifications, name = 'notifications'),
    path('liked_objects/', views.liked_objects, name = 'liked_objects'),
    path('notifications/ajax_notif_update/', views.ajax_notif_update, name = 'ajax_notif_update'),
    path('messages/', include('messenger.urls', namespace = 'messenger')),
    path('<int:user_id>/ajax_comment/', views.ajax_comment, name ='ajax_comment'),
    path('<int:user_id>/ajax_comment_comment/', views.ajax_comment_comment, name ='ajax_comment_comment'),
    # path('favicon\.ico', RedirectView.as_view(url='/static/images/favicon.ico'), name='favicon'),

    # path('captcha/', include('captcha.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)


handler404 = 'newpro.views.e_handler404'
handler500 = 'newpro.views.e_handler500'
