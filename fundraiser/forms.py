from django import forms
from django.contrib.auth.models import User
from .models import  Project
import re

class RegistrationForm(forms.ModelForm):
    mobile = forms.CharField(max_length=11)
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model= User
        fields =["first_name","last_name","email","username","password1"]

    def clean_mobile(self):
        mobile = self.cleaned_data.get("mobile")
        pattern=r'^(010|011|012|015)\d{8}$'
        if not re.match(pattern, mobile):
            raise forms.ValidationError("Egyptian mobile number must start with 010/011/012/015 and be 11 digits.")
        return mobile
    
    def clean_password(self):
        data=super().clean()
        if data.get("password1") != data.get("password2"):
            raise forms.ValidationError("The password doesn't match")
        return data

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'details', 'target', 'start_date', 'end_date']

    def clean(self):
            cleaned_data = super().clean()
            start = cleaned_data.get("start_date")
            end = cleaned_data.get("end_date")

            if start and end:
                if start > end:
                    raise forms.ValidationError("End date must be after start date")

            return cleaned_data

