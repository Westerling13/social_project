from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError

from .models import Story, Profile, Comment


class SignUpForm(UserCreationForm):
    # username = forms.CharField(label=)
    first_name = forms.CharField(label='Имя')
    last_name = forms.CharField(label='Фамилия')
    email = forms.EmailField(label='Электронный адрес')

    def clean(self):
        super().clean()
        username = self.cleaned_data['username']
        if '@' in username:
            raise ValidationError('Извините, имя пользователя не может содержать @')

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


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
