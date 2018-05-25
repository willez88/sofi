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
## @namespace base.models
#
# Contiene las clases, atributos y métodos para el modelo de datos básico
# @author William Páez (wpaez at cenditel.gob.ve)
# @author <a href='http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/'>Licencia de Software CENDITEL versión 1.2</a>
# @date 14-01-2018
# @version 2.0

from django.db import models
from django.contrib.auth.models import User
from .constant import SINO

class Evento(models.Model):
    """!
    Clase que contiene los datos de un evento

    @author William Páez (wpaez at cenditel.gob.ve)
    @copyright <a href='http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/'>Licencia de Software CENDITEL versión 1.2</a>
    @date 14-01-2018
    """

    ## Nombre del evento
    nombre = models.CharField(max_length=150)

    ## Breve descripción del evento
    resumen = models.TextField()

    ## Lugar de realización del evento
    lugar = models.TextField(blank=True)

    ## Correo del evento
    email = models.EmailField()

    ## Cuenta Twitter del evento
    cuenta_twitter = models.CharField(max_length=50, blank=True)

    ## Clave de la cuenta del twitter
    password_twitter = models.CharField(max_length=12, blank=True)

    ## Cuenta Facebook del evento
    centa_facebook = models.CharField(max_length=50, blank=True)

    ## clave de la cuenta del Facebook
    password_facebook = models.CharField(max_length=12, blank=True)

    ##
    presentaciones = models.BooleanField(choices=SINO)

    ## Permitir que los usuarios se suscriban al evento
    suscripciones = models.BooleanField(choices=SINO)

    ## Permitir que el evento sea visible para todos los usuarios
    publicar = models.BooleanField(choices=SINO)

    ## Permitir a los usuarios dejar comentarios sobre el evento
    comentario = models.BooleanField(default=True)

    ## Fecha del evento
    fecha = models.DateField()

    ## Fecha inicial del evento
    fecha_inicial = models.DateField()

    ## Fecha final del evento
    fecha_final = models.DateField()

    ## Logo del evento
    logo = models.ImageField(upload_to='evento')

    ## Video sobre el tema del evento
    media_video = models.URLField(blank=True)

    ## Relación del usuario del sistema con el evento
    user= models.ForeignKey(User, on_delete=models.CASCADE)
