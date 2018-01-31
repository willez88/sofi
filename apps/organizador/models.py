# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext as _
from tools.constantes import PORCENTAJE
from evento.models import Evento
from suscriptor.models import UserProfile

class Organizador(models.Model):
    organizador = models.ForeignKey(UserProfile, verbose_name=_('organizador'))
    evento = models.ForeignKey(Evento, verbose_name=_('evento'))
    
    def __unicode__(self):
        return "%s %s" % (self.organizador.nombre.title(), self.organizador.apellido.title())

    class Meta:
        verbose_name = _(u'Organizador')
        verbose_name_plural = _(u'Organizadores')


class Tarea(models.Model):
    descripcion = models.TextField(max_length=500, verbose_name=_(u'descripción'))
    porcentaje = models.IntegerField(choices=PORCENTAJE, verbose_name=_('%'))
    organizador = models.ForeignKey(Organizador, verbose_name=_('organizador'))
    
    def __unicode__(self):
        return "%s" % (self.descripcion)

    class Meta:
        verbose_name = _(u'Tarea')
        verbose_name_plural = _(u'Tareas')
