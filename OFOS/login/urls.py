from django.contrib import admin
from django.urls import path,include
from .views import *
app_name = "login"

urlpatterns = [
    path('register/',register,name='register'),
    path('home/',home,name='home'),
    path('',login_request,name='login')
]