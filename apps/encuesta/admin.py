#!/usr/bin/env python
# -*- coding: utf-8 -*-

from encuesta.models import Encuesta, Items
from django.contrib import admin
from evento.models import Evento

class ItemsInline(admin.TabularInline):
    model = Items


class EncuestaAdmin(admin.ModelAdmin):
    list_display = ('descripcion', 'evento')
    list_filter = ('evento',)
    #search_fields = ('^suscriptor__nombres', '^suscriptor__apellidos')

    inlines = [
            ItemsInline,
        ]

    #Filtra todos los FK pertenecientes al creador del evento
    def formfield_for_foreignkey(self, db_field, request, **kwargs):

        if not request.user.is_superuser:

            if db_field.name == "evento":
                kwargs["queryset"] = Evento.objects.filter(admin=request.user)

        return super(EncuestaAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    #Filtra la lista de encuestas pertenecientes al creador 
    def queryset(self, request):
        qs = super(EncuestaAdmin, self).queryset(request)
        
        if request.user.is_superuser:
            return qs
        
        return qs.filter(evento__admin=request.user)        

admin.site.register(Encuesta, EncuestaAdmin)


