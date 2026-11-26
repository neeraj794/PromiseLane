from django.urls import path
from .views import *

urlpatterns = [
    path('',login_,name='login'),
    path('register/',register,name='register'),
    path('profile/',profile,name='profile'),
    path('logout/',logout_,name='logout'),
    path('update_password/',update_password,name='update_password'),
    path('update_profile/',update_profile,name='update_profile'),
    path('forgot_password/',forgot_password,name='forgot_password'),
    path('toggle_profile_visibility/',toggle_profile_visibility,name='toggle_profile_visibility')
]