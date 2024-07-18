from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class EmailPostForm(forms.Form):
    name=forms.CharField(max_length=30)
    email=forms.EmailField()
    to=forms.EmailField()
    comments=forms.CharField(required=False,widget=forms.Textarea)


class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(label="First Name", max_length=100, required=False)
    last_name = forms.CharField(label="Last Name", max_length=100, required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password1', 'password2']

class LoginForm(forms.Form):
    username = forms.CharField(label="Username", max_length=100, required=False)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
