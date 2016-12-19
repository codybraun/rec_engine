from django.conf.urls import url

from . import views
import psycopg2
import os 
import numpy as np
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

urlpatterns = [
   url(r'user/(?P<user_id>[^/]+)/product/(?P<product_id>[^/]+)/activity$', views.activity),
   url(r'user/(?P<user_id>[^/]+)/rec$', views.rec),
   url(r'user$', views.user),
   url(r'product$', views.product)
 ]

