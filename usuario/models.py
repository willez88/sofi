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
## @namespace usuario.models
#
# Contiene las clases, atributos y métodos para el modelo de datos de usuario
# @author William Páez (wpaez at cenditel.gob.ve)
# @author <a href='http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/'>Licencia de Software CENDITEL versión 1.2</a>
# @date 14-01-2018
# @version 2.0

from django.db import models
from django.contrib.auth.models import User
from evento.models import Evento
from base.constant import NIVEL, SINO
from django.utils.translation import ugettext_lazy as _

class Perfil(models.Model):
    """!
    Clase que contiene los datos del perfil de un usuario del sistema

    @author Alexander Olivares (olivaresa at cantv.net)
    @author William Páez (wpaez at cenditel.gob.ve)
    @copyright <a href='http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/'>Licencia de Software CENDITEL versión 1.2</a>
    @date 14-01-2018
    """

    ## Teléfono del usuario
    telefono = models.CharField(max_length=15)

    ## Profesión del usuario
    profesion = models.CharField(max_length=100)

    ## Organización al que el usuario pertenece
    organizacion = models.CharField(max_length=100)

    ## Cuenta facebook del usuario
    cuenta_facebook = models.CharField(max_length=100)

    ## Cuenta twitter del usuario
    cuenta_twitter = models.CharField(max_length=100)

    ## Nivel del usuario
    nivel = models.IntegerField(choices=NIVEL)

    ## Establece la relación del usuario del sistema con el perfil
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        """!
        Método para representar la clase de forma amigable

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/'>Licencia de Software CENDITEL versión 1.2</a>
        @date 14-01-2018
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Devuelve una cadena de caracteres con el nombre y apellido del usuario
        """

        return "%s %s" % (self.user.first_name, self.user.last_name)

    class Meta:
        """!
        Meta clase del modelo que establece algunas propiedades

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/'>Licencia de Software CENDITEL versión 1.2</a>
        @date 14-01-2018
        @version 1.0.0
        """

        verbose_name = _("Perfil")
        verbose_name_plural = _("Perfiles")

class Suscriptor(models.Model):
    """!
    Clase que relaciona a los suscriptores con los eventos

    @author Alexander Olivares (olivaresa at cantv.net)
    @author William Páez (wpaez at cenditel.gob.ve)
    @copyright <a href='http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/'>Licencia de Software CENDITEL versión 1.2</a>
    @date 14-01-2018
    """

    otorgar = models.BooleanField(choices=SINO)

    ## Establece la relación entre el suscriptor y el evento
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)

    ## Establece la relación entre el suscriptor y el usuario del sistema
    perfil = models.ForeignKey(Perfil, on_delete=models.CASCADE)

    def __str__(self):
        """!
        Método para representar la clase de forma amigable

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/'>Licencia de Software CENDITEL versión 1.2</a>
        @date 14-01-2018
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Devuelve una cadena de caracteres con el nombre del evento y el nombre de usuario
        """

        return "%s, %s" % (self.evento.nombre, self.perfil.user.username)
