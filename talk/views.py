__author__ = 'rrmerugu'

from django.shortcuts import render_to_response, get_object_or_404, render
from django.template import RequestContext

from django.views.decorators.cache import never_cache


@never_cache
def talk(request):
    return render_to_response('talk.html',  context_instance=RequestContext(request))
