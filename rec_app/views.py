from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader
import requests 
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
    return HttpResponse(str(model_to_dict(user)))
  else:
    return HttpResponse("Invalid")

def product(request):
  if request.method=="POST":
    product = Product.objects.create()
    product.save()
    return HttpResponse(product)
  else:
    return HttpResponse("Invalid")

def activity(user_id, product_id, request):
  if request.method=="POST":
    score = request.POST.score
    activity = Activity.objects.create(user_id=user_id, product_id=product_id, score=score)
    activity.save()
    return HttpResponse(activity)
  else:
    return HttpResponse("Invalid")

def rec(request):
  if request.method=="POST":
    user = User.objects.get(user_id=request.POST.user_id) 
    game_recs =  Rec.objects.filter(player_id=player.id).exclude(game_id__in = Activity.objects.filter(player_id=player.id).values_list("game_id", flat=True)).distinct().order_by("score").select_related('game')[:20] 
    product = Product.objects.create()
    product.save()
    return HttpResponse(product)
  else:
    return HttpResponse("Invalid")

