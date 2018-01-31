from django.contrib import admin
from evento.models import Evento
from patrocinador.models import Patrocinador


class PatrocinadorAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'url', 'logo'] 
    list_filter = ['evento', 'nombre']

    #Filtra todos los FK pertenecientes al creador del evento
    def formfield_for_manytomany(self, db_field, request, **kwargs):

        if not request.user.is_superuser:

            if db_field.name == "evento":
                kwargs["queryset"] = Evento.objects.filter(admin=request.user)

        return super(PatrocinadorAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)

    #Filtra la lista pertenecientes al creador 
    def queryset(self, request):
        qs = super(PatrocinadorAdmin, self).queryset(request)
        
        if request.user.is_superuser:
            return qs
        
        return qs.filter(evento__admin=request.user)        

admin.site.register(Patrocinador, PatrocinadorAdmin)
