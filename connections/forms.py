from django import forms
from .models import Report,PartnerPreFerences

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['reason','description']
        widgets = {
            'description':forms.Textarea(
                attrs={
                    'rows':4,
                    'placeholder':'Explain why you are reporting this profile'
                }
            )
        }

class PartnerPreFerenceForm(forms.ModelForm):
    class Meta:
        model = PartnerPreFerences
        fields = ['min_age','max_age','preferred_gender','religion','marital_status','city']
        widgets = {
            'min_age':forms.NumberInput(
                attrs={
                    'min':18,
                    'max':100
                }
            ),
            'max_age':forms.NumberInput(
                 attrs={
                    'min':18,
                    'max':100
                }
            ),
            'city':forms.TextInput(
                attrs={
                    'placeholder':'Enter the preferred City'
                }
            )
        }

        def clean(self):
            cleaned_data = super().clean()

            min_age = cleaned_data.get('min_age')
            max_age = cleaned_data.get('max_age')

            if min_age and max_age and min_age > max_age:
                raise forms.ValidationError("Minimum age cannot be greater than maximum age.")
            if min_age and min_age < 18:
                raise forms.ValidationError("Minimum age must be atleast 18")
            return cleaned_data
