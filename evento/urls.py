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
## @namespace evento.urls
#
# Contiene las rutas de la aplicación evento
# @author William Páez (wpaez at cenditel.gob.ve)
# @author <a href='http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/'>Licencia de Software CENDITEL versión 1.2</a>
# @date 14-01-2018
# @version 2.0

from django.urls import path, re_path
from django.conf import settings
from django.views.static import serve
from django.contrib.auth.decorators import login_required
from .views import (
    EventoListView, EventoCreateView, EventoUpdateView, EventoDeleteView, SuscribirView,
    SuscribirReporteView, CertificadoListView, CertificadoCreateView, CertificadoUpdateView,
    CertificadoDeleteView, CertificadoView, SuscriptorUpdateView, CertificadoDescargarView
)

app_name = 'evento'

urlpatterns = [
    path('listar', login_required(EventoListView.as_view()), name='listar'),
    path('registrar', login_required(EventoCreateView.as_view()), name='registrar'),
    path('actualizar/<int:pk>/', login_required(EventoUpdateView.as_view()), name = "actualizar"),
    path('eliminar/<int:pk>/', login_required(EventoDeleteView.as_view()), name = "eliminar"),

    path('suscribir/<int:pk>/', login_required(SuscribirView.as_view()), name = "suscribir"),
    path('suscribir/reporte/<int:pk>/', login_required(SuscribirReporteView.as_view()), name = "suscribir_reporte"),

    path('certificado/listar', login_required(CertificadoListView.as_view()), name='certificado_listar'),
    path('certificado/registrar', login_required(CertificadoCreateView.as_view()), name='certificado_registrar'),
    path('certificado/actualizar/<int:pk>/', login_required(CertificadoUpdateView.as_view()), name = "certificado_actualizar"),
    path('certificado/eliminar/<int:pk>/', login_required(CertificadoDeleteView.as_view()), name = "certificado_eliminar"),
    path('certificado/descargar/<int:evento>/', login_required(CertificadoDescargarView.as_view()), name = "certificado_descargar"),

    path('certificado/<int:pk>/', login_required(CertificadoView.as_view()), name = "certificado"),
    path('certificado/suscriptor/actualizar/<int:pk>/', login_required(SuscriptorUpdateView.as_view()), name = "suscriptor_actualizar"),

    re_path(r'^media/(?P<path>.*)$', serve, {
        'document_root': settings.MEDIA_ROOT,
    }),
]
