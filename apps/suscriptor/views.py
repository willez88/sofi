# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic.simple import direct_to_template
from django.contrib.sites.models import Site
from evento.models import Evento
from models import Suscriptores, UserProfile
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext as _
from configuracion.models import Site
import os

@login_required
def suscribir(request, id_evento, template='suscriptor/suscriptor.html'):
    evento = Evento.objects.get(id=id_evento)
    
    suscriptor_profile = UserProfile.objects.filter(user=request.user)
    if suscriptor_profile:
        suscriptor_profile = suscriptor_profile.get()
        if suscriptor_profile.nombre and suscriptor_profile.apellido and suscriptor_profile.cedula and suscriptor_profile.nacionalidad:

            if not Suscriptores.objects.filter(suscriptor=suscriptor_profile, evento=evento):
                
                try:
                    suscribir = Suscriptores(suscriptor=suscriptor_profile, evento=evento)
                    suscribir.save()
                    
                    dominio = Site.objects.get_current().domain
                    
                    asunto = _(u'Suscripción a evento')
                    mensaje = _(u'Estimado(a)') + ' ' + suscriptor_profile.nombre_completo() + ' ' + _(u'su suscripción al evento') + ' \\"' + evento.nombre  + '\\" ' + _(u'en') + ' ' + dominio + ', ' + _(u'se ha realizado con éxito.') + '\n\n' + _(u'gracias') + '...'
                    direccion_emisor = evento.email
                    direccion_destino = suscriptor_profile.user.email
                    mail = 'python manage.py sendemail \"%s\" \"%s\" \"%s\" \"%s\"' % (asunto, mensaje, direccion_emisor, direccion_destino)
                    os.system(mail.encode('UTF-8'))
                    ok = 1
                except Exception:
                    ok = 0
                
            else:
                ok = 0

        else:
            return HttpResponseRedirect('/profiles/edit/')
        
    
    
    return render_to_response(template,{'evento': evento, 'site_name': Site.objects.get_current().name, 'ok': ok}, context_instance=RequestContext(request))
  
def reporte(request, id_evento, template='suscriptor/reporte.html'):
    evento = Evento.objects.get(id=id_evento)
    suscriptores = Suscriptores.objects.filter(evento = id_evento)
    return render_to_response(template, {'suscriptores': suscriptores, 'evento': evento, 'site_name': Site.objects.get_current().name}, context_instance=RequestContext(request))
    
