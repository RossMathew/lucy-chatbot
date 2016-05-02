__author__ = 'rrmerugu'


from django.db import models
from core.models import MyUser
from django.utils import timezone


class Question(models.Model):
    """
    All the questions you can program.
    """
    id = models.AutoField(primary_key=True)
    text = models.CharField(max_length=1000)
    date = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now)
    answers = models.ManyToManyField('Answer', related_name='questions', blank=True)
    author = models.ForeignKey(MyUser)

    def __unicode__(self):
        return self.text



class Answer(models.Model):
    """
    There can be multiple answers for a given question
    This is a one(Q) to many(A) relation,
    """
    id = models.AutoField(primary_key=True)
    text = models.CharField(max_length=1000)
    date = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(MyUser, null=True)
    # question = models.ManyToManyField(Question, related_name='answers')

    def __unicode__(self):
        return self.text
