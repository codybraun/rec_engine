from django import forms
from user_app.models import *
from django.core.exceptions import ValidationError

class UserForm(forms.Form):
  username = forms.CharField()
  def clean_password(self):
     if (len(self.cleaned_data["password"]) < 7):
        raise ValidationError("Password must be at least seven characters long")
     return self.cleaned_data["password"]
  def clean_username(self):
     if (User.objects.filter(username=self.cleaned_data["username"])):
        raise ValidationError("A user with that username already exists")
     return self.cleaned_data["username"]
  def clean_email(self):
     if not ("." in self.cleaned_data["email"] and "@" in self.cleaned_data["email"]): 
        raise ValidationError("Must enter a valid email address")
     return self.cleaned_data["email"]
  email = forms.CharField()
  password = forms.CharField(widget=forms.PasswordInput())
  widgets = {
    'password': forms.CharField(widget=forms.PasswordInput())
  }

class LoginForm(forms.Form):
  username = forms.CharField()
  password = forms.CharField(widget=forms.PasswordInput())
  widgets = {
    'password': forms.CharField(widget=forms.PasswordInput())
  }
