"""
Nombre del software: Sofi

Descripción: Sistema de gestión de eventos

Nombre del licenciante y año: Fundación CENDITEL (2018)

Autores: William Páez

La Fundación Centro Nacional de Desarrollo e Investigación en Tecnologías Libres (CENDITEL),
ente adscrito al Ministerio del Poder Popular para Educación Universitaria, Ciencia y Tecnología
(MPPEUCT), concede permiso para usar, copiar, modificar y distribuir libremente y sin fines
comerciales el "Software - Registro de bienes de CENDITEL", sin garantía
alguna, preservando el reconocimiento moral de los autores y manteniendo los mismos principios
para las obras derivadas, de conformidad con los términos y condiciones de la licencia de
software de la Fundación CENDITEL.

El software es una creación intelectual necesaria para el desarrollo económico y social
de la nación, por tanto, esta licencia tiene la pretensión de preservar la libertad de
este conocimiento para que contribuya a la consolidación de la soberanía nacional.

Cada vez que copie y distribuya el "Software - Registro de bienes de CENDITEL"
debe acompañarlo de una copia de la licencia. Para más información sobre los términos y condiciones
de la licencia visite la siguiente dirección electrónica:
http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/
"""
## @namespace event.models
#
# Contiene las clases, atributos y métodos para el modelo de datos de eventos
# @author William Páez (wpaez at cenditel.gob.ve)
# @author <a href='http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/'>Licencia de Software CENDITEL versión 1.2</a>
# @date 30-05-2018
# @version 2.0

from django.db import models
from django.contrib.auth.models import User
from base.constant import YESNO
from base.models import Location
from django.utils.translation import ugettext_lazy as _

class Event(models.Model):
    """!
    Clase que contiene los datos de un evento

    @author Alexander Olivares (olivaresa at cantv.net)
    @author William Páez (wpaez at cenditel.gob.ve)
    @copyright <a href='http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/'>Licencia de Software CENDITEL versión 1.2</a>
    @date 30-05-2018
    """

    ## Nombre del evento
    name = models.CharField('nombre', max_length=150)

    ## Breve descripción del evento
    summary = models.TextField('resumen', blank=True)

    ## Correo del evento
    email = models.EmailField('correo', unique=True)

    ## Logo del evento
    logo = models.ImageField('logo', upload_to='event/')

    ## Video sobre el tema del evento
    video = models.URLField('vídeo', blank=True)

    ## Cuenta Twitter del evento
    twitter_account = models.CharField('cuenta de twitter', max_length=50, blank=True)

    ## Clave de la cuenta del twitter
    #password_twitter = models.CharField(max_length=12, blank=True)

    ## Cuenta Facebook del evento
    facebook_account = models.CharField('cuenta de facebook', max_length=50, blank=True)

    ## clave de la cuenta del Facebook
    #password_facebook = models.CharField(max_length=12, blank=True)

    ## Permitir mostrar las presentaciones
    presentation = models.BooleanField('presentación', choices=YESNO)

    ## Permitir que los usuarios se suscriban al evento
    subscription = models.BooleanField('suscripción', choices=YESNO)

    ## Permitir que el evento sea visible para todos los usuario
    publication = models.BooleanField('publicación', choices=YESNO)

    ## Permitir a los usuarios dejar comentarios sobre el evento
    commentary = models.BooleanField('comentario', choices=YESNO)

    ## Fecha del evento
    date = models.DateField('fecha')

    ## Fecha inicial del evento
    start_date = models.DateField('fecha inicial')

    ## Fecha final del evento
    end_date = models.DateField('fecha final')

    ## Establece la relación entre la ubicación geográfica y el evento
    location = models.OneToOneField(Location, on_delete=models.CASCADE, verbose_name='ubicación')

    ## Establece la relación entre usuario del sistema con el evento
    user= models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='usuario')

    def __str__(self):
        """!
        Método para representar la clase de forma amigable

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/'>Licencia de Software CENDITEL versión 1.2</a>
        @date 30-05-2018
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Una cadena de caracteres con el nombre del evento
        """

        return self.name

    class Meta:
        """!
        Meta clase del modelo que establece algunas propiedades

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/'>Licencia de Software CENDITEL versión 1.2</a>
        @date 02-08-2018
        """

        verbose_name = _('Evento')
        verbose_name_plural = _('Eventos')

class Certificate(models.Model):
    """!
    Clase que contiene los datos de un certificado que se genera para algún usuario cuando es otorgado

    @author Alexander Olivares (olivaresa at cantv.net)
    @author William Páez (wpaez at cenditel.gob.ve)
    @copyright <a href='http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/'>Licencia de Software CENDITEL versión 1.2</a>
    @date 09-06-2018
    """

    ## Imagen delantera del certificado
    front_image = models.ImageField('imagen delantera', upload_to='certificate/')

    ## Imagen tracera del certificado
    back_image = models.ImageField('imagen tracera', upload_to='certificate/')

    #encuesta = models.BooleanField(choices=SINO)

    ## Coordenada en el eje Y del nombre del suscriptor
    coordinate_y_name = models.IntegerField('coordenada y del nombre')

    ## Temática del evento
    thematic = models.TextField('temática')

    ## Establece la relación del certificado con el evento
    event = models.OneToOneField(Event, on_delete=models.CASCADE, verbose_name='evento')

    def __str__(self):
        """!
        Método para representar la clase de forma amigable

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/'>Licencia de Software CENDITEL versión 1.2</a>
        @date 09-06-2018
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Una cadena de caracteres con el id del certificado y el nombre del evento
        """

        return str(self.id) + ' | ' + str(self.event)

    class Meta:
        """!
        Meta clase del modelo que establece algunas propiedades

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/'>Licencia de Software CENDITEL versión 1.2</a>
        @date 02-08-2018
        """

        verbose_name = _('Certificado')
        verbose_name_plural = _('Certificados')