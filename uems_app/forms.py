from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth.models import User
from .models import Event

class RegisterForm(UserCreationForm):
    first_name = forms.TextInput(attrs={"required": True})
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
    description = forms.CharField(max_length=1024, required=True)
    location = forms.CharField(max_length=255, required=True)
    archived = forms.BooleanField(required=False)
    from_date = forms.DateTimeField()
    to_date = forms.DateTimeField()

    class Meta:
        model = Event
        fields = ["name", "description", "location", "archived", "from_date", "to_date"]