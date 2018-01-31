#!/usr/bin/env python
from certificado.models import Certificado, CertificadoSuscriptor
from django.contrib import admin
from evento.models import Evento


class CertificadoAdmin(admin.ModelAdmin):
    list_display = ('evento', 'imagen_de_fondo_delantera', 'encuesta',)


    #Filtra todos los FK pertenecientes al creador
    def formfield_for_foreignkey(self, db_field, request, **kwargs):

        if not request.user.is_superuser:

            if db_field.name == "evento":
                kwargs["queryset"] = Evento.objects.filter(admin=request.user)

        return super(CertificadoAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    #Filtra la lista pertenecientes al creador
    def queryset(self, request):
        qs = super(CertificadoAdmin, self).queryset(request)

        if request.user.is_superuser:
            return qs

        return qs.filter(evento__admin=request.user)

admin.site.register(Certificado, CertificadoAdmin)

class CertificadoSuscriptorAdmin(admin.ModelAdmin):
    list_display = ('suscriptor', 'key', 'evento','certificado', 'otorgar',)
    list_filter = ('certificado',)
    search_fields = ('^suscriptor__nombres', '^suscriptor__apellidos')

    #Filtra la lista pertenecientes al creador
    def queryset(self, request):
        qs = super(CertificadoSuscriptorAdmin, self).queryset(request)

        if request.user.is_superuser:
            return qs

        return qs.filter(certificado__evento__admin=request.user)

admin.site.register(CertificadoSuscriptor, CertificadoSuscriptorAdmin)
