from django import forms
from .models import BankDetails

class RegisterForm(forms.ModelForm):
    class Meta:
        model=BankDetails
        # fields="__all__"
        fields=['acc_num','name','phone','email','aadhar_num','profile','aadhar_photo','acc_type','Gender','address','occupation']
