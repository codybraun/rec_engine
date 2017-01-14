from django import forms
from user_app.models import *
class UserForm(forms.Form):

  password = forms.CharField()
  username = forms.CharField()
  email = forms.CharField()
  widgets = {
    'password': forms.PasswordInput(),
  }
class LoginForm(forms.Form):
  password = forms.CharField()
  username = forms.CharField()
  widgets = {
    'password': forms.CharField(),
  }
