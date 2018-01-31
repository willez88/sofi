# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponse, Http404, HttpResponseRedirect
from encuesta.forms import EncuestaForm
from certificado.models import CertificadoSuscriptor
from encuesta.models import Encuesta ,Votacion, Items
from datetime import datetime
from django.template import RequestContext
from django.db import transaction
from django.contrib.auth.decorators import login_required

@login_required
def realizar(request, evento, key):
    
    try:
        suscriptor = CertificadoSuscriptor.objects.get(key=key)
    except Exception, error:
        suscriptor = None

    
    if suscriptor:
        evento_suscriptor = suscriptor.certificado.evento
    
    
        
        if str(evento_suscriptor.id) == evento and suscriptor.certificado.encuesta:
            
            encuesta = Encuesta.objects.get(evento=evento_suscriptor)

            votacion = Votacion.objects.filter(key=suscriptor, item__encuesta__evento=evento_suscriptor)

            if votacion:
                return HttpResponseRedirect('http://%s/certificado/descargar/%s/%s/'% (request.get_host(),evento, key))
            else:
                
                if not request.POST:
                    form = EncuestaForm(evento=evento_suscriptor)
                    return render_to_response('encuesta/encuesta.html', {'evento': evento_suscriptor, 'form': form, 'descripcion': encuesta.descripcion, 'key': key}, context_instance=RequestContext(request))
                else:
                    form = EncuestaForm(evento=evento_suscriptor, data=request.POST)
                    if form.is_valid():
                        
                        
                        transaction.commit_manually()
                        try:
                            for i in form.fields.keys():
                                
                                item = Items.objects.get(id=i)
                                key = CertificadoSuscriptor.objects.get(key=request.POST['key'])
                                votacion = Votacion.objects.create(item=item, respuesta=int(form.cleaned_data[i]), fecha = datetime.date(datetime.now()), key=key)
                        except:
                            transaction.rollback()
                        else:
                            transaction.commit()
                            return HttpResponseRedirect('http://%s/certificado/descargar/%s/%s/'% (request.get_host(),evento, key.key))
                        
        
    raise Http404()

def reporte(request, evento):
    import tools.graph_encuesta
    from evento.models import Evento
    
    if Evento.objects.filter(id=evento) and Encuesta.objects.filter(evento=evento):
        evento = Evento.objects.get(id=evento)
        encuesta = Encuesta.objects.get(evento=evento)
        items_encuesta = encuesta.items_set.all()
        
        total_items = items_encuesta.count()

        
        mucho = []
        suficiente = []
        poco = []
        nada = []

        
        for i in encuesta.items_set.all():
            enc = i.votacion_set.distinct().count()
            
            m = i.votacion_set.filter(respuesta=1).count() * 100 / enc
            s = i.votacion_set.filter(respuesta=2).count() * 100 / enc
            p = i.votacion_set.filter(respuesta=3).count() * 100 / enc
            n = i.votacion_set.filter(respuesta=4).count() * 100 / enc
            
            mucho.append(m)
                
            suficiente.append(s)
                
            poco.append(p)
                
            nada.append(n)
            
            
        list_items = ["%s" % i for i in range(1,total_items+1)]
        
        url = tools.graph_encuesta.generar_encuesta(evento.id, evento.nombre, list_items, mucho, suficiente, poco, nada)
        
        #items = ""
        #
        #for i in items_encuesta:
        #    items += i.nombre + "\n\n"
        
        return render_to_response('encuesta/reporte.html', {'evento': evento, 'items': items_encuesta, 'grafico': url, 'descripcion': encuesta.descripcion}, context_instance=RequestContext(request))
    else:
        raise Http404
