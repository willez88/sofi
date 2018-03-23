# -*- coding: utf-8 -*-

from django.db import models
from evento.models import Evento
from suscriptor.models import Suscriptores as Suscriptor
from hashlib import md5
import random
from tools import email as email_tools
from tools.constantes import SINO
from django.contrib.sites.models import Site
from django.utils.translation import ugettext as _
from datetime import datetime

class Certificado(models.Model):
    imagen_de_fondo_delantera = models.ImageField(upload_to='certificado/files', verbose_name=_(u'Imagen delantera'))
    imagen_de_fondo_tracera = models.ImageField(upload_to='certificado/files', verbose_name=_(u'Imagen tracera'))
    evento = models.ForeignKey(Evento, unique=True, verbose_name=_(u'Evento'))
    encuesta = models.BooleanField(choices=SINO, verbose_name=_(u'Encuesta'))
    posicion_y_nombre = models.IntegerField(verbose_name=_(u'Posición y del nombre'))
    posicion_x_key = models.IntegerField(verbose_name=_(u'Posición x del serial'))
    posicion_y_key = models.IntegerField(verbose_name=_(u'Posición y del serial'))
    tematica = models.TextField(verbose_name=_(u'Temática'))
    
    def save(self, force_insert=False, force_update=False):
        super(Certificado, self).save(force_insert, force_update)
        self.__agregaCertificadoSuscriptor()
        

    def __unicode__(self):
        return "Certificado - %s" % self.evento

    def __agregaCertificadoSuscriptor(self):
        lista_suscritos = Suscriptor.objects.filter(evento=self.evento)
        
        
        for i in lista_suscritos:
            suscriptor = i
            key = md5("%s%s%s%s" % (i.nombre_completo().encode("ascii", "replace"), str(random.randrange(1000, 1000000000)), self.evento.nombre.encode("ascii", "replace"), datetime.now().isoformat())).hexdigest()
            certificado = self
            
            # exception para determinar si ya fue generado el CertificadoSuscriptor
            try:
                CertificadoSuscriptor.objects.get(suscriptor=suscriptor, certificado=certificado)
            except Exception, error:
                certificado_suscriptor = CertificadoSuscriptor(suscriptor=suscriptor, key=key, certificado=certificado, otorgar=False)
                certificado_suscriptor.save()
            
    class Meta:
        verbose_name = _('Configurar')
        verbose_name_plural = _('Configurar')
        
class CertificadoSuscriptor(models.Model):
    suscriptor = models.ForeignKey(Suscriptor, editable=False)
    key = models.CharField(max_length=32, editable=False)
    certificado = models.ForeignKey(Certificado, editable=False)
    otorgar = models.BooleanField(choices=SINO)
    
    def evento(self):
        return self.certificado.evento

    def save(self, force_insert=False, force_update=False):
        if self.otorgar:
            email = self.suscriptor.suscriptor.user.email
            nombre = self.suscriptor.nombre_completo()
            evento = self.suscriptor.evento.nombre
            evento_id =  self.suscriptor.evento.id
            evento_email = self.suscriptor.evento.email
            
            if self.certificado.encuesta:
                url = 'http://%s/encuesta/%s/%s/' % (Site.objects.get(id=1).domain, evento_id, self.key)
            else:
                url = 'http://%s/certificado/descargar/%s/%s/' % (Site.objects.get(id=1).domain, evento_id, self.key)
                
            mensaje = _('Estimado(a)') + ' %s ' % nombre + _('su certificado del evento') + ' %s, ' % evento + _('puede descargarlo en el siguiente enlace:') + '\n%s\n\n' % url + _(u'Gracias por su participación...')
            
            
            try:
                email_tools.enviar_mail(_(u'Certificado de asistencia a evento'), mensaje, evento_email, [email])
            except Exception, error:
                pass

        super(CertificadoSuscriptor, self).save(force_insert, force_update)
        
    
    def __unicode__(self):
        return self.suscriptor.nombre_completo()
        
    class Meta:
        verbose_name = _('Otorgar')
        verbose_name_plural = _('Otorgar')
