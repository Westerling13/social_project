from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from .models import Story, Profile


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(label='Имя')
    last_name = forms.CharField(label='Фамилия')
    email = forms.EmailField(label='Электронный адрес')

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')


class StoryAddForm(forms.ModelForm):
    class Meta:
        model = Story
        fields = ('title', 'as_md', 'text', 'published')


class SettingsForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = (
            'first_name', 'last_name', 'email', 'gender', 'birth_date', 'image', 'bio', 'is_private'
        )
