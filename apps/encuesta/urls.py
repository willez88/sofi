#!/usr/bin/env python
from django.conf.urls.defaults import *


urlpatterns = patterns('',
    url(r'^(\d+)/(.+)/$', 'encuesta.views.realizar', name="encuesta"),
    url(r'^reporte/(\d+)/$', 'encuesta.views.reporte', name="reporte encuesta"),
)

