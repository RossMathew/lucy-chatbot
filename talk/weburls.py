__author__ = 'rrmerugu'

from django.conf.urls import url, include
from rest_framework import routers
from . import viewsets, views

urlpatterns = [
    url(r'^$', views.talk, name='talk'),
]
