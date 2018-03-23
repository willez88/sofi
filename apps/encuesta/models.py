# -*- coding: utf-8 -*-
from django.db import models
from evento.models import Evento
#from suscriptor.models import Suscriptor
from suscriptor.models import Suscriptores as Suscriptor
from suscriptor.models import UserProfile
from django.utils.translation import ugettext as _
from certificado.models import CertificadoSuscriptor
from tools.constantes import MSPN

class Encuesta(models.Model):
    descripcion = models.TextField(verbose_name=_(u'descripción'))
    evento = models.ForeignKey(Evento, verbose_name=_(u'evento'))
    
    def __unicode__(self):
        return self.descripcion
    
class Items(models.Model):
    nombre = models.CharField(max_length=200, verbose_name=_(u'nombre'))
    encuesta = models.ForeignKey(Encuesta, verbose_name=_(u'encuesta'))

class Votacion(models.Model):
    fecha = models.DateField(verbose_name=_(u'fecha'))
    respuesta = models.IntegerField(choices=MSPN, verbose_name=_(u'respuesta'))
    item = models.ForeignKey(Items, verbose_name=_(u'item'))
    key = models.ForeignKey(CertificadoSuscriptor, verbose_name=_(u'key'))
    