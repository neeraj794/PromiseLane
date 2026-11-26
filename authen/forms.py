from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import ProImage

User = get_user_model()

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'phone',
            'gender',
            'dob',
            'password1',
            'password2'
        ]
        widgets = {
            'dob':forms.DateInput(
                attrs={'type':'date'}
            )
        }

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'phone',
            'gender',
            'dob',
        ]

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = ProImage
        fields = ['Proimage']