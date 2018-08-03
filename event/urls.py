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
## @namespace event.urls
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
    EventListView, EventCreateView, EventUpdateView, EventDeleteView, EventDetailView, SubscribeView,
    SubscribeReportView, CertificateListView, CertificateCreateView, CertificateUpdateView,
    CertificateDeleteView, CertificateView, SubscriberUpdateView, CertificateDownloadView
)

app_name = 'event'

urlpatterns = [
    path('listar/', login_required(EventListView.as_view()), name='list'),
    path('registrar/', login_required(EventCreateView.as_view()), name='create'),
    path('actualizar/<int:pk>/', login_required(EventUpdateView.as_view()), name = 'update'),
    path('eliminar/<int:pk>/', login_required(EventDeleteView.as_view()), name = 'delete'),
    path('detalle/<int:pk>/', EventDetailView.as_view(), name='detail'),

    path('suscribir/<int:pk>/', login_required(SubscribeView.as_view()), name = 'subscribe'),
    path('suscribir/reporte/<int:pk>/', SubscribeReportView.as_view(), name = 'subscribe_report'),

    path('certificado/listar/', login_required(CertificateListView.as_view()), name='certificate_list'),
    path('certificado/registrar', login_required(CertificateCreateView.as_view()), name='certificate_create'),
    path('certificado/actualizar/<int:pk>/', login_required(CertificateUpdateView.as_view()), name = 'certificate_update'),
    path('certificado/eliminar/<int:pk>/', login_required(CertificateDeleteView.as_view()), name = 'certificate_delete'),
    path('certificado/descargar/<int:evento>/', login_required(CertificateDownloadView.as_view()), name = 'certificate_download'),

    path('certificado/<int:pk>/', login_required(CertificateView.as_view()), name = 'certificate'),
    path('certificado/suscriptor/actualizar/<int:pk>/', login_required(SubscriberUpdateView.as_view()), name = 'subscriber_update'),

    re_path(r'^media/(?P<path>.*)$', serve, {
        'document_root': settings.MEDIA_ROOT,
    }),
]
