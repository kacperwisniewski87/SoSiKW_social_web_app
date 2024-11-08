from django.urls import path
from . import views

app_name = 'friends'
urlpatterns = [
    path('all/', views.friends_all_view, name='friends_all_view'),
    path('requests/received/', views.friends_requests_received_view, name='friends_requests_received_view'),
    path('requests/rejected/', views.friends_requests_rejected_view, name='friends_requests_rejected_view'),
    path('requests/sent/', views.friends_requests_sent_view, name='friends_requests_sent_view'),
    path('blocked/', views.blocked_users_view, name='blocked_users_view'),
    path('search/', views.friends_search_view, name='friends_search_view'),

    # request management AJAX
    path('send_request/<int:user_id>/', views.send_friend_request, name='send_friend_request'),
    path(
        'requests/received/accept/<int:friendship_request_id>',
        views.friends_request_accept,
        name='friends_request_accept'),
    path(
        'requests/received/reject/<int:friendship_request_id>',
        views.friends_request_reject,
        name='friends_request_reject'),
    path(
        'requests/sent/cancel/<int:friendship_request_id>',
        views.friends_request_cancel,
        name='friends_request_cancel'),

    # friend removal
    path('remove/<int:friend_id>/', views.friends_remove_friend, name='friends_remove_friend'),

    # block management AJAX
    path(
        "blocked/add/<str:request_type>/<int:user_id>/",
        views.blocked_add_block,
        name="blocked_add_block"),
    path(
        "blocked/remove/<int:user_id>/",
        views.blocked_remove_block,
        name="blocked_remove_block"),

    # user search AJAX
    path('search/xyz/', views.friends_search_result, name='friends_search_result'),

    # friendships info management AJAX
    path('friendship-status/<int:user_id>/', views.check_friendship_status, name='check_friendship_status'),
]
