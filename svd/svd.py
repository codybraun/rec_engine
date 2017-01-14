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

class SingularValueDecomposition():

  def __init__(self):
    self.build_affinity_matrix()
    self.build_full_svd()
    self.matrix = None

  def build_full_svd(self):
    self.u,self.s,self.v=np.linalg.svd(self.affinity_matrix, full_matrices=False) 

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
    x = np.asarray([row for row in self.matrix])
    y =  np.asarray([0] * (len(self.matrix[0]) +1))
    print (x.shape, y.shape)
    expanded_matrix = np.asarray(np.concatenate((([(row + [0]) for row in self.matrix]), np.asarray([[0] * (len(self.matrix[0])+1)])), axis=0))
    print ("MATRIX SIZES " + str(expanded_matrix.shape) + " " + str(rhs.shape))
    rhs = np.add(expanded_matrix, rhs);
    u,s,v=np.linalg.svd(expanded_matrix, full_matrices=False) 
    return "junk"
  
  def build_affinity_matrix(self):
    c.execute('SELECT id FROM rec_app_user')
    users = []
    for row in c.fetchall():
      users.append(row[0])
    c.execute('SELECT id FROM rec_app_product')
    products = []
    for row in c.fetchall():
      products.append(row[0])
    c.execute('SELECT product_id, user_id, score FROM rec_app_activity')
    matrix = [[0] * len(users) for product in products]
    for row in c.fetchall():
      matrix[products.index(row[0])][users.index(row[1])] = row[2]
    self.affinity_matrix = matrix
    self.users = users
    self.products = products

  def update_affinity_matrix(self, user_id,product_id,score):
    pass
 
  def commit_recs(self):
    rec_matrix = [[0] * len(self.products) for user in self.users]
    for i in range(len(self.users)):
       for j in range(len(self.products)):
         propensity = np.vdot(self.v[i], self.u[j].T)
      	 c.execute("INSERT INTO rec_app_rec (user_id, product_id, score) VALUES ('{0}', '{1}', '{2}') ON CONFLICT (user_id, product_id) DO UPDATE SET score='{2}'".format(self.users[i], self.products[j], propensity))
         rec_matrix[i][j]= propensity
         conn.commit()
    self.rec_matrix = rec_matrix

  def commit_user_recs(self, user_id):
    i = self.users.index(int(user_id))
    for j in range(len(self.products)):
      propensity = np.vdot(self.v[i], self.u[j].T)
      c.execute("INSERT INTO rec_app_rec (user_id, product_id, score) VALUES ('{0}', '{1}', '{2}') ON CONFLICT (user_id, product_id) DO UPDATE SET score='{2}'".format(self.users[i], self.products[j], propensity))
      conn.commit()

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

