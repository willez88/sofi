# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.sites.models import Site
from django.utils.translation import ugettext as _
from tools.thumbs import ImageWithThumbsField

MB = (
    (True, _(u'Menú')),
    (False, _(u'Barra'))
)

class Enlaces(models.Model):
    descripcion = models.CharField(max_length=30, verbose_name=_(u'descripción'))
    url = models.URLField()
    ubicacion = models.BooleanField(verbose_name=_(u'ubicación'), choices=MB)
    
    def __unicode__(self):
            return unicode("%s" % self.descripcion)

    class Meta:
        verbose_name = _(u'Enlaces')
        verbose_name_plural = _(u'Enlaces')

    
Site.add_to_class('titulo', models.CharField(max_length=20, verbose_name=_(u'título')))
Site.add_to_class('subtitulo', models.CharField(max_length=20, verbose_name=_(u'subtítulo')))
Site.add_to_class('informacion', models.TextField(verbose_name=_(u'información')))
Site.add_to_class('logo', ImageWithThumbsField(upload_to='configuracion/files', sizes=((120,100),), verbose_name=_(u'logo')))
Site.add_to_class('banner', ImageWithThumbsField(upload_to='configuracion/files', sizes=((160,600),), verbose_name=_(u'banner 160x600')))
