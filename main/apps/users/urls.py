from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^create', views.create),
    url(r'^login', views.login),
    url(r'^logout', views.logout),
    url(r'^users/(?P<book_id>\d+)$', views.users),
]
