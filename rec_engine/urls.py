from django.conf.urls import include, url
from django.contrib import admin
from rec_app import views
from rest_framework.authtoken import views as rfviews

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('rec_app.urls')),
    url(r'^', include('user_app.urls')),
    url(r'token', rfviews.obtain_auth_token),
]
