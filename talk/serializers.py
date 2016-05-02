__author__ = 'rrmerugu'

from rest_framework import serializers
from .models import Question, Answer



class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ('text','date', 'id')

class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)
    class Meta:
        model = Question
        fields = ('text','date', 'id', 'answers', 'author')
        read_only_fields = ('answers',)


class AnswersOfQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer



