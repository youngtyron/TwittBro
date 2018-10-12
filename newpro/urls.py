from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from .views import e_handler404, e_handler500, MyPasswordResetConfirmView, PeopleListView, OnePostView
from django.conf.urls.static import  static
from . import views, ajax
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetCompleteView



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.first_page, name = 'first_page'),
    path('ajax_update_messages/', ajax.ajax_update_messages),
    path('mywall/', views.mywall, name ='mywall'),
    path('login/', views.login_user, name = 'login'),
    path('logout/', views.logout_user, name='logout'),
    path('registration/', views.registration, name = 'registration'),
    path('avatarize/', views.avatarize, name = 'avatarize'),
    path('avatarize/ajax_avatarize/', ajax.ajax_avatarize),
    path('change_password/', views.change_password, name = 'change_password'),
    path('edit_profile/', views.edit_profile, name = 'edit_profile'),
    path('edit_profile/ajax_update_profile/', ajax.ajax_update_profile),
    path('edit_profile/ajax_avatar_remove/', ajax.ajax_avatar_remove),
    path('delete_user_confirm/', views.delete_user_confirm, name = 'delete_user_confirm'),
    path('delete_user_action/', views.delete_user_action, name= 'delete_user_action'),
    path('password/reset/', PasswordResetView.as_view(), name = 'password_reset'),
    path('password/reset/done/', PasswordResetDoneView.as_view(), name = 'password_reset_done'),
    path('password/reset/<uidb64>/<token>/', MyPasswordResetConfirmView.as_view(), name = 'password_reset_confirm'),
    path('password/reset/complete/', PasswordResetCompleteView.as_view(), name = 'password_reset_complete'),
    path('people/', PeopleListView.as_view(), name = 'people'),
    path('people/ajax_scroll_people/', ajax.ajax_scroll_people),
    path('news/', views.news, name = 'news'),
    path('news/ajax_scroll_news/', ajax.ajax_scroll_news),
    path('news/ajax_comment/', ajax.ajax_comment_from_news),
    path('news/ajax_comment_comment/', ajax.ajax_comment_comment_from_news),
    path('news/ajax_post_delete_from_news/', ajax.ajax_post_delete_from_news),
    path('news/ajax_repost_from_news/', ajax.ajax_repost_from_news),
    path('news/ajax_like_from_news/', ajax.ajax_like_from_news, name ='ajax_like_from_news'),
    path('search/', views.search, name = 'search'),
    path('search/ajax_scroll_postresults/', ajax.ajax_scroll_postresults),
    path('search/ajax_like_from_results/', ajax.ajax_like_from_results),
    path('search/ajax_repost_from_results/', ajax.ajax_repost_from_results),
    path('search/ajax_comment/', ajax.ajax_comment_from_results),
    path('search/ajax_comment_comment/', ajax.ajax_comment_comment_from_results),
    path('search/ajax_post_delete_from_results/', ajax.ajax_post_delete_from_results),
    path('<int:user_id>/', views.wall, name = 'wall'),
    path('<int:user_id>/ajax_scroll_wall/', ajax.ajax_scroll_wall),
    path('<int:user_id>/ajax_post/', ajax.ajax_posting, name ='ajax_post'),
    path('<int:user_id>/ajax_like/', ajax.ajax_like, name ='ajax_like'),
    path('<int:user_id>/ajax_status/', ajax.ajax_status, name ='ajax_status'),
    path('<int:user_id>/ajax_give_access/', ajax.ajax_give_access, name = 'ajax_give_access'),
    path('<int:user_id>/ajax_black_book/', ajax.ajax_black_book, name = 'ajax_black_book'),
    path('<int:user_id>/ajax_repost/', ajax.ajax_repost, name ='ajax_repost'),
    path('<int:user_id>/ajax_simple_subscribe/', ajax.ajax_simple_subscribe, name ='ajax_simple_subscribe'),
    path('<int:user_id>/ajax_simple_unsubscribe/', ajax.ajax_simple_unsubscribe, name ='ajax_simple_unsubscribe'),
    path('<int:user_id>/ajax_post_delete/', ajax.ajax_post_delete, name ='ajax_post_delete'),
    path('<int:user_id>/ajax_write/', ajax.ajax_write, name ='ajax_write'),
    path('<int:user_id>/ajax_comment/', ajax.ajax_comment, name ='ajax_comment'),
    path('<int:user_id>/ajax_comment_comment/', ajax.ajax_comment_comment, name ='ajax_comment_comment'),
    path('notifications/', views.notifications, name = 'notifications'),
    path('liked_objects/', views.liked_objects, name = 'liked_objects'),
    path('notifications/ajax_notif_update/', ajax.ajax_notif_update, name = 'ajax_notif_update'),
    path('messages/', include('messenger.urls', namespace = 'messenger')),
    path('post/<int:post_id>/', OnePostView.as_view(), name = 'post_detail'),
    path('post/<int:post_id>/ajax_like/', ajax.ajax_like_post_detail),
    path('post/<int:post_id>/ajax_repost/', ajax.ajax_repost_post_detail),
    path('post/<int:post_id>/ajax_comment/', ajax.ajax_comment_from_detail),
    path('post/<int:post_id>/ajax_comment_comment/', ajax.ajax_comment_comment_from_detail),
    path('post/<int:post_id>/ajax_post_delete_from_detail/', ajax.ajax_post_delete_from_detail),

]
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)


handler404 = 'newpro.views.e_handler404'
handler500 = 'newpro.views.e_handler500'
