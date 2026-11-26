from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from datetime import date
from django.core.exceptions import ValidationError

# Create your models here.
def validate_age(value):
    today = date.today()
    if value > today:
        raise ValidationError('date of birth cannot be in the future')
    age = today.year - value.year
    if (today.month , today.day) < (value.month , value.day):
        age -= 1
    if age < 18:
        raise ValidationError('you must be atleast 18 years old to register')
    
class ProImage(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    Proimage = models.ImageField(upload_to='profile/',default='image.png')

class CustomUser(AbstractUser):
    age = models.PositiveIntegerField(default=0)
    phone = models.IntegerField(default=0)
    gender = models.CharField(max_length=30,blank=True)
    dob = models.DateField(null=True,blank=True,validators={validate_age})

