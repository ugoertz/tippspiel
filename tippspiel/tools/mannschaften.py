#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import datetime
import django

sys.path.append('/var/django/tippspiel')
django.setup()

from tipps.models import Mannschaft, Runde

mannschaften = (
        ('Frankreich', 'fra'),
        ('Spanien', 'esp'),
        ('Deutschland', 'ger'),
        ('England', 'eng'),
        ('Portugal', 'por'),
        ('Belgien', 'bel'),
        ('Italien', 'ita'),
        ('Russland', 'rus'),
        ('Schweiz', 'sui'),
        ('Österreich', 'aut'),
        ('Kroatien', 'cro'),
        ('Ukraine', 'ukr'),
        ('Tschechien', 'cze'),
        ('Schweden', 'swe'),
        ('Polen', 'pol'),
        ('Rumänien', 'rou'),
        ('Slowakei', 'svk'),
        ('Ungarn', 'hun'),
        ('Türkei', 'tur'),
        ('Irland', 'irl'),
        ('Island', 'isl'),
        ('Wales', 'wal'),
        ('Albanien', 'alb'),
        ('Nordirland', 'nir'),

        # ('Niederlande', 'ned'),
        # ('Bosnien und Herzegowina', 'bih'),
        # ('Argentinien', 'arg'),
        # ('Brasilien', 'bra'),
        # ('Chile', 'chi'),
        # ('Ecuador', 'ecu'),
        # ('Kolumbien', 'col'),
        # ('Uruguay', 'uru'),
        # ('Algerien', 'alg'),
        # ('Elfenbeinküste', 'civ'),
        # ('Ghana', 'gha'),
        # ('Kamerun', 'cmr'),
        # ('Nigeria', 'nga'),
        # ('Costa Rica', 'crc'),
        # ('Honduras', 'hon'),
        # ('Mexiko', 'mex'),
        # ('USA', 'usa'),
        # ('Australien', 'aus'),
        # ('Iran', 'irn'),
        # ('Japan', 'jpn'),
        # ('Südkorea', 'kor'),
        # ('Dänemark', 'den'),
        # ('Griechenland', 'gre'),
)

for m, c in mannschaften:
    ma = Mannschaft(name=m.decode('utf8'), code=c)
    ma.save()


for k, s in Runde.NAME_CHOICES:
    ru = Runde(name=k, faktor=1, freigabe=0)
    ru.save()


