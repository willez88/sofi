from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('',
    url(r'^mis_tareas/$', direct_to_template, {'template': 'organizador/tareas.html'}),
    url(r'^actualizar_tarea/(\d+)/$', 'organizador.views.actualizar_tarea'),
)
