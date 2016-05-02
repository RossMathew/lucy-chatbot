from rest_framework import views
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from rest_framework import filters, generics
from django.http import JsonResponse
from django.views.decorators.cache import never_cache
from .models import Answer, Question
from .serializers import AnswerSerializer, QuestionSerializer
import django_filters, logging
from random import randint

logger = logging.getLogger(__name__)

class QuestionFilter(django_filters.FilterSet):

    text_has = django_filters.CharFilter(name="text", lookup_type='icontains')
    text_is = django_filters.CharFilter(name="text", lookup_type='exact')
    class Meta:
        model = Question
        fields  = [ 'text_is', 'text_has']


class AnswerViewSet(ModelViewSet):
    lookup_field = 'id'
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [AllowAny,]


class QuestionViewSet(ModelViewSet):
    lookup_field = 'id'
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [AllowAny,]
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = QuestionFilter



"""
two states of responses - aware and notware
"""
not_found_error_messages = [
    "Hold on !! I barely understood what it mean!",
    "I don't know what you are talking about!",
    "What! I really can't understand",
    "My master never taught me what this mean!",
    "Jesus! teach me what he means!",
    "Oh My! I need oxford dictionary to understand this"
]

# not_understood_question_messages = [
#     "What"
# ]
class QuestionViewList(generics.GenericAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = QuestionFilter
    permission_classes = [AllowAny,]

    @never_cache
    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        # so now take the first one and reply pick one random response and send it to user
        logger.debug(queryset)
        if queryset.count() >= 1:
            # Now take the first entry - assuming thats most relevant
            answers = queryset[0].answers
            logger.debug(answers.count())
            answers_count = answers.count()
            if answers.count() >=1:
                answers_list = [answer.text for answer in answers.all()]
                logger.debug(answers_list)
                if answers_count == 1:
                    answer = answers_list[0]
                else:
                    randnum = randint(0,answers_count-1)
                    logger.debug(randnum)
                    answer = answers_list[randnum]

                return JsonResponse({'mesg': "I've nothing to say about this :( ", 'answer': answer, 'aware': True}, status=200)

            else:
                # no answer found, so generating a randome error message
                answer = not_found_error_messages[randint(0, len(not_found_error_messages)-1)]
                return JsonResponse({'mesg': "I've nothing to say about this :( ", 'answer': answer, 'aware': False}, status=200)
            # no answer found, so generating a randome error message
            answer = not_found_error_messages[randint(0, len(not_found_error_messages)-1)]
            return JsonResponse({'mesg': "Got some reply for you", 'answer': answer, 'aware': False}, status=200)
        else:
            # no question found so generating a randome error message
            answer = not_found_error_messages[randint(0, len(not_found_error_messages)-1)]
            return JsonResponse({'mesg': "I've nothing to say about this :( ", 'answer': answer, 'aware': False}, status=200)
