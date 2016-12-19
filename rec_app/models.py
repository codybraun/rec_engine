from __future__ import unicode_literals
import uuid

from django.contrib.auth.models import User
from django.db import models

class User(models.Model):
  pass

class Product(models.Model):
  pass
 
class Activity(models.Model):
  user = models.ForeignKey(User)
  product = models.ForeignKey(Product)
  score = models.FloatField()

class Rec(models.Model):
  product = models.ForeignKey(Product)
  user = models.ForeignKey(User)
  score = models.FloatField()
  unique_together = (('product_id','user_id'),)

