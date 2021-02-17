from django.conf import settings
from django.urls import path, re_path
from django.views.static import serve

from .views import (
    CertificateCreateView, CertificateDeleteView, CertificateDownloadView,
    CertificateListView, CertificateUpdateView, CertificateView,
    EventCreateView, EventDeleteView, EventDetailView, EventListView,
    EventUpdateView, SubscribeReportView, SubscriberUpdateView, SubscribeView,
)

app_name = 'event'

urlpatterns = [
    path('listar/', EventListView.as_view(), name='list'),
    path('registrar/', EventCreateView.as_view(), name='create'),
    path('actualizar/<int:pk>/', EventUpdateView.as_view(), name='update'),
    path('eliminar/<int:pk>/', EventDeleteView.as_view(), name='delete'),
    path('detalle/<int:pk>/', EventDetailView.as_view(), name='detail'),

    path('suscribir/<int:pk>/', SubscribeView.as_view(), name='subscribe'),
    path(
        'suscribir/reporte/<int:pk>/', SubscribeReportView.as_view(),
        name='subscribe_report'
    ),

    path(
        'certificado/listar/', CertificateListView.as_view(),
        name='certificate_list'
    ),
    path(
        'certificado/registrar', CertificateCreateView.as_view(),
        name='certificate_create'
    ),
    path(
        'certificado/actualizar/<int:pk>/', CertificateUpdateView.as_view(),
        name='certificate_update'
    ),
    path(
        'certificado/eliminar/<int:pk>/', CertificateDeleteView.as_view(),
        name='certificate_delete'
    ),
    path(
        'certificado/descargar/<int:evento>/',
        CertificateDownloadView.as_view(),
        name='certificate_download'
    ),

    path(
        'certificado/<int:pk>/', CertificateView.as_view(), name='certificate'
    ),
    path(
        'certificado/suscriptor/actualizar/<int:pk>/',
        SubscriberUpdateView.as_view(),
        name='subscriber_update'
    ),

    re_path(r'^media/(?P<path>.*)$', serve, {
        'document_root': settings.MEDIA_ROOT,
    }),
]
