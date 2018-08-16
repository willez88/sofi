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
## @namespace user.views
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
from django.views.generic import CreateView, UpdateView, DetailView, FormView
from .forms import ProfileForm, ProfileUpdateForm, LoginForm
from django.contrib.auth.models import User
from .models import Profile
from base.models import Parish, Location
from django.contrib.auth import authenticate, login

class LoginView(FormView):
    """!
    Clase que gestiona la vista principal del logeo de usuario

    @author William Páez (wpaez at cenditel.gob.ve)
    @copyright <a href='http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/'>Licencia de Software CENDITEL versión 1.2</a>
    @date 22-06-2018
    """
    form_class = LoginForm
    template_name = 'user/login.html'
    success_url = reverse_lazy('base:home')

    def form_valid(self, form):
        """!
        Función que valida si el formulario es correcto

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/'>Licencia de Software CENDITEL versión 1.2</a>
        @date 22-06-2018
        @param self <b>{object}</b> Objeto que instancia la clase
        @param form <b>{object}</b> Objeto que contiene el formulario de registro
        @return Formulario validado
        """

        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return super(LoginView, self).form_valid(form)

class ProfileCreateView(CreateView):
    """!
    Clase que permite a cualquier persona registrarse en el sistema

    @author William Páez (wpaez at cenditel.gob.ve)
    @copyright <a href='http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/'>Licencia de Software CENDITEL versión 1.2</a>
    @date 25-05-2018
    """

    model = User
    form_class = ProfileForm
    template_name = 'user/profile.create.html'
    success_url = reverse_lazy('user:login')

    def form_valid(self, form):
        """!
        Función que valida si el formulario es correcto

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/'>Licencia de Software CENDITEL versión 1.2</a>
        @date 25-05-2018
        @param self <b>{object}</b> Objeto que instancia la clase
        @param form <b>{object}</b> Objeto que contiene el formulario de registro
        @return Formulario validado
        """

        self.object = form.save(commit=False)
        self.object.username = form.cleaned_data['username']
        self.object.first_name = form.cleaned_data['first_name']
        self.object.last_name = form.cleaned_data['last_name']
        self.object.email = form.cleaned_data['email']
        self.object.set_password(form.cleaned_data['password'])
        self.object.is_active = True
        self.object.save()

        location = Location.objects.create(
            address = form.cleaned_data['address'],
            parish = form.cleaned_data['parish']
        )

        profile = Profile.objects.create(
            phone=form.cleaned_data['phone'],
            profession=form.cleaned_data['profession'],
            organization=form.cleaned_data['organization'],
            twitter_account=form.cleaned_data['twitter_account'],
            facebook_account=form.cleaned_data['facebook_account'],
            level = 2,
            location = location,
            user= self.object
        )

        return super(ProfileCreateView, self).form_valid(form)

class ProfileUpdateView(UpdateView):
    """!
    Clase que permite a un usuario actualizar sus datos de perfil

    @author William Páez (wpaez at cenditel.gob.ve)
    @copyright <a href='http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/'>Licencia de Software CENDITEL versión 1.2</a>
    @date 25-05-2018
    """

    model = User
    form_class = ProfileUpdateForm
    template_name = 'user/profile.create.html'
    success_url = reverse_lazy('base:home')

    def dispatch(self, request, *args, **kwargs):
        """!
        Función que valida si el usuario del sistema tiene permisos para entrar a esta vista

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
            return super(ProfileUpdateView, self).dispatch(request, *args, **kwargs)
        else:
            return redirect('base:error_403')

    def get_initial(self):
        """!
        Función que agrega valores predeterminados a los campos del formulario

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/'>Licencia de Software CENDITEL versión 1.2</a>
        @date 25-05-2018
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Diccionario con los valores predeterminados
        """

        initial_data = super(ProfileUpdateView, self).get_initial()
        initial_data['phone'] = self.object.profile.phone
        initial_data['profession'] = self.object.profile.profession
        initial_data['organization'] = self.object.profile.organization
        initial_data['twitter_account'] = self.object.profile.twitter_account
        initial_data['facebook_account'] = self.object.profile.facebook_account
        initial_data['state'] = self.object.profile.location.parish.municipality.state
        initial_data['municipality'] = self.object.profile.location.parish.municipality
        initial_data['parish'] = self.object.profile.location.parish
        initial_data['address'] = self.object.profile.location.address
        return initial_data

    def form_valid(self, form):
        """!
        Función que valida si el formulario es correcto

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/'>Licencia de Software CENDITEL versión 1.2</a>
        @date 25-05-2018
        @param self <b>{object}</b> Objeto que instancia la clase
        @param form <b>{object}</b> Objeto que contiene el formulario de registro
        @return Formulario validado
        """

        self.object = form.save(commit=False)
        self.object.username = form.cleaned_data['username']
        self.object.first_name = form.cleaned_data['first_name']
        self.object.last_name = form.cleaned_data['last_name']
        self.object.email = form.cleaned_data['email']
        self.object.save()

        if Profile.objects.filter(user=self.object):
            profile = Profile.objects.get(user=self.object)
            profile.phone = form.cleaned_data['phone']
            profile.profesion = form.cleaned_data['profession']
            profile.organization = form.cleaned_data['organization']
            profile.twitter_account = form.cleaned_data['twitter_account']
            profile.facebook_account = form.cleaned_data['facebook_account']
            profile.save()
            location = Location.objects.get(pk=profile.location.id)
            location.address = form.cleaned_data['address']
            location.parish = form.cleaned_data['parish']
            location.save()

        return super(ProfileUpdateView, self).form_valid(form)

class ProfileDetailView(DetailView):
    """!
    Clase que permite a un usuario ver el perfil completo de otros usuarios

    @author William Páez (wpaez at cenditel.gob.ve)
    @copyright <a href='http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/'>Licencia de Software CENDITEL versión 1.2</a>
    @date 11-06-2018
    """

    model = User
    template_name = 'user/profile.detail.html'
