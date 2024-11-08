from django.urls import path
from django.contrib.auth.views import LoginView
from . import views


app_name = 'users'
urlpatterns = [
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
]
