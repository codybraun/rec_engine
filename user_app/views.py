from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader
import requests 
import random
from user_app.models import *
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.forms.models import model_to_dict 
from rest_framework.decorators import api_view

def logout_user(request):
  logout(request)
  return HttpResponseRedirect("/login/")

def login_user(request):
  context={'form':LoginForm}
  if request.method=="POST":
    username = str(request.POST['username'])
    password = str(request.POST['password'])
    user = authenticate(username=username, password=password)   
    if user is not None:
      login(request, user)
      return HttpResponseRedirect("/")
    else:
      template = loader.get_template("recs/login.html")
      context['error']="Username and password are not correct."
      return HttpResponse(template.render(context, request))
  else:
    if request.user.is_authenticated:  
      return HttpResponseRedirect("/")
    else:
      template = loader.get_template("recs/login.html")
      return HttpResponse(template.render(context, request))
  
def new_user(request):
  template = loader.get_template("recs/new_user.html")
  if request.method=="POST":
    form = UserForm(request.POST)
    if form.is_valid():
        print form.cleaned_data
        user = User(username=form.cleaned_data.get("username",""), email=form.cleaned_data.get("email",""))
        user.set_password(form.cleaned_data["password"])
        user.save()
        return HttpResponseRedirect("/login/")
    else:
        print "ERRORS " + str(form.errors)
        return HttpResponse(template.render({'form':UserForm, "errors":form.errors}, request))
  else:
      context={'form':UserForm()}
      return HttpResponse(template.render(context, request))

def profile(request):
  context={}
  if request.user.is_authenticated:  
    template = loader.get_template("recs/profile.html")
    return HttpResponse(template.render(context, request))
  else:
    return HttpResponseRedirect("/login/")

def docs(request):
  template = loader.get_template("recs/docs.html")
  context = {}
  return HttpResponse(template.render(context, request))
