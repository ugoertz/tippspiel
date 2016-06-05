from django.shortcuts import render_to_response
from django.core.mail import send_mail
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Template, Context, RequestContext
from django.conf import settings


def login_required_msg(test_func, message, redirect='/'):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if not test_func(request.user):
                messages.error(request, message)
                return HttpResponseRedirect(redirect)
            else:
                return view_func(request, *args, **kwargs)
        return wrapper
    return decorator




def rtr(request, template, **kwargs):
    return render_to_response(template+'.html', kwargs, context_instance=RequestContext(request))


