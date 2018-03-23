from detalle.models import Presentacion, Ponente, Evento
from django.shortcuts import render_to_response
from django.contrib.sites.models import Site
from django.template import RequestContext


def listDetalle(request, id, template_name='detalle/detalle.html'):
    evento = Evento.objects.get(id=id)

    template = render_to_response(template_name, {'evento': evento, 'site_name': Site.objects.get(id=1).name}, context_instance=RequestContext(request))
    return template