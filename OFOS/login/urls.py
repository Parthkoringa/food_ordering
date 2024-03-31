from django.contrib import admin
from django.urls import path,include
from .views import *
app_name = "login"

urlpatterns = [
    path('register/',register,name='register'),
    path('home/',home,name='home'),
    path('',landing,name='landing'),
    path('home/search',search,name="search"),
    path('logout/',logout_req,name='logout_req'),
    path('login/',login_request,name='login'),
    path('rest_prod/<int:id>',rest_prod,name='rest_prod'),
    path('reset_password/',reset_password,name='reset_password'),
    path('rest_prod/confirm_order<int:id>',confirm_order,name='confirm_order'),
    path('home/profile<int:id>',profile,name='profile'),
    path('confirm_order/download',download, name='download'),
    path('login/reset',reset,name='reset')
]