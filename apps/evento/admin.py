from evento.models import Evento
from django.contrib import admin
from datetime import datetime


class EventoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'fecha_ini', 'fecha_fin', 'presentaciones', 'suscripciones','publicar']
    search_fields = ['nombre', 'fecha_ini']
    exclude = ('fecha', 'admin')

    def save_model(self, request, obj, form, change):
        obj.fecha = datetime.now()
        obj.admin = request.user
        obj.save()    
    
    def queryset(self, request):
        qs = super(EventoAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(admin=request.user)        
                
admin.site.register(Evento, EventoAdmin)

