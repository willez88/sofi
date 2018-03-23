from suscriptor.models import Suscriptores
from django.contrib import admin
from suscriptor.models import UserProfile

class SuscriptorAdmin(admin.ModelAdmin):
    list_display = ['nombre_completo', 'evento'] #, 'cedula', 'email','evento'
    list_filter = ['evento']

admin.site.register(Suscriptores, SuscriptorAdmin)
admin.site.register(UserProfile)