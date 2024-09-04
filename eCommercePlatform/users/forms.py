from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from . import models


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class OrderForm(forms.ModelForm):
    class Meta:
        model = models.Order
        fields = ["full_name", "address", "city", "state", "zipcode", "country"]


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email"]
