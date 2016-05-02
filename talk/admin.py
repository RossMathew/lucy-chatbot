__author__ = 'rrmerugu'


from django.contrib import admin
from core.models import MyUser
from .models import Answer, Question



class QuestionAdmin(admin.ModelAdmin):
    list_filter = ('date',)
    exclude = ['author', 'date','updated']
    def save_model(self, request, obj, form, change):
        if getattr(obj, 'author', None) is None:
            obj.author = request.user
        obj.save()

class AnswerAdmin(admin.ModelAdmin):
    list_filter = ('date',)
    exclude = ['question','author', 'date','updated']

    ## auto selecting the loggedin user - http://blog.lincoln.hk/blog/2011/10/18/django-admin-auto-select-current-user/

    # saves the current user as author
    def save_model(self, request, obj, form, change):
        if getattr(obj, 'author', None) is None:
            obj.author = request.user
        obj.save()

admin.site.register(Answer, AnswerAdmin)
admin.site.register(Question, QuestionAdmin)