from django.contrib import admin

from .models import Location


class LocationAdmin(admin.ModelAdmin):
    """!
    Clase que agrega modelo Ubicación en el panel administrativo

    @author William Páez <paez.william8@gmail.com>
    @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>
        GNU Public License versión 2 (GPLv2)</a>
    """

    # Mostrar los campos
    list_display = ('address', 'parish')

    # Ordenar por campos
    ordering = ('parish',)


admin.site.register(Location, LocationAdmin)
