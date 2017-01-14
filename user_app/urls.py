from django.conf.urls import url

from . import views

urlpatterns = [
   # url(r'$', views.login, name='index'),
    url(r'create_user/$', views.new_user),
    url(r'login/$', views.login_user),
    url(r'logout/$', views.logout_user),
    url(r'^$', views.profile),
    url(r'profile/$', views.profile),
    url(r'docs/$', views.docs),
#    url(r'$', views.login_user)
]
