from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
from evento.models import Evento
from django.template import RequestContext


def comentario(request, evento):
    if Evento.objects.filter(id=evento):
        evento = Evento.objects.get(id=evento)
        return render_to_response('comentario/comentario.html', {'objeto': evento, 'evento': evento}, context_instance=RequestContext(request))
    else:
        raise Http404
    
