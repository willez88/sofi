from django.contrib import admin

from .models import Certificate, Event


class EventAdmin(admin.ModelAdmin):
    """!
    Clase que agrega modelo Evento en el panel administrativo

    @author William Páez <paez.william8@gmail.com>
    @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>
        GNU Public License versión 2 (GPLv2)</a>
    """

    # Mostrar los campos
    list_display = ('user',)

    # Mostrar 25 registros por página
    # list_per_page = 25

    # Ordenar por campos
    ordering = ('user',)


class CertificateAdmin(admin.ModelAdmin):
    """!
    Clase que agrega modelo Certificado en el panel administrativo

    @author William Páez <paez.william8@gmail.com>
    @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>
        GNU Public License versión 2 (GPLv2)</a>
    """

    # Mostrar los campos
    list_display = ('event', 'front_image',)

    # Mostrar 25 registros por página
    # list_per_page = 25

    # Ordenar por campos
    ordering = ('event',)


admin.site.register(Event, EventAdmin)
admin.site.register(Certificate, CertificateAdmin)
