from django.conf.urls import url

from . import views
import psycopg2
import os 
import numpy as np
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

urlpatterns = [
   url(r'^users/(?P<user_id>[^/]+)/product/(?P<product_id>[^/]+)/activity$', views.new_activity),
   url(r'^users/(?P<user_id>[^/]+)/rec/$', views.rec),
   url(r'^users$', views.user),
   url(r'^products$', views.product),
   url(r'^activities$', views.get_activity),
 ]

