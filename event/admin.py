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
## @namespace event.__init__
#
# Contiene las clases, atributos y métodos básicos del sistema a implementar en el panel administrativo
# @author William Páez (wpaez at cenditel.gob.ve)
# @author <a href='http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/'>Licencia de Software CENDITEL versión 1.2</a>
# @date 30-05-2018
# @version 2.0

from django.contrib import admin
from .models import Event, Certificate

# Register your models here.

class EventAdmin(admin.ModelAdmin):
    """!
    Clase que agrega modelo Evento en el panel administrativo

    @author William Páez (wpaez at cenditel.gob.ve)
    @copyright <a href='http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/'>Licencia de Software CENDITEL versión 1.2</a>
    @date 22-06-2018
    """

    ## Mostrar los campos
    list_display = ('user',)

    ## Mostrar 25 registros por página
    #list_per_page = 25

    ## Ordenar por perfil
    ordering = ('user',)

## Registra el modelo Evento en el panel administrativo
admin.site.register(Event, EventAdmin)

class CertificateAdmin(admin.ModelAdmin):
    """!
    Clase que agrega modelo Certificado en el panel administrativo

    @author William Páez (wpaez at cenditel.gob.ve)
    @copyright <a href='http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/'>Licencia de Software CENDITEL versión 1.2</a>
    @date 22-06-2018
    """

    ## Mostrar los campos
    list_display = ('event','front_image',)

    ## Mostrar 25 registros por página
    #list_per_page = 25

    ## Ordenar por evento
    ordering = ('event',)

## Registra el modelo Evento en el panel administrativo
admin.site.register(Certificate, CertificateAdmin)
