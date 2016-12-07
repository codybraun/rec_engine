from __future__ import unicode_literals
import uuid

from django.contrib.auth.models import User
from django.db import models

class User(models.Model):
  id = models.BigIntegerField(unique=True, primary_key=True)

class Product(models.Model):
  id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
  
class Activity(models.Model):
  id =  models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
  user = models.ForeignKey(User)
  product = models.ForeignKey(Product)
  score = models.FloatField()

class Rec(models.Model):
  product = models.ForeignKey(Product)
  user = models.ForeignKey(User)
  score = models.FloatField()
  unique_together = (('product_id','user_id'),)

