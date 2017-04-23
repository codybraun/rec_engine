from django.conf.urls import url

from . import views
import psycopg2
import os 
import numpy as np
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

urlpatterns = [
   url(r'^users/(?P<user_id>[^/]+)/products/(?P<product_id>[^/]+)/activities$', views.activity),
   url(r'^users/(?P<user_id>[^/]+)/recs/$', views.rec),
   url(r'^users$', views.user),
   url(r'^products$', views.product),
   url(r'^activities$', views.all_activity),
 ]

