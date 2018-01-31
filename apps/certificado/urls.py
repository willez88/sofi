#!/usr/bin/env python

from django.conf.urls.defaults import *
#from django.views.generic.simple import direct_to_template

urlpatterns = patterns('',
    # Esta urls da problemas cuando se activa
    url(r'^descargar/(\d+)/(.+)/$', 'certificado.views.descargar', name="descargar"),
    url(r'^obtenerCertificados/$', 'certificado.views.obtenerCertificados', name="obtenerCertificados"),
)
