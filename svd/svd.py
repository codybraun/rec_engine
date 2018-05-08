from __future__ import unicode_literals

from django.apps import AppConfig

from django.conf.urls import url

from . import views
import psycopg2
import os 
import numpy as np
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.db import connection
import traceback
import threading 
threads = [] 
connection._rollback()
connection.close()

pw = os.getenv("PSQLPW")
psql_host = os.getenv("PSQLHOST")
conn = psycopg2.connect("host=" + psql_host + " dbname=recs_engine user=jcbraun password="+pw)
c = conn.cursor()

class SingularValueDecomposition():

  def __init__(self):
    self.affinity_matrices = {}
    self.svd_dict = {}
    c.execute('SELECT id FROM rec_app_user')
    for owner in c.fetchall(): 
      self.build_affinity_matrix_for_owner(owner[0])
      self.build_full_svd_for_owner(owner[0])
    self.matrix = None
    t = threading.Thread(target=self.background_commit)
    threads.append(t)
    t.start()

  def build_full_svd_for_owner(self, owner_id):
    try: 
      self.update_owner_svd(owner_id, np.linalg.svd(self.affinity_matrices[owner_id], full_matrices=False))
    except Exception as e:
      print e
      traceback.print_exc()
 
  def update_owner_svd(self, owner_id, usv):
    self.svd_dict[owner_id] = {}
    self.svd_dict[owner_id]["u"] = usv[0]
    self.svd_dict[owner_id]["s"] = usv[1]
    self.svd_dict[owner_id]["v"] = usv[2]

  def rank_one_svd_update(self, user_id, product_id):
    m = np.dot(urls.u.transpose(), a)
    p_vec = np.subtract(a, np.dot(urls.u, m))
    p = math.sqrt(np.dot(p_vec.transpose(), p_vec))
    P = np.divide(p_vec, p)
    n = np.dot(urls.v.transpose(), b)
    q_vec = np.subtract(b, np.dot(urls.v, n))
    q = math.sqrt(np.dot(q_vec.transpose(), q_vec))
    Q = np.divide(q_vec, q)
    rhs = np.outer(np.append(m, [p]), np.append(n, [q]))
    x = np.asarray([row for row in self.matrix])
    y =  np.asarray([0] * (len(self.matrix[0]) +1))
    expanded_matrix = np.asarray(np.concatenate((([(row + [0]) for row in self.matrix]), np.asarray([[0] * (len(self.matrix[0])+1)])), axis=0))
    rhs = np.add(expanded_matrix, rhs);
    u,s,v=np.linalg.svd(expanded_matrix, full_matrices=False)
  
  def build_affinity_matrix_for_owner(self, owner_id):
    c.execute('SELECT id FROM rec_app_user WHERE owner_id = ' + str(owner_id))
    users = []
    for row in c.fetchall():
      users.append(row[0])
    c.execute('SELECT id FROM rec_app_product')
    products = []
    for row in c.fetchall():
      products.append(row[0])
    c.execute('SELECT product_id, user_id, score FROM rec_app_activity WHERE owner_id = ' + str(owner_id))
    matrix = [[0] * len(users) for product in products]
    for row in c.fetchall():
      matrix[products.index(row[0])][users.index(row[1])] = row[2]
    self.affinity_matrices[owner_id] = matrix

  def update_affinity_matrix(self, user_id,product_id,score):
    pass

  def background_commit(self):
    while True:
      c.execute('SELECT id FROM rec_app_user')
      for owner in c.fetchall(): 
        self.commit_recs_for_owner(owner[0])       

  def commit_recs_for_owner(self, owner_id):
    c.execute('SELECT id FROM rec_app_user WHERE owner_id = ' + str(owner_id))
    users = c.fetchall()
    c.execute('SELECT id FROM rec_app_product WHERE owner_id = ' + str(owner_id))
    products = c.fetchall()
    rec_matrix = [[0] * len(products) for user in users]
    for i in range(len(users)):
      for j in range(len(products)):
        propensity = np.vdot(self.svd_dict[owner_id]["v"][i], self.svd_dict[owner_id]["u"][j].T)
      	c.execute("INSERT INTO rec_app_rec (user_id, product_id, score, owner_id) VALUES ('{0}', '{1}', '{2}', '{3}') ON CONFLICT (user_id, product_id) DO UPDATE SET score='{2}'".format(users[i][0], products[j][0], propensity, str(owner_id)))
        rec_matrix[i][j]= propensity
        conn.commit()
    self.rec_matrix = rec_matrix

  def commit_user_recs(self, user_id, owner_id):
    connection._rollback()
    connection.close()
    i = self.users.index(int(user_id))
    for j in range(len(self.products)):
      connection._rollback()
      connection.close()
      propensity = np.vdot(self.v[:,i], self.u[j].T)
      c.execute("INSERT INTO rec_app_rec (user_id, owner_id, product_id, score) VALUES ('{0}', '{1}', '{2}', '{3}') ON CONFLICT (user_id, product_id) DO UPDATE SET score='{2}'".format(user_id, owner_id, self.products[j], propensity))
      conn.commit()
