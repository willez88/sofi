from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template


urlpatterns = patterns('',
    url(r'^$', 'evento.views.listEventos', name="evento"),
    url(r'^(\d+)/$', 'evento.views.listEventos', name="evento"),
)
