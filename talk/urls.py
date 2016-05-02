__author__ = 'rrmerugu'

from django.conf.urls import url, include
from rest_framework import routers
from . import viewsets, views

router = routers.DefaultRouter()
router.register(r'answer', viewsets.AnswerViewSet)
router.register(r'question', viewsets.QuestionViewSet)


urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^get-answer/$', viewsets.QuestionViewList.as_view(), name='get-answer'),
]
