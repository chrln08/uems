from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth.models import User
from .models import Event
from datetime import datetime

class RegisterForm(UserCreationForm):
    first_name = forms.TextInput()
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email", "password1", "password2"]

class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ["username", "password"]

class NewEventForm(forms.Form):
    name = forms.CharField(max_length=255, required=True)
    description = forms.CharField(max_length=1024, required=True, widget=forms.Textarea)
    location = forms.CharField(max_length=255, required=True)
    from_date = forms.DateField()
    to_date = forms.DateField()

    class Meta:
        model = Event
        fields = ["name", "description", "thumbnail", "location", "from_date", "to_date"]

class ChangePasswordForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = ["old_password", "new_password1", "new_password2"]