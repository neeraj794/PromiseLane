from django.urls import path
from .views import *

urlpatterns = [
    path('',home,name='home'),
    path('browse_profiles/',browse_profiles,name='browse_profiles'),
    path('profile_detail/<int:pk>',profile_detail,name='profile_detail')
]