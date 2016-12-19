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
conn = psycopg2.connect("host=localhost dbname=game_recs user=jcbraun password="+pw)
print svdprint svd 
 

class SingularValueDecomposition():

  def __init__(self):
    self.build_affinity_matrix()
    self.build_full_svd()

  def build_full_svd(self):
    u,s,v=np.linalg.svd(matrix, full_matrices=True) 

  def rank_one_svd_update(self, user_id, product_id):
    #m = U'a
    m = np.dot(urls.u.transpose(), a)
    print "M SHAPE " + str(m.shape)
    #pVec = a - Um
    p_vec = np.subtract(a, np.dot(urls.u, m))
    #p = sqrt(p'p)
    p = math.sqrt(np.dot(p_vec.transpose(), p_vec))
    #P = pVec/p
    P = np.divide(p_vec, p)
    #n = V'b
    n = np.dot(urls.v.transpose(), b)
    print "n shape " + str(n.shape)
    #qVec = b - Vn
    q_vec = np.subtract(b, np.dot(urls.v, n))
    #q = sqrt(p'p)
    q = math.sqrt(np.dot(q_vec.transpose(), q_vec))
    #Q = qVec/q
    Q = np.divide(q_vec, q)
    print np.append(m, [p]).shape, np.append(n, [q]).shape
    rhs = np.outer(np.append(m, [p]), np.append(n, [q]))
    x = np.asarray([row for row in matrix])
    y =  np.asarray([0] * (len(matrix[0]) +1))
    print (x.shape, y.shape)
    expanded_matrix = np.asarray(np.concatenate((([(row + [0]) for row in matrix]), np.asarray([[0] * (len(matrix[0])+1)])), axis=0))
    print ("MATRIX SIZES " + str(expanded_matrix.shape) + " " + str(rhs.shape))
    rhs = np.add(expanded_matrix, rhs);
    u,s,v=np.linalg.svd(expanded_matrix, full_matrices=False) 
    return "junk"
  
  def build_affinity_matrix(self):
    c = conn.cursor()
    c.execute('SELECT id FROM recs_player')
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
    self.affinity_matrix = matrix

  def update_affinity_matrix(self, user_id,product_id,score):
    pass
 
  def commit_recs(self):
    rec_matrix = [[0] * len(games) for user in users]
    for i in range(len(users)):
       for j in range(len(games)):
         propensity = np.dot(v[i], u[j])
         conn = psycopg2.connect("host=localhost dbname=game_recs user=jcbraun password="+pw)
         c = conn.cursor()
         c.execute("INSERT INTO recs_rec (player_id, game_id, score) VALUES ('{0}', '{1}', '{2}')".format(users[i], games[j], propensity))
         rec_matrix[i][j]= propensity
         conn.commit()
    self.rec_matrix = rec_matrix


def update_user_game(request, game_id, user_id):
  if request.method=="POST" and request.user.is_authenticated:
    user_vector = np.asarray(generate_user_vector(user_id))
    game_vector = np.asarray(generate_game_vector(game_id))
    rank_one_mod(user_vector, game_vector, urls.matrix)
    return HttpResponse("Done")
  else:
    return HttpResponse("Something broke")

def update_user_stars(request, user_id, game_id):
  if request.method=="POST" and request.user.is_authenticated:
    user_id = request.user.id
    player_id = Player.objects.get(user_id=user_id).id
    rating = request.POST["rating"]
    Activity.objects.create(game_id=game_id, player_id=player_id, play_time=get_scaled_rating(game_id, rating)) 
    user_vector = np.asarray(generate_user_vector(user_id))
    game_vector = np.asarray(generate_game_vector(game_id))
    rank_one_mod(user_vector, game_vector, urls.matrix)
    return HttpResponseRedirect("/recs/recs")
  else:
    return HttpResponseRedirect("/recs/recs")

def get_scaled_rating(game_id, rating):
  #TODO add percentiles
  if (rating==3):
    return Activity.objects.filter(game_id=game_id).aggregate(Avg('play_time'))
  elif (rating==4):
    return Activity.objects.filter(game_id=game_id).aggregate(Avg('play_time'))
  elif (rating==5):
    return Activity.objects.filter(game_id=game_id).aggregate(Avg('play_time'))
  else:
    return 0

def generate_user_vector(user_id):
  vector = []
  player_id = Player.objects.all().filter(user_id=user_id).values()[0]["id"]
  game_list = Game.objects.all().only("game_id").order_by("game_id")
  for game in game_list:
    try:
      vector.append([Rec.objects.all().filter(game_id=game.game_id, player_id=player_id).values()[0]["score"]])
    except Exception:
      vector.append([0])
  return vector 
 
def generate_game_vector(game_id):
  vector = []
  user_list = Player.objects.all().only("id").order_by("id")
  for user in user_list:
    try:
      item =  [Rec.objects.all().filter(player__user_id=user.id, game_id=game_id).values()[0]["score"]]
      if item:
        vector.append(item)
      else:
        vector.append([0])
    except Exception:
      vector.append([0])
  return vector 

