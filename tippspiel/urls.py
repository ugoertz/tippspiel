from django.conf.urls import patterns, include, url
from django.contrib import admin

from base import views as base_views
from flatpage import views as flatpage_views
from tipps import views as tipps_views


urlpatterns = (
    url(r'^login/$', base_views.lgin),
    url(r'^logout/$', base_views.lgout),
    url(r'^anmeldung/(?P<team>[a-z]+)/$', base_views.anmeldung),
    url(r'^register/(?P<team>[a-z]+)/$', base_views.anmeldung),
    url(r'^$', tipps_views.liste),
    url(r'^stats/(?P<sortby>[a-z]+)/$', tipps_views.andere),
    url(r'^statskomplett/(?P<sortby>[a-z]+)/$', tipps_views.anderek),
    url(r'^stats/$', tipps_views.andere),
    url(r'^statskomplett/$', tipps_views.anderek),
    url(r'^stat_teams/$', tipps_views.stat_teams),
    url(r'^toggle_friend/(?P<id>\d+)/$', tipps_views.toggle_friend),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^(?P<url>\S+)/$', flatpage_views.flatpage, name='flatpage'),
)
