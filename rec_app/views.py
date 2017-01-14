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
import svd 
from rest_framework_swagger.views import get_swagger_view
from rest_framework.decorators import api_view
from rest_framework.decorators import authentication_classes
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth.models import User as Owner
schema_view = get_swagger_view(title=' API')

@api_view(['POST'])
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

@api_view(['POST'])
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

@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@csrf_exempt
def activity(request, user_id, product_id):
  """
    POST to this endpoint to create an activity, reflecting a user's interaction with a product.  
  """
  if request.method=="POST":
    score = request.POST["score"]
    activity = Activity.objects.create(user_id=user_id, product_id=product_id, score=score, owner=Owner.objects.get(id=request.user.id))
    activity.save()
    return HttpResponse(activity)

@authentication_classes((TokenAuthentication,))
@api_view(['POST'])
@csrf_exempt
def rec(request, user_id):
  user = User.objects.get(id=user_id) 
  svd.apps.svd_instance.commit_user_recs(user_id)
  base =  Rec.objects.filter(user_id=user_id, owner=request.user.id)
  repeats = request.GET.get("repeats")
  count = request.GET.get("count",20)
  if repeats:
    recs = base.distinct().order_by("score").select_related('product')[:count] 
  else:
    recs = base.exclude(product_id__in = Activity.objects.filter(user_id=user.id, owner=Owner.objects.get(id=request.user.id)).values_list("product_id", flat=True)).distinct().order_by("score").select_related('product')[:count] 
  return JsonResponse({"recs":[model_to_dict(rec) for rec in recs]})
