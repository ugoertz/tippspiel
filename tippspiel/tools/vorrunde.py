#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import datetime
import django

sys.path.append('/var/django/tippspiel')
django.setup()

from tipps.models import Spiel, Mannschaft, Runde

spiele = """
V1 | 2016-06-10, 21:00 | fra | rou
V1 | 2016-06-11, 15:00 | alb | sui
V1 | 2016-06-11, 18:00 | wal | svk
V1 | 2016-06-11, 21:00 | eng | rus
V1 | 2016-06-12, 18:00 | pol | nir
V1 | 2016-06-12, 21:00 | ger | ukr
V1 | 2016-06-12, 15:00 | tur | cro
V1 | 2016-06-13, 15:00 | esp | cze
V1 | 2016-06-13, 18:00 | irl | swe
V1 | 2016-06-13, 21:00 | bel | ita
V1 | 2016-06-14, 18:00 | aut | hun
V1 | 2016-06-14, 21:00 | por | isl

V2 | 2016-06-15, 18:00 | rou | sui
V2 | 2016-06-15, 21:00 | fra | alb
V2 | 2016-06-15, 15:00 | rus | svk
V2 | 2016-06-16, 15:00 | eng | wal
V2 | 2016-06-16, 18:00 | ukr | nir
V2 | 2016-06-16, 21:00 | ger | pol
V2 | 2016-06-17, 18:00 | cze | cro
V2 | 2016-06-17, 21:00 | esp | tur
V2 | 2016-06-17, 15:00 | ita | swe
V2 | 2016-06-18, 15:00 | bel | irl
V2 | 2016-06-18, 18:00 | isl | hun
V2 | 2016-06-18, 21:00 | por | aut

V3 | 2016-06-19, 21:00 | sui | fra
V3 | 2016-06-19, 21:00 | rou | alb
V3 | 2016-06-20, 21:00 | svk | eng
V3 | 2016-06-20, 21:00 | rus | wal
V3 | 2016-06-21, 18:00 | ukr | pol
V3 | 2016-06-21, 18:00 | nir | ger
V3 | 2016-06-21, 21:00 | cro | esp
V3 | 2016-06-21, 21:00 | cze | tur
V3 | 2016-06-22, 21:00 | ita | irl
V3 | 2016-06-22, 21:00 | swe | bel
V3 | 2016-06-22, 18:00 | hun | por
V3 | 2016-06-22, 18:00 | isl | aut
"""

spielliste = [ l for l in spiele.split('\n') if l.strip() ]

for l in spielliste:
    runde, datum, ms1, ms2 = l.split(' | ')
    print datum, ms1, ms2
    m1 = Mannschaft.objects.get(code = ms1)
    m2 = Mannschaft.objects.get(code = ms2)
    r = Runde.objects.get(name = runde)
    d1, d2 = datum.split(',')
    year, month, day = [ int(x) for x in d1.strip().split('-') ]
    hour, minutes = [ int(x) for x in d2.strip().split(':') ]
    d = datetime.datetime(year, month, day, hour, minutes)
    sp = Spiel(mannschaft1=m1, mannschaft2=m2, datum=d, runde=r)
    sp.save()

