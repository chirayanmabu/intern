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
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]

    profile_pic = forms.ImageField(
        label='',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'file'})
    )
    banner_pic = forms.ImageField(
        label='',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'file'})
    )
    first_name = forms.CharField(
        label='',
        min_length=2, max_length=30,
        widget=forms.TextInput(attrs={'placeholder': 'First name', 'class': 'form-control'})
    )
    last_name = forms.CharField(
        label='',
        min_length=2, max_length=30,
        widget=forms.TextInput(attrs={'placeholder': 'Last name', 'class': 'form-control'})
    )
    bio = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={'placeholder': 'Bio', 'class': 'form-control', 'rows': '3'})
    )
    phone = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={'type': 'number'})
    )
    address = forms.CharField(
        label='',
        min_length=2, max_length=50,
        widget=forms.TextInput(attrs={'placeholder': 'Address'})
    )
    dob = forms.DateField(
        label='',
        required=False,
        widget=forms.TextInput(attrs={'type': 'date'})
    )
    gender = forms.ChoiceField(
        label='',
        choices=GENDER_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = UserProfile
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
            'aria-describedby': 'Comment',
            'name': 'comment'
            })
    )

    class Meta:
        model = Comment
        fields = ['comment']