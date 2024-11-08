from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('r/', views.rooms_all, name='rooms_view'),
    path('<str:uuid_url>/', views.room_detail, name='room_detail_view'),

    # AJAX basic views
    path('r/create_group_chat', views.create_group_chat, name='create_group_chat'),
    path('r/add_to_group_results', views.add_to_group_chat_search_result, name='add_to_group_chat_search_result'),

    # AJAX group chat views
    path('<str:uuid_url>/add', views.add_friends_to_group_chat, name='add_friends_to_group_chat'),
    path('<str:uuid_url>/rename', views.rename_group_chat, name='rename_group_chat'),
    path('<str:uuid_url>/leave', views.leave_group_chat, name='leave_group_chat'),

    # AJAX non friend first message
    path('r/create_chat_with_user', views.create_chat_with_user, name='create_chat_with_user'),
]
