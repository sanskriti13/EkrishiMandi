from django import forms
from .models import *

class FarmerRegister(forms.ModelForm):
    class Meta:
        model = farmers
        fields = ['name','email','zipcode','crop','qty','entrytime']
        widgets = {
        'name': forms.TextInput(attrs={'class':'form-control'}),
        'email': forms.EmailInput(attrs={'class':'form-control'}),
        'zipcode': forms.TextInput(attrs={'class':'form-control'}),
        'qty': forms.TextInput(attrs={'class':'form-control'}),
        'entrytime':forms.DateTimeInput(attrs={'class':'form-control'}),
        }
