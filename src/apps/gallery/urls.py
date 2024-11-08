from django.urls import path
from . import views

app_name = 'gallery'
urlpatterns = [
    # album preview
    path('albums/<str:uuid_url>', views.album_preview, name='album_preview'),

    # album create
    path('albums_create', views.album_create, name='album_create'),
    path('albums_create/upload_temp_images', views.upload_temp_images, name='album_create_upload_temp_images',),
    path(
        'albums_create/delete_temp_images/<int:image_id>',
        views.delete_temp_image,
        name='album_create_delete_temp_image'
    ),
    path(
        'albums_create/delete_temp_images/all',
        views.delete_all_temp_images,
        name='album_create_delete_all_temp_images'
    ),

    # album edit
    path('albums/<str:uuid_url>/edit', views.album_edit, name='album_edit'),
    path('albums/<str:uuid_url>/edit/upload_temp_images', views.upload_temp_images,
         name='album_edit_upload_temp_images',),
    path('albums/<str:uuid_url>/edit/delete_temp_images/<int:image_id>', views.delete_temp_image,
         name='album_edit_delete_temp_image'),
    path('albums/<str:uuid_url>/edit/delete_temp_images/all', views.delete_all_temp_images,
         name='album_edit_delete_all_temp_images'),
    path('albums/<str:uuid_url>/edit/album_image_status/<int:image_id>', views.toggle_image_delete_status,
         name='album_edit_toggle_image_delete_status'),

    # album delete
    path('albums/<str:uuid_url>/delete', views.album_delete, name='album_delete'),

    # photos management
    path('photo/<str:post_type>/p=<int:post_id>&pic=<int:image_id>', views.image_preview,
         name='image_preview'),
    path('photo/<str:post_type>/p=<int:post_id>&pic=<int:image_id>/edit', views.image_edit,
         name='image_edit'),
    path('photo/<str:post_type>/p=<int:post_id>&pic=<int:image_id>/delete', views.image_delete,
         name='image_delete'),
]
