from django.urls import path
from . import views
from apps.gallery import views as gall_views


app_name = 'posts'
urlpatterns = [
    # post preview
    path('<int:post_id>', views.post_detail_view, name='post_detail_view'),

    # post create
    path('create', views.post_create, name='post_create'),
    path('create/upload_temp_images', gall_views.upload_temp_images, name='post_create_upload_temp_images'),
    path('create/delete_temp_images/<int:image_id>', gall_views.delete_temp_image,
         name='post_create_delete_temp_image'),
    path('create/delete_temp_images/all', gall_views.delete_all_temp_images, name='post_create_delete_all_temp_images'),

    # post edit
    path('<int:post_id>/edit', views.post_edit, name='post_edit'),
    path('<int:post_id>/edit/upload_temp_images', gall_views.upload_temp_images, name='post_edit_upload_temp_images'),
    path(
        '<int:post_id>/edit/delete_temp_images/<int:image_id>',
        gall_views.delete_temp_image,
        name='post_edit_delete_temp_image'
    ),
    path(
        '<int:post_id>/edit/delete_temp_images/all',
        gall_views.delete_all_temp_images,
        name='post_edit_delete_all_temp_images'
    ),
    path(
        '<int:post_id>/edit/post_image_status/<int:image_id>',
        gall_views.toggle_image_delete_status,
        name='post_edit_toggle_image_delete_status'
    ),

    # post delete
    path('<int:post_id>/delete', views.post_delete, name='post_delete'),
]
