from __future__ import unicode_literals

from django.apps import AppConfig

from django.conf.urls import url

from . import views
import psycopg2
import os 
import numpy as np
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

pw = os.getenv("SQLPW")
#pw = os.environ.get('SQLPW', False)
conn = psycopg2.connect("host=localhost dbname=recs_engine user=jcbraun password="+pw)

c = conn.cursor()
c.execute('SELECT id FROM rec_app_user')
users = []
for row in c.fetchall():
  users.append(row[0])
c.execute('SELECT id FROM rec_app_product')
games = []
for row in c.fetchall():
  games.append(row[0])
c.execute('SELECT score, product_id, user_id FROM rec_app_activity')
matrix = [[0] * len(users) for game in games]
for row in c.fetchall():
  matrix[games.index(row[1])][users.index(row[2])] = row[0]
try:
  u,s,v=np.linalg.svd(matrix, full_matrices=True) 
except Exception as e:
  print e 
print "HERE "

class SvdConfig(AppConfig):
    name = 'svd'
