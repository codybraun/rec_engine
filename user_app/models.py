from __future__ import unicode_literals
import uuid

from django.contrib.auth.models import User
from django.db import models

class Account(models.Model):
  owner = models.ForeignKey(User, default=None, null=True)
