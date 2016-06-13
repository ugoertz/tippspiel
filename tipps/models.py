import datetime

from django.db import models
from django.contrib.auth.models import User
from django import forms
from django.conf import settings

def sign(i):
    if i > 0: return 1
    elif i < 0: return -1
    return 0


class Userdata(models.Model):
    user = models.OneToOneField(User)
    team = models.CharField(max_length=10, choices=settings.TEAM_CHOICES)
    punkte = models.IntegerField()
    platz = models.IntegerField(default=0)
    friends = models.ManyToManyField('self', blank=True, symmetrical=False)

    def __unicode__(self):
        return self.user.get_full_name()


class Mannschaft(models.Model):
    code = models.CharField(max_length=3)
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'mannschaften'


class Runde(models.Model):
    NAME_CHOICES = (('V1', 'Vorrunde, Spieltag 1'),
                    ('V2', 'Vorrunde, Spieltag 2'),
                    ('V3', 'Vorrunde, Spieltag 3'),
                    ('AF', 'Achtelfinale'),
                    ('VF', 'Viertelfinale'),
                    ('HF', 'Halbfinale'),
                    # ('3P', 'Spiel um 3. Platz'),
                    ('F', 'Finale'))
    name = models.CharField(max_length=2, choices=NAME_CHOICES, unique=True)
    faktor = models.IntegerField(default=1)

    freigabe = models.IntegerField(default=2)

    def __str__(self):
        freigaben = { 0: 'Keine', 1: 'Ansicht', 2: 'Tipp' }
        return self.get_name() + ' (Freigabe: ' + freigaben[self.freigabe] + ')'

    def get_name(self):
        names = dict(Runde.NAME_CHOICES)
        return names[self.name]

    class Meta:
        verbose_name_plural = 'Runden'


class Spiel(models.Model):
    mannschaft1 = models.ForeignKey(Mannschaft, related_name='ms1')
    mannschaft2 = models.ForeignKey(Mannschaft, related_name='ms2')
    tore1 = models.IntegerField(blank=True, null=True)
    tore2 = models.IntegerField(blank=True, null=True)
    datum = models.DateTimeField()
    runde = models.ForeignKey(Runde)

    def __unicode__(self):
        result = self.runde.name + ': ' + self.mannschaft1.name + ' - ' + self.mannschaft2.name
        if self.tore1 != None:
            result += ' (' + str(self.tore1) + ':' + str(self.tore2) +')'
        return result

    def tippbar(self):
        if self.runde.freigabe != 2: return 0
        if self.tore1 != None and self.tore2 != None: return 0
        if self.datum - datetime.datetime.now() >= datetime.timedelta(hours=1): return 1
        return 0

    def save(self):
        models.Model.save(self)

        # tipps updaten
        for t in Tipp.objects.filter(spiel=self.id):
            t.punkte = Tipp.NULL
            if self.tore1 != None and self.tore2 != None:
                if sign(self.tore1 - self.tore2) == sign(t.tore1 - t.tore2): t.punkte = Tipp.TENDENZ
                if self.tore1 - self.tore2 == t.tore1 - t.tore2 and self.tore1 != self.tore2:
                    t.punkte = Tipp.TORDIFFERENZ
                if self.tore1 == t.tore1 and self.tore2 == t.tore2:
                    t.punkte = Tipp.ERGEBNIS
            t.save()

        ulist = Userdata.objects.all()
        for u in ulist:
            u.punkte = 0
            for t in Tipp.objects.filter(user=u.user):
                if t.tore1 != t.tore2:
                    u.punkte += { Tipp.NULL: 0,
                                  Tipp.TENDENZ: 5,
                                  Tipp.TORDIFFERENZ: 7,
                                  Tipp.ERGEBNIS: 9 }[t.punkte] * t.spiel.runde.faktor
                else:
                    u.punkte += { Tipp.NULL: 0,
                                  Tipp.TENDENZ: 5,
                                  Tipp.TORDIFFERENZ: 7,
                                  Tipp.ERGEBNIS: 7 }[t.punkte] * t.spiel.runde.faktor
            u.save()
        ulist = Userdata.objects.all().order_by('-punkte')

        vorheriger_platz, punkte_vorheriger_platz = 0, 1000
        for ctr, u in enumerate(ulist):
            if u.punkte == punkte_vorheriger_platz:
                u.platz = vorheriger_platz
            else:
                u.platz = ctr + 1
                vorheriger_platz, punkte_vorheriger_platz = u.platz, u.punkte
            u.save()


    class Meta:
        verbose_name_plural = 'Spiele'
        unique_together = (('mannschaft1', 'mannschaft2', 'datum'),)



class Tipp(models.Model):
    user = models.ForeignKey(User)
    spiel = models.ForeignKey(Spiel)
    tore1 = models.IntegerField()
    tore2 = models.IntegerField()
    punkte = models.IntegerField()

    NULL = 0
    TENDENZ = 1
    TORDIFFERENZ = 2
    ERGEBNIS = 3

    def __unicode__(self):
        return ' '.join([self.user.username, unicode(self.spiel), unicode(self.tore1), unicode(self.tore2) ])

    class Meta:
        unique_together = (('user', 'spiel'),)


