from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, HttpResponseRedirect

from misc.tools import rtr
from .models import Flatpage


def flatpage(request, url='/', template=None):
    try:
        f = Flatpage.objects.language().fallbacks().get(url=url)
    except ObjectDoesNotExist:
        # check all languages and redirect if url exists for another language
        for l, _ in settings.LANGUAGES:
            try:
                f = Flatpage.objects.language(l).get(url=url)
                print 'redirect', request.LANGUAGE_CODE, f.url
                return HttpResponseRedirect('/%s/' % Flatpage.objects.language().get(id=f.id))
            except ObjectDoesNotExist:
                pass

        # url does not exist at all
        raise Http404

    template = template or 'flatpages/default'

    return rtr(request, template, flatpage=f)

