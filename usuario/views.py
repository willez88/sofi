"""
Nombre del software: Sofi

Descripción: Sistema de gestión de eventos

Nombre del licenciante y año: Fundación CENDITEL (2018)

Autores: William Páez

La Fundación Centro Nacional de Desarrollo e Investigación en Tecnologías Libres (CENDITEL),
ente adscrito al Ministerio del Poder Popular para Educación Universitaria, Ciencia y Tecnología
(MPPEUCT), concede permiso para usar, copiar, modificar y distribuir libremente y sin fines
comerciales el "Software - Registro de bienes de CENDITEL", sin garantía
alguna, preservando el reconocimiento moral de los autores y manteniendo los mismos principios
para las obras derivadas, de conformidad con los términos y condiciones de la licencia de
software de la Fundación CENDITEL.

El software es una creación intelectual necesaria para el desarrollo económico y social
de la nación, por tanto, esta licencia tiene la pretensión de preservar la libertad de
este conocimiento para que contribuya a la consolidación de la soberanía nacional.

Cada vez que copie y distribuya el "Software - Registro de bienes de CENDITEL"
debe acompañarlo de una copia de la licencia. Para más información sobre los términos y condiciones
de la licencia visite la siguiente dirección electrónica:
http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/
"""
## @namespace usuario.views
#
# Contiene las clases, atributos, métodos y/o funciones a implementar para las vistas del módulo usuario
# @author William Páez (wpaez at cenditel.gob.ve)
# @author <a href='http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/'>Licencia de Software CENDITEL versión 1.2</a>
# @date 14-01-2018
# @version 2.0

from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView
from .forms import PerfilForm, PerfilUpdateForm
from django.contrib.auth.models import User
from .models import Perfil
from base.models import Parroquia, Ubicacion

class PerfilCreateView(CreateView):
    """!
    Clase que permite a cualquier persona registrarse en el sistema

    @author William Páez (wpaez at cenditel.gob.ve)
    @copyright <a href='http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/'>Licencia de Software CENDITEL versión 1.2</a>
    @date 25-05-2018
    """

    model = User
    form_class = PerfilForm
    template_name = 'usuario/perfil.registrar.html'
    success_url = reverse_lazy('usuario:login')

    def form_valid(self, form):
        """!
        Metodo que valida si el formulario es correcto

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/'>Licencia de Software CENDITEL versión 1.2</a>
        @date 25-05-2018
        @param self <b>{object}</b> Objeto que instancia la clase
        @param form <b>{object}</b> Objeto que contiene el formulario de registro
        @return Retorna el formulario validado
        """

        self.object = form.save(commit=False)
        self.object.username = form.cleaned_data['username']
        self.object.first_name = form.cleaned_data['first_name']
        self.object.last_name = form.cleaned_data['last_name']
        self.object.email = form.cleaned_data['email']
        self.object.set_password(form.cleaned_data['password'])
        self.object.is_active = True
        self.object.save()

        #parroquia = Parroquia.objects.get(pk=form.cleaned_data['parroquia'])

        ubicacion = Ubicacion.objects.create(
            direccion = form.cleaned_data['direccion'],
            parroquia = form.cleaned_data['parroquia']
        )

        perfil = Perfil.objects.create(
            telefono=form.cleaned_data['telefono'],
            profesion=form.cleaned_data['profesion'],
            organizacion=form.cleaned_data['organizacion'],
            cuenta_facebook=form.cleaned_data['cuenta_facebook'],
            cuenta_twitter=form.cleaned_data['cuenta_twitter'],
            nivel = 2,
            ubicacion = ubicacion,
            user= self.object
        )

        return super(PerfilCreateView, self).form_valid(form)

class PerfilUpdateView(UpdateView):
    """!
    Clase que permite a un usuario actualizar sus datos de perfil

    @author William Páez (wpaez at cenditel.gob.ve)
    @copyright <a href='http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/'>Licencia de Software CENDITEL versión 1.2</a>
    @date 25-05-2018
    """

    model = User
    form_class = PerfilUpdateForm
    template_name = 'usuario/perfil.registrar.html'
    success_url = reverse_lazy('base:inicio')

    def dispatch(self, request, *args, **kwargs):
        """!
        Metodo que valida si el usuario del sistema tiene permisos para entrar a esta vista

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/'>Licencia de Software CENDITEL versión 1.2</a>
        @date 25-05-2018
        @param self <b>{object}</b> Objeto que instancia la clase
        @param request <b>{object}</b> Objeto que contiene la petición
        @param *args <b>{tupla}</b> Tupla de valores, inicialmente vacia
        @param **kwargs <b>{dict}</b> Diccionario de datos, inicialmente vacio
        @return Redirecciona al usuario a la página de error de permisos si no es su perfil
        """

        if self.request.user.id == self.kwargs['pk']:
            return super(PerfilUpdateView, self).dispatch(request, *args, **kwargs)
        else:
            return redirect('base:error_403')

    def get_initial(self):
        """!
        Metodo que agrega valores predeterminados a los campos del formulario

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/'>Licencia de Software CENDITEL versión 1.2</a>
        @date 25-05-2018
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Retorna un diccionario con los valores predeterminados
        """

        datos_iniciales = super(PerfilUpdateView, self).get_initial()
        #perfil = Perfil.objects.get(user=self.object)
        datos_iniciales['telefono'] = self.object.perfil.telefono
        datos_iniciales['profesion'] = self.object.perfil.profesion
        datos_iniciales['organizacion'] = self.object.perfil.organizacion
        datos_iniciales['cuenta_facebook'] = self.object.perfil.cuenta_facebook
        datos_iniciales['cuenta_twitter'] = self.object.perfil.cuenta_twitter
        datos_iniciales['estado'] = self.object.perfil.ubicacion.parroquia.municipio.estado
        datos_iniciales['municipio'] = self.object.perfil.ubicacion.parroquia.municipio
        datos_iniciales['parroquia'] = self.object.perfil.ubicacion.parroquia
        datos_iniciales['direccion'] = self.object.perfil.ubicacion.direccion
        return datos_iniciales

    def form_valid(self, form):
        """!
        Metodo que valida si el formulario es correcto

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/'>Licencia de Software CENDITEL versión 1.2</a>
        @date 25-05-2018
        @param self <b>{object}</b> Objeto que instancia la clase
        @param form <b>{object}</b> Objeto que contiene el formulario de registro
        @return Retorna el formulario validado
        """

        self.object = form.save(commit=False)
        self.object.username = form.cleaned_data['username']
        self.object.first_name = form.cleaned_data['first_name']
        self.object.last_name = form.cleaned_data['last_name']
        self.object.email = form.cleaned_data['email']
        self.object.save()

        if Perfil.objects.filter(user=self.object):
            perfil = Perfil.objects.get(user=self.object)
            perfil.telefono = form.cleaned_data['telefono']
            perfil.profesion = form.cleaned_data['profesion']
            perfil.organizacion = form.cleaned_data['organizacion']
            perfil.cuenta_facebook = form.cleaned_data['cuenta_facebook']
            perfil.cuenta_twitter = form.cleaned_data['cuenta_twitter']
            perfil.save()
            ubicacion = Ubicacion.objects.get(pk=perfil.ubicacion.id)
            ubicacion.direccion = form.cleaned_data['direccion']
            ubicacion.parroquia = form.cleaned_data['parroquia']
            ubicacion.save()

        return super(PerfilUpdateView, self).form_valid(form)

class PerfilDetailView(DetailView):
    """!
    Clase que permite a un usuario ver el perfil completo de otros usuarios

    @author William Páez (wpaez at cenditel.gob.ve)
    @copyright <a href='http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/'>Licencia de Software CENDITEL versión 1.2</a>
    @date 11-06-2018
    """

    model = User
    template_name = 'usuario/perfil.detalle.html'
