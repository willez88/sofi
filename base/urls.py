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
## @namespace base.urls
#
# Contiene las rutas de la página de inicio y otras que son de use general en el sistema
# @author William Páez (wpaez at cenditel.gob.ve)
# @author <a href='http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/'>Licencia de Software CENDITEL versión 1.2</a>
# @date 14-01-2018
# @version 2.0

from django.urls import path, re_path
from .views import HomeView, Error403View
from django.contrib.auth.decorators import login_required
from .ajax import ComboUpdateView

app_name = 'base'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('error-403/', Error403View.as_view(), name = "error_403"),

    re_path(r'^ajax/combo-update/?$', ComboUpdateView.as_view(), name='combo_update'),
]

## URLs de peticiones AJAX
#urlpatterns += [
    #path('ajax/actualizar-combo/<int:opcion>/<slug:app>/<slug:mod>/<slug:campo>/<slug:n_value>/<slug:n_text>/', ActualizarComboView.as_view(), name='actualizar_combo'),
#]
