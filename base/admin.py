from django.contrib import admin

from .models import Location


class LocationAdmin(admin.ModelAdmin):
    """!
    Clase que agrega modelo Ubicación en el panel administrativo

    @author William Páez <wpaez@cenditel.gob.ve>
    @copyright <a href='https://tinyurl.com/y3tfnema'>
        Licencia de Software CENDITEL versión 1.2</a>
    """

    # Mostrar los campos
    list_display = ('address', 'parish')

    # Ordenar por campos
    ordering = ('parish',)


admin.site.register(Location, LocationAdmin)
