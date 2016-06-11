# -*- coding: utf-8 -*-

import sys
import datetime
from email.Utils import formatdate

import django
sys.path.append('/var/django/tippspiel')
django.setup()

from django.contrib.sites.models import Site
from django.core.mail import send_mail
from tipps.models import User, Tipp, Spiel, Userdata

__debug = True

EMAIL_TEXT = u"""Liebe(r) {first_name},

uns fehlen noch Deine Tipps zu den folgenden Spielen:

{missing_bets}.

Die Tipps koennen bis eine Stunde vor Spielbeginn unter
{url} eingetragen werden.

Viele Gruesse,

Ulrich



Dear {first_name},

we still miss your bet on the outcome of the following matches:

{missing_bets}.

You can enter your bets until one hour before the match starts at
{url}

Best regards,

Ulrich
"""

def s_string(s):
    return s.datum.strftime('%d.%m., %H h: ') + s.mannschaft1.name + ' - ' + s.mannschaft2.name

errors = []
success = []
no_msg = []
t = datetime.datetime.now()
spiele = Spiel.objects.filter(datum__gte=t+datetime.timedelta(hours=4)).filter(datum__lte=t+datetime.timedelta(hours=36))
users = Userdata.objects.all()

for u in users:
    fehlende_tipps = [ s_string(s) for s in spiele if Tipp.objects.filter(user=u.user, spiel=s.id).count() == 0 ]
    if fehlende_tipps:
        try:
            send_mail(
                    'EM-Tippspiel: Erinnerung / Betting game reminder',
                    EMAIL_TEXT.format(
                        first_name=u.user.first_name,
                        missing_bets=',\n'.join(fehlende_tipps),
                        url=Site.objects.get_current().domain),
                    'ug@geometry.de',
                    [u.user.email],
                    fail_silently=False
                    )
            success.append(u.user.get_full_name() + ' ' + u.user.email)
        except:
            errors.append(u.user.get_full_name() + ' ' + u.user.email)
    else:
        no_msg.append(u.user.get_full_name() + ' ' + u.user.email)

if __debug or errors:
    send_mail(
            'Email reminder',
            'Nomsg bei folgenden Nutzern:\n' + '\n'.join(no_msg) + '\n\n'+\
            'Msg bei folgenden Nutzern:\n' + '\n'.join(success) + '\n\n'+\
            'Probleme bei folgenden Nutzern:\n' + '\n'.join(errors),
            'ug@geometry.de',
            ['ug@geometry.de'],
            )

