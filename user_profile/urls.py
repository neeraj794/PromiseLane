from django.urls import path
from .views import *

urlpatterns = [
    path('create_profile/',create_profile,name='create_profile'),
    path('update_user_profile/',update_user_profile,name='update_user_profile')
]