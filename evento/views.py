from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Evento
from .forms import EventoForm

class EventoListView(ListView):
    """!
    Clase que permite a un usuario listar los eventos que ha creado

    @author William Páez (wpaez at cenditel.gob.ve)
    @copyright <a href='http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/'>Licencia de Software CENDITEL versión 1.2</a>
    @date 30-05-2018
    """

    model = Evento
    template_name = "evento.listar.html"

    def dispatch(self, request, *args, **kwargs):
        """!
        Metodo que valida si el usuario del sistema tiene permisos para entrar a esta vista

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/'>Licencia de Software CENDITEL versión 1.2</a>
        @date 30-05-2018
        @param self <b>{object}</b> Objeto que instancia la clase
        @param request <b>{object}</b> Objeto que contiene la petición
        @param *args <b>{tupla}</b> Tupla de valores, inicialmente vacia
        @param **kwargs <b>{dict}</b> Diccionario de datos, inicialmente vacio
        @return Redirecciona al usuario a la página de error de permisos en caso de no pertenecer a este nivel
        """

        if self.request.user.id == self.kwargs['pk'] and self.request.user.perfil.nivel == 1:
            return super(EventoListView, self).dispatch(request, *args, **kwargs)
        else:
            return redirect('error_403')

class EventoCreateView(CreateView):
    """!
    Clase que permite a un usuario crear eventos

    @author William Páez (wpaez at cenditel.gob.ve)
    @copyright <a href='http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/'>Licencia de Software CENDITEL versión 1.2</a>
    @date 30-05-2018
    """

    model = Evento
    form_class = EventoForm
    template_name = "evento.registrar.html"
    success_url = reverse_lazy('evento_listar')

    def form_valid(self, form):
        """!
        Metodo que valida si el formulario es correcto

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/'>Licencia de Software CENDITEL versión 1.2</a>
        @date 30-05-2018
        @param self <b>{object}</b> Objeto que instancia la clase
        @param form <b>{object}</b> Objeto que contiene el formulario de registro
        @return Retorna el formulario validado
        """

        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()

        return super(EventoCreateView, self).form_valid(form)

class EventoUpdateView(UpdateView):
    """!
    Clase que permite a un usuario registrado en el sistema actualizar los datos de los eventos que ha creado

    @author William Páez (wpaez at cenditel.gob.ve)
    @copyright <a href='http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/'>Licencia de Software CENDITEL versión 1.2</a>
    @date 30-05-2018
    """

    model = Evento
    form_class = EventoForm
    template_name = "evento.registrar.html"
    success_url = reverse_lazy('inicio')

    def dispatch(self, request, *args, **kwargs):
        """!
        Metodo que valida si el usuario del sistema tiene permisos para entrar a esta vista

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/'>Licencia de Software CENDITEL versión 1.2</a>
        @date 30-05-2018
        @param self <b>{object}</b> Objeto que instancia la clase
        @param request <b>{object}</b> Objeto que contiene la petición
        @param *args <b>{tupla}</b> Tupla de valores, inicialmente vacia
        @param **kwargs <b>{dict}</b> Diccionario de datos, inicialmente vacio
        @return Redirecciona al usuario a la página de error de permisos si no es su perfil
        """

        if self.request.user.id == self.kwargs['pk'] and self.request.user.perfil.nivel == 1:
            return super(PerfilUpdateView, self).dispatch(request, *args, **kwargs)
        else:
            return redirect('error_403')

    def get_initial(self):
        """!
        Metodo que agrega valores predeterminados a los campos del formulario

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/'>Licencia de Software CENDITEL versión 1.2</a>
        @date 30-05-2018
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Retorna un diccionario con los valores predeterminados
        """

        datos_iniciales = super(EventoUpdateView, self).get_initial()
        evento = Evento.objects.get(user=self.object)
        datos_iniciales['nombre'] = evento.nombre
        datos_iniciales['resumen'] = evento.resumen
        datos_iniciales['lugar'] = evento.lugar
        datos_iniciales['email'] = evento.email
        datos_iniciales['cuenta_twitter'] = evento.cuenta_twitter
        datos_iniciales['cuenta_facebook'] = evento.cuenta_facebook
        datos_iniciales['presentacion'] = evento.presentacion
        datos_iniciales['suscripcion'] = evento.suscripcion
        datos_iniciales['publicacion'] = evento.publicacion
        datos_iniciales['comentario'] = evento.comentario
        datos_iniciales['fecha'] = evento.fecha
        datos_iniciales['fecha_inicial'] = evento.fecha_inicial
        datos_iniciales['fecha_final'] = evento.fecha_final
        datos_iniciales['logo'] = evento.logo
        return datos_iniciales

    def form_valid(self, form):
        """!
        Metodo que valida si el formulario es correcto

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/'>Licencia de Software CENDITEL versión 1.2</a>
        @date 30-05-2018
        @param self <b>{object}</b> Objeto que instancia la clase
        @param form <b>{object}</b> Objeto que contiene el formulario de registro
        @return Retorna el formulario validado
        """

        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()

        return super(EventoUpdateView, self).form_valid(form)
