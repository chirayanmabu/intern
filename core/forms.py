from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

from .models import *


class CreateUserForm(UserCreationForm):
    username = forms.CharField(
        label = 'Username',
        widget=forms.TextInput(attrs={'placeholder': 'Username', 'class': 'form-control'})
    )
    email = forms.CharField(
        label='Email',
        widget=forms.TextInput(attrs={'placeholder': 'Email', 'class': 'form-control'})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm password', 'class': 'form-control'})
    )


    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ProfileForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['profile_pic'].label = False
        self.fields['banner_pic'].label = False
        self.fields['first_name'].label = False
        self.fields['last_name'].label = False
        self.fields['bio'].label = False
        self.fields['phone'].label = False
        self.fields['address'].label = False
        self.fields['gender'].label = False
        self.fields['dob'].label = False

    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]

    profile_pic = forms.ImageField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'file'})
    )
    banner_pic = forms.ImageField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'file'})
    )
    first_name = forms.CharField(
        min_length=2, max_length=30,
        widget=forms.TextInput(attrs={'placeholder': 'First name', 'class': 'form-control'})
    )
    last_name = forms.CharField(
        min_length=2, max_length=30,
        widget=forms.TextInput(attrs={'placeholder': 'Last name', 'class': 'form-control'})
    )
    bio = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Bio', 'class': 'form-control', 'rows': '3'})
    )
    phone = forms.CharField(
        widget=forms.TextInput(attrs={'type': 'number'})
    )
    address = forms.CharField(
        min_length=2, max_length=50,
        widget=forms.TextInput(attrs={'placeholder': 'Address'})
    )
    dob = forms.DateField(
        required=False,
        widget=forms.TextInput(attrs={'type': 'date'})
    )
    gender = forms.ChoiceField(
        choices=GENDER_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = UserInfo
        fields = '__all__'
        # exclude = ['user']


class PostForm(ModelForm):
    body = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={'rows': '3', 'placeholder': 'Caption'})
    )

    post_pic = forms.ImageField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'file'})
    )

    class Meta:
        model = Post
        fields = ['body', 'post_pic']


class CommentForm(ModelForm):
    comment = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={
            'placeholder': 'Comment',
            'class': 'form-control mb-0',
            'aria-label': 'Comment',
            'aria-describedby': 'Comment'
            })
    )

    class Meta:
        model = Comment
        fields = ['comment']