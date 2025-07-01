from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):
    """
    A form for registering new users, extending Django's UserCreationForm.
    Fields:
        email (EmailField): The user's email address.
        Extended fields used in the custom form:
        - Username
        - Password
        - Confirm Password
    Meta:
        model (User): The user model to create.
        fields (list): The fields to include in the form: username, email, password1, password2.
    """

    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
