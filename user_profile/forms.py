from django import forms
from .models import MatrimonialProfile

class MatrimonialProfileForm(forms.ModelForm):
    class Meta:
        model = MatrimonialProfile
        exclude = ['user','created_at','updated_at']
        widgets = {
            'about': forms.Textarea (
                attrs={
                    'rows':4,
                    'placeholder':'Tell About Yourself'
                }
            )
        }