from django.conf.urls import url

from . import views
import psycopg2
import os 
import numpy as np
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

pw = os.getenv("SQLPW")
#pw = os.environ.get('SQLPW', False)
conn = psycopg2.connect("host=localhost dbname=game_recs user=jcbraun password="+pw)

c = conn.cursor()
c.execute('SELECT id FROM ')
users = []
for row in c.fetchall():
  users.append(row[0])
c.execute('SELECT game_id, name FROM recs_game')
games = []
named_games = []
for row in c.fetchall():
  games.append(row[0])
  named_games.append(row[1])
c.execute('SELECT play_time, game_id, player_id FROM recs_activity')
matrix = [[0] * len(users) for game in games]
for row in c.fetchall():
  matrix[games.index(row[1])][users.index(row[2])] = row[0]
u,s,v=np.linalg.svd(matrix, full_matrices=True) 

urlpatterns = [
   url(r'user/(?P<user_id>[^/]+)/product/(?P<product_id>[^/]+)/activity$', views.activity),
   url(r'user/(?P<user_id>[^/]+)/rec$', views.rec),
   url(r'user$', views.user),
   url(r'product$', views.product)
 ]

