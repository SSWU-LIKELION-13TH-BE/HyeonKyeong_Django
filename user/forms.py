from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from django.forms import ModelForm
from .models import *

class SignUpForm(UserCreationForm):
    email= forms.EmailField(required= True)
    nickname = forms.CharField(max_length=50, required=True)  # 닉네임 필드 추가

    class Meta:
        model = CustomUser
        fields =['username','nickname','email','phone_number','password1','password2']


class BoardForm(ModelForm):
    class Meta:
        model = Board
        fields = ['title', 'content', 'writer','image', 'stacks', 'github_link']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

class ProfileUpdateForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'nickname', 'email']



class GuestbookForm(forms.ModelForm):
    class Meta:
        model = Guestbook
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': '방명록을 남겨보세요!'}),
        }