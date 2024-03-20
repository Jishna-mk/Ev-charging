from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.models import User


class UserAddForm(UserCreationForm):
    class Meta:
        model =User
        fields=["username","email","password1","password2"]

from django import forms
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user',)        