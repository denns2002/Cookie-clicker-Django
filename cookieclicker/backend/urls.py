from django.urls import path
from . import views

urlpatterns = [
    path('register', views.Register, name='register'),
    path('login', views.User_login, name='login'),
    path('logout', views.User_logout, name='logout'),
    path('', views.index, name='index'),
]
