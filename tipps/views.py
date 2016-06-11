import datetime

from django.utils.translation import ugettext as _
from django.db.models import Sum, Count
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt

from .models import Userdata, Spiel, Tipp, Runde
from misc.tools import rtr

color_dict = { Tipp.NULL: 'EEEEEE', Tipp.TENDENZ: 'CCFFCC', Tipp.TORDIFFERENZ: '99FF99', Tipp.ERGEBNIS: '55FF55' }

@login_required # FIXME msg
def liste(request):
    t = datetime.datetime.now() + datetime.timedelta(hours=1)
    spiele = list(Spiel.objects.filter(runde__freigabe__gt=0).filter(datum__gte=t).order_by('datum', 'mannschaft1'))
    spiele_alt = list(Spiel.objects.filter(runde__freigabe__gt=0).filter(datum__lt=t).order_by('-datum', 'mannschaft1'))
    if request.POST:
        for s in spiele:
            tipps = Tipp.objects.filter(user=request.user.id).filter(spiel=s.id)
            if tipps:
                s.tt1, s.tt2 = tipps[0].tore1, tipps[0].tore2
                s.tc = '99FF99'
            else:
                s.tc = 'EEEEEE'
            if not s.tippbar(): continue
            try:
                t1, t2 = request.POST['s'+str(s.id)+'t1'], request.POST['s'+str(s.id)+'t2']
                assert t1 != '' or t2 != ''
            except:
                continue
            try:
                t1 = int(t1)
                assert t1 >= 0
                t2 = int(t2)
                assert t2 >= 0
            except:
                s.tc = 'FF9999'
                continue
            s.tt1, s.tt2 = t1, t2
            s.tc = '99FF99'
            if tipps:
                if tipps[0].tore1 != t1 or tipps[0].tore2 != t2:
                    tipp = tipps[0]
                    tipp.tore1, tipp.tore2 = t1, t2
                    tipp.save()
            else:
                tipp = Tipp(spiel=s, user=request.user, tore1=t1, tore2=t2, punkte=0)
                tipp.save()
    else:
        for s in spiele:
            s.tc = 'EEEEEE'
            tipps = Tipp.objects.filter(user=request.user.id).filter(spiel=s.id)
            if tipps:
                s.tt1 = tipps[0].tore1
                s.tt2 = tipps[0].tore2
                s.tc = '99FF99'
    for s in spiele_alt:
        s.tc = 'CCCCCC'
        tipps = Tipp.objects.filter(user=request.user.id).filter(spiel=s.id)
        if tipps:
            s.tt1 = tipps[0].tore1
            s.tt2 = tipps[0].tore2
            s.tc = color_dict[tipps[0].punkte]
    return rtr(request, 'liste', spiele=spiele, spiele_alt=spiele_alt, current_time=str(datetime.datetime.now()))

@login_required
def andere(request, sortby=None):
    return stats(request, sortby, 10)


@login_required
def anderek(request, sortby=None):
    return stats(request, sortby)


@login_required
def stats(request, sortby=None, limit=None):
    ud = Userdata.objects.get(user=request.user)
    t = datetime.datetime.now() + datetime.timedelta(hours=1)
    sp = Spiel.objects.filter(runde__freigabe__exact=2).filter(datum__lt=t).order_by('-datum')
    if limit is None:
        spiele = sp
    else:
        spiele = sp[:limit]
    slist = []
    for s in spiele:
        if s.tippbar(): continue
        slist.append(s)
    if sortby == 'byteam':
        ulist = list(Userdata.objects.filter(team=ud.team).order_by('platz'))
        ulist.extend(list(Userdata.objects.exclude(team=ud.team).order_by('team', 'platz')))
    else:
        if ud.friends.count() > 1: # always a friend to oneself
            ulist = list(ud.friends.all().order_by('platz'))
            ulist.extend(list(Userdata.objects.exclude(id__in=ud.friends.all()).order_by('platz')))
        else:
            ulist = list(Userdata.objects.all().order_by('platz'))
    punkte = -1
    for u in ulist:
        if u.punkte != punkte:
            u.punkte_verschieden = 1
        punkte = u.punkte
        u.li = []
        for s in slist:
            tipps = Tipp.objects.filter(user=u.user, spiel=s.id)
            if tipps:
                t = tipps[0]
                u.li.append((str(t.tore1)+':'+str(t.tore2), color_dict[t.punkte]))
            else:
                u.li.append(('-', 'CCCCCC'))
    return rtr(request, 'andere', slist=slist, ud=ud, users=ulist, limit=limit,
                                  zeige_plaetze=(ud.platz != 0 and sortby!='byteam'))


@login_required
@csrf_exempt
def toggle_friend(request, id):
    ud = Userdata.objects.get(user=request.user)
    fr = Userdata.objects.get(id=id)
    if ud != fr:
        if fr in ud.friends.all():
            ud.friends.remove(fr)
        else:
            ud.friends.add(fr)
    return HttpResponse({}, content_type="application/json")


@login_required
def stat_teams(request):
    teams = []
    for team, teamname in settings.TEAM_CHOICES:
        num_players = Userdata.objects.filter(team=team).count()
        if num_players:
            sum_pts = Userdata.objects.filter(team=team).aggregate(Sum('punkte'))['punkte__sum']
            avg = sum_pts*1.0/num_players if num_players else 0
            teams.append(( avg, teamname, num_players, sum_pts, '%.2f' % avg))
    teams.sort()
    teams.reverse()
    return rtr(request, 'stat_teams', teams=teams)
