#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
sys.path.append('/home/ug/django/wm10') # FIXME

import datetime
from em08.tipps.models import Spiel, Mannschaft, Runde

spiele = """
VF | 2008-06-19, 20:45 | por | ger
VF | 2008-06-20, 20:45 | cro | tur
"""


spielliste = [ l for l in spiele.split('\n') if l.strip() ]

for l in spielliste:
    runde, datum, ms1, ms2 = l.split(' | ')
    m1 = Mannschaft.objects.filter(code__exact = ms1)[0]
    m2 = Mannschaft.objects.filter(code__exact = ms2)[0]
    r = Runde.objects.filter(name__exact = runde)[0]
    d1, d2 = datum.split(',')
    year, month, day = [ int(x) for x in d1.strip().split('-') ]
    hour, minutes = [ int(x) for x in d2.strip().split(':') ]
    d = datetime.datetime(year, month, day, hour, minutes)
    sp = Spiel(mannschaft1=m1, mannschaft2=m2, datum=d, runde=r)
    sp.save()

