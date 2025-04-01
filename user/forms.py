from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class SignUpForm(UserCreationForm):
    email= forms.EmailField(required= True)
    nickname = forms.CharField(max_length=50, required=True)  # 닉네임 필드 추가

    class Meta:
        model = CustomUser
        fields =['username','nickname','email','phone_number','password1','password2']