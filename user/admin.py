from django.contrib import admin

from .models import Profile, Subscriber


class ProfileAdmin(admin.ModelAdmin):
    """!
    Clase que agrega modelo Perfil del usuario en el panel administrativo

    @author William Páez <wpaez@cenditel.gob.ve>
    @copyright <a href='https://tinyurl.com/y3tfnema'>
        Licencia de Software CENDITEL versión 1.2</a>
    """

    # Mostrar los campos
    list_display = ('user', 'phone',)

    # Filtrar por campos
    list_filter = ('user',)

    # Mostrar 25 registros por página
    # list_per_page = 25

    # Ordenar por campos
    ordering = ('user',)

    # Buscar por campos
    # search_fields = ('telefono', 'user',)


class SubscriberAdmin(admin.ModelAdmin):
    """!
    Clase que agrega modelo Suscriptor en el panel administrativo

    @author William Páez <wpaez@cenditel.gob.ve>
    @copyright <a href='https://tinyurl.com/y3tfnema'>
        Licencia de Software CENDITEL versión 1.2</a>
    """

    # Mostrar los campos
    list_display = ('profile', 'event',)

    # Filtrar por campos
    # list_filter = ('user', 'telefono',)

    # Mostrar 25 registros por página
    # list_per_page = 25

    # Ordenar por campos
    ordering = ('profile',)

    # Buscar por campos
    # search_fields = ('telefono', 'user',)


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Subscriber, SubscriberAdmin)
