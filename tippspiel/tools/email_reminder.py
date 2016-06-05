#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import datetime
sys.path.append('/home/ug/devel/tippspiel/tippspiel')
sys.path.append('/home/ug/devel/tippspiel')
sys.path.append('/home/ug/devel')

import smtplib
from email.Utils import formatdate
import django
from settings import DATABASES
from tippspiel.tipps.models import User, Tipp, Spiel, Userdata

__debug = True

EMAIL_HEADER = """Date: %s
From: "EM-Tippspiel" <ug@geometry.de>
To: %s
Subject: %s
Content-Type: TEXT/PLAIN; charset=iso-8859-1
Content-Transfer-Encoding: QUOTED-PRINTABLE

"""

EMAIL_TEXT = u"""Liebe(r) %s,

uns fehlen noch Deine Tipps zu den folgenden Spielen:

%s.

Die Tipps koennen bis eine Stunde vor Spielbeginn unter
http://em12.geometry.de/ eingetragen werden.

Viele Gruesse,

Ulrich



Dear %s,

we still miss your bet on the outcome of the following matches:

%s

You can enter your bets until one hour befor the match starts at
http://em12.geometry.de/

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
user = Userdata.objects.all()
fromaddr = '"EM-Tippspiel" <ug@geometry.de>'
for u in user:
    fehlende_tipps = [ s_string(s) for s in spiele if Tipp.objects.filter(user=u.user, spiel=s.id).count() == 0 ]
    if fehlende_tipps:
        msg = EMAIL_HEADER % (formatdate(), u.user.email, 'EM-Tippspiel: Erinnerung') +\
              (EMAIL_TEXT % (u.user.first_name, ',\n'.join(fehlende_tipps), u.user.first_name, ',\n'.join(fehlende_tipps), ) ).encode('latin1').encode('quotedprintable')
        try:
            toaddrs = [u.user.email]
            server = smtplib.SMTP('localhost')
            server.sendmail(fromaddr, toaddrs, msg)
            server.quit()
            success.append(u.user.get_full_name() + ' ' + u.user.email)
        except:
            errors.append(u.user.get_full_name() + ' ' + u.user.email)
    else:
        no_msg.append(u.user.get_full_name() + ' ' + u.user.email)

if __debug or errors:
    server = smtplib.SMTP('localhost')
    server.sendmail('u@g0ertz.de', ['u@g0ertz.de'], 
                    EMAIL_HEADER % (formatdate(), 'u@g0ertz.de', 'Email-Reminder: Probleme') +\
                    'Nomsg bei folgenden Nutzern:\n' + ('\n'.join(no_msg)).encode('latin1').encode('quotedprintable') + '\n\n'+\
                    'Msg bei folgenden Nutzern:\n' + ('\n'.join(success)).encode('latin1').encode('quotedprintable') + '\n\n'+\
                    'Probleme bei folgenden Nutzern:\n' + ('\n'.join(errors)).encode('latin1').encode('quotedprintable'))
    server.quit()

