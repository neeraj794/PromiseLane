from django.urls import path
from .views import *

urlpatterns = [
    path('send_interest/<int:pk>',send_interest,name='send_interest'),
    path('sent_interests/',sent_interests,name='sent_interests'),
    path('received_interests/',recieved_interests,name='received_interests'),
    path('recieved_interests/',recieved_interests,name='recieved_interests'),
    path('respond_interests/<int:pk>',respond_interests,name='respond_interests'),
    path('unblock_user/<int:pk>',unblock_user,name='unblock_user'),
    path('block_user/<int:pk>',block_user,name='block_user'),
    path('blocked_users/',blocked_users,name='blocked_users'),
    path('report_profile/<int:pk>',report_profile,name='report_profile'),
    path('partner_preferences/',partner_preferences,name='partner_preferences'),
    path('matches/',matches,name='matches')
]