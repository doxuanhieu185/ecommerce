from typing import Any
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class CreateUserForms(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        
    def __init__(self, *args, **kwargs):
        super(CreateUserForms, self).__init__(*args, **kwargs)
        self.fields['email'].required = True 
        
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email đã được sử dụng')
        
        if len(email) > 350:
            raise forms.ValidationError('Email quá dài!')
        
        return email