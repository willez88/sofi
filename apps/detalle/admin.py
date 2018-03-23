from detalle.models import Presentacion, Ponente
from django.contrib import admin

class PonenteAdmin(admin.ModelAdmin):
    list_display = ('suscriptor', 'presentacion', 'evento')
    search_fields = ('suscriptor', 'evento')
    list_filter = ('presentacion__evento',)
    
    #Filtra todos los FK pertenecientes al creador del evento
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
    
        if not request.user.is_superuser:
    
            if db_field.name == "presentacion":
                #kwargs["queryset"] = Evento.objects.filter(admin=request.user)
                kwargs["queryset"] = Presentacion.objects.filter(evento__admin=request.user)
    
        return super(PonenteAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    #Filtra la lista de encuestas pertenecientes al creador 
    def queryset(self, request):
        qs = super(PonenteAdmin, self).queryset(request)
        
        if request.user.is_superuser:
            return qs
        
        return qs.filter(presentacion__evento__admin=request.user)

    
admin.site.register(Ponente, PonenteAdmin)

class PresentacionAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'fecha', 'evento', 'ponente')
    search_fields = ('titulo', 'fecha', 'evento', 'ponente')
    list_filter = ['evento']

    #Filtra todos los FK pertenecientes al creador del evento
    def formfield_for_foreignkey(self, db_field, request, **kwargs):

        if not request.user.is_superuser:

            if db_field.name == "evento":
                kwargs["queryset"] = Evento.objects.filter(admin=request.user)

        return super(PresentacionAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    #Filtra la lista de encuestas pertenecientes al creador 
    def queryset(self, request):
        qs = super(PresentacionAdmin, self).queryset(request)
        
        if request.user.is_superuser:
            return qs
        
        return qs.filter(evento__admin=request.user)        

admin.site.register(Presentacion, PresentacionAdmin)