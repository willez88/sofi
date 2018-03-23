from django.contrib import admin
from suscriptor.models import UserProfile
from organizador.models import Organizador, Tarea
from evento.models import Evento

class TareaInline(admin.TabularInline):
    model = Tarea

class OrganizadorAdmin(admin.ModelAdmin):
    list_display = ['organizador', 'evento'] #, 'cedula', 'email','evento'
    list_filter = ['evento', 'organizador']

    inlines = [
            TareaInline,
        ]

    #Filtra todos los FK pertenecientes al creador del evento
    def formfield_for_foreignkey(self, db_field, request, **kwargs):

        if not request.user.is_superuser:

            if db_field.name == "evento":
                kwargs["queryset"] = Evento.objects.filter(admin=request.user)

        return super(OrganizadorAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    #Filtra la lista de encuestas pertenecientes al creador 
    def queryset(self, request):
        qs = super(OrganizadorAdmin, self).queryset(request)
        
        if request.user.is_superuser:
            return qs
        
        return qs.filter(evento__admin=request.user)        

admin.site.register(Organizador, OrganizadorAdmin)
