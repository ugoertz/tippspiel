from random import choice
from django.utils.translation import ugettext as _
from django.utils.translation import ugettext_lazy as ugl
from django import forms
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.contrib.sites.models import Site
from django.template import RequestContext
from django.core.mail import send_mail

from tipps.models import Userdata
from tipps.views import liste
from misc.tools import rtr, login_required_msg

# -----------------------------------------------------------------------------

class LoginForm(forms.Form):
    benutzer = forms.CharField()
    passwort = forms.CharField(widget = forms.PasswordInput(attrs = {'tabindex': 2}),
                               required=False)


WELCOME_EMAIL = '''
Liebe(r) {anrede},

danke fuer Deine Anmeldung beim EM-Tippspiel.

Adresse der Webseite: http://{url}/
Hilfe-Seite: http://{url}/hilfe/

Dein Benutzername: {username}
Dein Passwort: {passwd}

Viele Gruesse,

Ulrich



Dear {anrede},

thanks for registering for the betting game.

Web site URL: http://{url}/
Help page: http://{url}/help/

You user name: {username}
Your password: {passwd}

Best,

Ulrich
'''

FORGOT_PASSWORD_EMAIL = '''
Liebe(r) {anrede},

hier ist Dein neues Passwort:

Dein Benutzername: {username}
Dein Passwort: {passwd}

Adresse der Webseite: http://{url}/
Hilfe-Seite: http://{url}/hilfe/

Viele Gruesse,

Ulrich



Dear {anrede},

please find below your new password:

You user name: {username}
Your password: {passwd}

Web site URL: http://{url}/
Help page: http://{url}/help/

Best,

Ulrich
'''

def lgin(request):
    if request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            if 'ForgotPW' in request.POST:
                ps = User.objects.filter(username__exact = form.cleaned_data['benutzer'])
                if not ps:
                    messages.error(request, _('Benutzer unbekannt'))
                    return rtr(request, 'loginform', form=form)
                p = ps[0]
                pw = ''.join([choice('bcdfghjklmnpqrstvwxz') + choice('aeiouy') for i in range(4)])
                p.set_password(pw)
                p.save()
                send_mail('EM-Tippspiel, neues Passwort',
                          FORGOT_PASSWORD_EMAIL.format(
                              anrede=p.first_name,
                              username=form.cleaned_data['benutzer'],
                              passwd=pw,
                              url=Site.objects.get_current().domain),
                          'ug@geometry.de',
                          [ p.email ] )
                messages.info(request, _('Du hast eine Email mit einem neuen Passwort bekommen.'))
                return rtr(request, 'loginform', form=form)
            user = authenticate(username=form.cleaned_data['benutzer'], password=form.cleaned_data['passwort'])
            if (not user is None) and user.is_active:
                login(request, user)
                return HttpResponseRedirect('/') # liste(request)
            else:
                messages.error(request, _('Login fehlgeschlagen.'))
        else:
            messages.info(request, _('Bitte Benutzernamen und Passwort eingeben.'))
    else:
        form = LoginForm()
    return rtr(request, 'loginform', form=form)


def lgout(request):
    logout(request)
    messages.info(request, _('Du bist abgemeldet worden.'))
    return rtr(request, 'loginform', form=LoginForm())

# ---------------------------------------------------------------

class CreateForm(forms.Form):
    benutzername = forms.CharField(max_length = 20, widget = forms.TextInput(attrs = { 'size': 20 }), label = ugl('Benutzername'))
    def clean_benutzername(self):
        try:
            assert User.objects.filter(username=self.cleaned_data['benutzername']).count() == 0
        except AssertionError:
            raise forms.ValidationError(_('Dieser Benutzername ist schon vergeben.'))
        return self.cleaned_data['benutzername']

    vorname = forms.CharField(max_length = 100, widget = forms.TextInput(attrs = { 'size': 50 }), label=ugl('Vorname'))
    nachname = forms.CharField(max_length = 100, widget = forms.TextInput(attrs = { 'size': 50 }), label=ugl('Nachname'))
    email = forms.EmailField(max_length = 100, widget = forms.TextInput(attrs = { 'size': 50 }))


def anmeldung(request, team):
    teams = [x[1].lower() for x in settings.TEAM_CHOICES]
    if not team in teams:
        raise Http404
    team = {x[1].lower(): x[0] for x in settings.TEAM_CHOICES}[team]
    logout(request)
    if request.POST:
        form = CreateForm(request.POST)

        if form.is_valid():
            passwort = ''.join([choice('bcdfghjklmnpqrstvwxz') + choice('aeiouy') for i in range(4)])
            u = User.objects.create_user(form.cleaned_data['benutzername'],
                                         form.cleaned_data['email'],
                                         passwort)
            u.first_name = form.cleaned_data['vorname']
            u.last_name = form.cleaned_data['nachname']
            send_mail('EM-Tippspiel-Anmeldung',
                      WELCOME_EMAIL.format(
                          anrede=u.first_name,
                          username=u.username,
                          passwd=passwort,
                          url=Site.objects.get_current().domain),
                      'ug@geometry.de',
                      [ u.email ] )
            u.save()

            ud = Userdata(user=u, punkte=0)
            ud.team = team
            ud.save()
            ud.friends.add(ud)
            ud.save()
            u = authenticate(username=form.cleaned_data['benutzername'], password=passwort)
            login(request, u)
            messages.info(request, _('Anmeldung erfolgreich.'))
            return HttpResponseRedirect('/')
        else:
            messages.error(request, _('Die Angaben sind nicht vollstaendig.'))
            return rtr(request, 'anmeldung', form=form)
    else:
        return rtr(request, 'anmeldung', form=CreateForm())


