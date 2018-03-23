from django.contrib.comments.models import Comment
from django.contrib import admin

class ComentarioAdmin(admin.ModelAdmin):
    fields = ('is_public',)
    list_display = ('user_name', 'user_email', 'comment', 'submit_date', 'instancia_evento', 'is_public')
    list_filter = ('submit_date', 'is_public',)

    #Filtra todos los FK pertenecientes al creador del evento
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
    
        if not request.user.is_superuser:
    
            if db_field.name == "presentacion":
                kwargs["queryset"] = Comment.objects.filter(instancia_evento__admin=request.user)
    
        return super(ComentarioAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    #Filtra la lista de encuestas pertenecientes al creador 
    def queryset(self, request):
        qs = super(ComentarioAdmin, self).queryset(request)
        
        if request.user.is_superuser:
            return qs
        
        return qs.filter(instancia_evento__admin=request.user)



admin.site.unregister(Comment)
admin.site.register(Comment, ComentarioAdmin)
