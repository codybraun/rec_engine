from __future__ import unicode_literals

from django.apps import AppConfig

from django.conf.urls import url

from . import views
import psycopg2
import os 
import svd
import numpy as np
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

svd_instance = svd.SingularValueDecomposition()
svd_instance.build_affinity_matrix()
svd_instance.build_full_svd()
svd_instance.commit_recs()

class SvdConfig(AppConfig):
    name = 'svd'
