from django.views.generic import TemplateView
from event.models import Event


class HomeView(TemplateView):
    """!
    Clase para mostrar la página de inicio según el nivel de usuario

    @author William Páez <wpaez@cenditel.gob.ve>
    @copyright <a href='https://tinyurl.com/y3tfnema'>
        Licencia de Software CENDITEL versión 1.2</a>
    """

    template_name = 'base/base.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['event'] = Event.objects.all()
        return context


class Error403View(TemplateView):
    """!
    Clase para mostrar error de permiso

    @author William Páez <wpaez@cenditel.gob.ve>
    @copyright <a href='https://tinyurl.com/y3tfnema'>
        Licencia de Software CENDITEL versión 1.2</a>
    """

    template_name = 'base/error_403.html'
