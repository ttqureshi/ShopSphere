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
    contact_no = forms.CharField(max_length=13, widget=forms.TextInput({ "placeholder": "+923000000000"}))
    class Meta:
        model = models.Order
        fields = ["full_name", "contact_no", "address", "city", "state", "zipcode", "country"]


class UserUpdateForm(forms.ModelForm):
    username = forms.CharField(required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email"]
