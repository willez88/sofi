# -*- coding: utf-8 -*-
from django.db import models
from evento.models import Evento
from django.utils.translation import ugettext as _
from tools.constantes import SINO, DIAS_ANTI

class Notificaciones(models.Model):
    evento = models.ForeignKey(Evento, verbose_name=_(u'evento'), unique=True)
    dias = models.IntegerField(choices=DIAS_ANTI, verbose_name=_(u'Días de anticipación'))
    organizadores = models.BooleanField(choices=SINO, verbose_name=_(u'Notificar a Organizadores'))
    ponentes = models.BooleanField(choices=SINO, verbose_name=_(u'Notificar a Ponentes'))
    suscriptores = models.BooleanField(choices=SINO, verbose_name=_(u'Notificar a Suscriptores'))
    
    
    def __unicode__(self):
        return unicode(self.evento)
    
    class Meta:
        verbose_name = _(u'Notificación')
        verbose_name_plural = _(u'Notificaciones')

class EventosNotificados(models.Model):
    notificacion = models.ForeignKey(Notificaciones)
    fecha = models.DateTimeField()
