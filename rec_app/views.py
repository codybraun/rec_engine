from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader
import requests 
import json
import random
from rec_app.models import *
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from django.core import serializers
import svd 
from rest_framework_swagger.views import get_swagger_view
from rest_framework.decorators import api_view
from rest_framework.decorators import authentication_classes
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth.models import User as Owner
schema_view = get_swagger_view(title=' API')

#TODO update SVD as actvitiy POSTed?
#Update user recs as activity posted, not when recs requested

@api_view(['POST','GET'])
@authentication_classes((TokenAuthentication,))
@csrf_exempt
def user(request):
  """
    POST to this endpoint to create a new user. The new user, with associated id, will be returned. 
  """
  if request.method=="POST":
    user = User.objects.create(owner=Owner.objects.get(id=request.user.id))
    user.save()
    return JsonResponse(model_to_dict(user))
  elif request.method=="GET":
    users = User.objects.filter(owner=request.user.id)
    return_value = []
    for user in users:
      return_value.append({"id":user.id})
    return JsonResponse(return_value, safe=False)

@api_view(['POST','GET'])
@authentication_classes((TokenAuthentication,))
@csrf_exempt
def product(request):
  """
    POST to this endpoint to create a new product. The new product, with associated id, will be returned. 
  """
  if request.method=="POST":
    product = Product.objects.create(owner=Owner.objects.get(id=request.user.id))
    product.save()
    return JsonResponse(model_to_dict(product))
  elif request.method=="GET":
    products = Product.objects.filter(owner=request.user.id)
    return_value = []
    for product in products:
      return_value.append({"id":product.id})
    return JsonResponse(return_value, safe=False)


@api_view(['POST','GET'])
@authentication_classes((TokenAuthentication,))
@csrf_exempt
def new_activity(request, user_id, product_id):
  if request.method=="POST":
    score = request.POST["score"]
    activity = Activity.objects.create(user_id=user_id, product_id=product_id, score=score, owner=Owner.objects.get(id=request.user.id))
    activity.save()
    return HttpResponse(activity)

def get_activity(request):
  if request.method=="GET":
    activities = Activity.objects.filter(owner=request.user.id)
    return_value = []
    for activity in activities:
      return_value.append({"id":activity.id,"user_id":activity.user_id, "product_id":activity.product_id, "score":activity.score})
    return JsonResponse(return_value, safe=False)


@authentication_classes((TokenAuthentication,))
@api_view(['GET'])
@csrf_exempt
def rec(request, user_id):
  user = User.objects.get(id=user_id) 
  owner_id = user.owner_id
  #svd.apps.svd_instance.commit_user_recs(user_id, owner_id)
  base =  Rec.objects.filter(user_id=user_id, owner=request.user.id)
  repeats = request.GET.get("repeats")
  count = request.GET.get("count",20)
  if repeats:
    recs = base.distinct().order_by("score").select_related('product')[:count] 
  else:
    recs = base.exclude(product_id__in = Activity.objects.filter(user_id=user.id, owner=Owner.objects.get(id=request.user.id)).values_list("product_id", flat=True)).distinct().order_by("score").select_related('product')[:count] 
  return JsonResponse({"recs":[model_to_dict(rec) for rec in recs]})
