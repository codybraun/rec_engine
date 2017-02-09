import psycopg2
import os 
import numpy as np

pw = os.getenv("PSQLPW")
psql_host = os.getenv("PSQLHOST")
conn = psycopg2.connect("host=" + psql_host +" dbname=game_recs user=jcbraun password="+pw)

c = conn.cursor()
c.execute('SELECT user_id FROM recs_user')
users = []
for row in c.fetchall():
  users.append(row[0])
c.execute('SELECT game_id FROM recs_game')
games = []
for row in c.fetchall():
  games.append(row[0])
c.execute('SELECT play_time, game_id, player_id FROM recs_activity')
matrix = [[0] * len(users) for game in games]
#print matrix
#print users 
#print games
for row in c.fetchall():
  matrix[games.index(row[1])][users.index(row[2])] = row[0]
print np.linalg.svd(matrix)
