#!/usr/bin/env python
from configuracion.models import Enlaces
from django.contrib import admin

class EnlacesAdmin(admin.ModelAdmin):
    list_display = ('descripcion', 'url', 'ubicacion')
    
admin.site.register(Enlaces, EnlacesAdmin)

