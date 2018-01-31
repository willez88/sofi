# -*- coding: utf-8 -*-
from django.contrib import admin
from notificaciones.models import Notificaciones

class NotificacionAdmin(admin.ModelAdmin):
    list_display = ['evento', 'dias', 'organizadores', 'ponentes', 'suscriptores'] 
    list_filter = ['evento']

    #Filtra todos los FK pertenecientes al creador del evento
    def formfield_for_foreignkey(self, db_field, request, **kwargs):

        if not request.user.is_superuser:

            if db_field.name == "evento":
                kwargs["queryset"] = Evento.objects.filter(admin=request.user)

        return super(NotificacionAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    #Filtra la lista de encuestas pertenecientes al creador 
    def queryset(self, request):
        qs = super(NotificacionAdmin, self).queryset(request)
        
        if request.user.is_superuser:
            return qs
        
        return qs.filter(evento__admin=request.user)        

admin.site.register(Notificaciones, NotificacionAdmin)
