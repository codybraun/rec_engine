from __future__ import unicode_literals
import uuid

from django.contrib.auth.models import User as Owner
from django.db import models

class User(models.Model):
  owner = models.ForeignKey(Owner)

class Product(models.Model):
  owner = models.ForeignKey(Owner)

class Activity(models.Model):
  user = models.ForeignKey(User)
  product = models.ForeignKey(Product)
  score = models.FloatField()
  owner = models.ForeignKey(Owner)

class Rec(models.Model):
  product = models.ForeignKey(Product)
  user = models.ForeignKey(User)
  score = models.FloatField()
  owner = models.ForeignKey(Owner)

  class Meta:
    unique_together = ('product','user')

