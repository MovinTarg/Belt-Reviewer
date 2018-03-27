from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^add', views.add),
    url(r'^create', views.create),
    url(r'^(?P<book_id>\d+)$', views.books),
    url(r'^(?P<book_id>\d+)/review$', views.review),
    url(r'^(?P<book_id>\d+)/delete/(?P<review_id>\d+)$', views.delete),
]
