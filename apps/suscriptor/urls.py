from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('',
    url(r'^registro/(\d+)/$', 'suscriptor.views.suscribir', name="suscriptor"),
    url(r'^mis_suscripciones/$', direct_to_template, {'template': 'suscriptor/suscripciones.html'}),
    url(r'^reporte/(\d+)/$', 'suscriptor.views.reporte', name="reporte"),
)
