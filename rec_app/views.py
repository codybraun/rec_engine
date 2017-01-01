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
#from svd import SingularValueDecomposition
import svd

#svd = svd.SingularValueDecomposition() 
print svd.views 

@csrf_exempt
def user(request):
  if request.method=="POST":
    user = User.objects.create()
    user.save()
    return JsonResponse(model_to_dict(user))
  else:
    return HttpResponse("Invalid")

@csrf_exempt
def product(request):
  if request.method=="POST":
    product = Product.objects.create()
    product.save()
    return JsonResponse(model_to_dict(product))
  else:
    return HttpResponse("Invalid")

@csrf_exempt
def activity(request, user_id, product_id):
  if request.method=="POST":
    score = request.POST["score"]
    activity = Activity.objects.create(user_id=user_id, product_id=product_id, score=score)
    activity.save()
    return HttpResponse(activity)
  else:
    return HttpResponse("Invalid")

def rec(request, user_id):
  user = User.objects.get(id=user_id) 
  game_recs =  Rec.objects.filter(user_id=user_id).exclude(product_id__in = Activity.objects.filter(user_id=user.id).values_list("product_id", flat=True)).distinct().order_by("score").select_related('product')[:20] 
  print {"recs":[model_to_dict(game) for game in game_recs]}
  return JsonResponse({"recs":[model_to_dict(game) for game in game_recs]})
    
