from django.urls import path
from . import views

app_name = 'account'
urlpatterns = [
    path('', views.profile_main_view, name='profile_main_view'),
    path('info', views.profile_info_view, name='profile_info_view'),
    path('info/edit', views.profile_info_edit_view, name='profile_info_edit_view'),
    path('friends', views.friends_main_view, name='friends_main_view'),
    path('gallery', views.user_all_photos_view, name='user_all_photos_view'),
    path('gallery_albums', views.user_albums_view, name='user_albums_view'),

    # ajax views
    path('hud_data', views.hud_open_get_user_data, name='hud_open_get_user_data'),
]
