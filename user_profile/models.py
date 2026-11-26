from django.db import models
from authen.models import CustomUser

# Create your models here.
class MatrimonialProfile(models.Model):
    RELIGION_CHOICES = [
        ('Hindu','Hindu'),
        ('Muslim','Muslim'),
        ('Christian','Christaian'),
        ('Other','Other')
    ]
    MARITAL_STATUS_CHOICES = [
        ('Single','Single'),
        ('Divorced','Divorced'),
        ('Widowed','Widowed'),
    ]
    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE,related_name='matrimonial_profile')
    religion = models.CharField(max_length=30,choices=RELIGION_CHOICES)
    caste = models.CharField(max_length=100,blank=True)
    height = models.CharField(max_length=20,blank=True)
    marital_status = models.CharField(
        max_length=30,
        choices = MARITAL_STATUS_CHOICES,
        default='Single'
    )
    education = models.CharField(max_length=150)
    occupation = models.CharField(max_length=150)
    annual_income = models.CharField(max_length=100,blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    about = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)