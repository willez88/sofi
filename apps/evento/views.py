from evento.models import Evento
from django.shortcuts import render_to_response
from django.contrib.sites.models import Site
#Libreria que nos va a permitir realizar la paginacion
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.template import RequestContext
from django.conf import settings
import datetime

def listEventos(request, pagina=1, template_name='evento/evento.html'):
    
    #Obtenemos los objetos de la clase Evento y los paginamos de EVENTOS_PAG por pagina
    paginador = Paginator(Evento.objects.all(), settings.EVENTOS_PAG)
    #Esta variable almacena el rango de las paginas encontradas
    rango_paginas = paginador.page_range

    eventos = paginador.page(pagina)
    
    fecha_hoy = datetime.datetime.date(datetime.datetime.now())
    
    #Enviamos la variable evento que contiene los eventos de la pagina seleccionada
    template = render_to_response(template_name, {'eventos': eventos,'rango_paginas':rango_paginas, 'site_name': Site.objects.get(id=1).name, 'fecha_hoy': fecha_hoy}, context_instance=RequestContext(request))
    return template
