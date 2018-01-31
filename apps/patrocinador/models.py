from django.db import models
from django.utils.translation import ugettext as _
from tools.thumbs import ImageWithThumbsField
from evento.models import Evento

class Patrocinador(models.Model):
    nombre = models.CharField(max_length=200, verbose_name=_(u'nombre'))
    logo = ImageWithThumbsField(upload_to='patrocinador/files', sizes=((100,64),))
    url = models.URLField()
    evento = models.ManyToManyField(Evento, verbose_name=_(u'evento'))
    
    def __unicode__(self):
        return "%s" % (self.nombre)

    class Meta:
        verbose_name = _(u'Patrocinador')
        verbose_name_plural = _(u'Patrocinadores')

