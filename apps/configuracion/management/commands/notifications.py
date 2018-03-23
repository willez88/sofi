# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError
from django.utils.translation import ugettext as _
from django.core.mail import send_mail
from notificaciones.models import Notificaciones, EventosNotificados
from organizador.models import Organizador
from suscriptor.models import Suscriptores
from detalle.models import Ponente
from datetime import datetime, timedelta
from evento.models import Evento
from configuracion.models import Site

class Command(BaseCommand):

    def handle(self, *args, **options):
        
        try:

            fecha_hoy = datetime.date(datetime.now())
            #gte mayor o igual
            
            #filtra eventos mayores o iguales a la fecha actual
            eventos = Evento.objects.filter(fecha_fin__gte=fecha_hoy)
            
            for i in eventos:
                notificaciones = i.notificaciones_set.get()
                
                if notificaciones:
                    
                    dias_evento = (i.fecha_fin - fecha_hoy).days
                    
                    # enviar notificación
                    if dias_evento <= notificaciones.dias:
                        
                        asunto = _(u'Notificación de evento')
                        direccion_emisor = i.email
                        direccion_destino = []
                        dominio = Site.objects.get_current().domain
                        
                        if notificaciones.organizadores:
                            
                            for ij in i.organizador_set.all():
                                direccion_destino.append(ij.organizador.user.email)
                            
                            mensaje = _(u'Estimado(a) organizador(a).') + '\n\n' + _(u'Faltan') + ' ' + str(dias_evento) + ' ' + _(u'días para el evento') + ' \"' + i.nombre  + '\" ' + _(u'en') + ' ' + dominio + '\n\n' + _(u'gracias') + '...'
                            send_mail(asunto, mensaje, direccion_emisor, direccion_destino)
                            
                            
                        if notificaciones.ponentes:

                            for ij in i.presentacion_set.all():
                                for ik in ij.ponente_set.all():
                                    direccion_destino.append(ik.suscriptor.user.email)
                            
                            mensaje = _(u'Estimado(a) ponente.') + '\n\n' + _(u'Faltan') + ' ' + str(dias_evento) + ' ' + _(u'días para el evento') + ' \"' + i.nombre  + '\" ' + _(u'en') + ' ' + dominio + '\n\n' + _(u'gracias') + '...'
                            send_mail(asunto, mensaje, direccion_emisor, direccion_destino)


                        if notificaciones.suscriptores:
                        
                            for ij in i.suscriptores_set.all():
                                direccion_destino.append(ij.suscriptor.user.email)
                            
                            mensaje = _(u'Estimado(a) suscriptor(a).') + '\n\n' + _(u'Faltan') + ' ' + str(dias_evento) + ' ' + _(u'días para el evento') + ' \"' + i.nombre  + '\" ' + _(u'en') + ' ' + dominio + '\n\n' + _(u'gracias') + '...'
                            send_mail(asunto, mensaje, direccion_emisor, direccion_destino)

        except Exception, error:
            raise CommandError(_(u'Notificación Error') + ':\n%s' % str(error))
