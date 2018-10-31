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
## @namespace event.views
#
# Contiene las clases, atributos, métodos y/o funciones a implementar para las vistas del módulo evento
# @author William Páez (wpaez at cenditel.gob.ve)
# @author <a href='http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/'>Licencia de Software CENDITEL versión 1.2</a>
# @date 30-05-2018
# @version 2.0

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView, DetailView
from django.views import View
from .models import Event, Certificate
from .forms import EventForm, CertificateForm
from user.models import Subscriber, Profile
from user.forms import SubscriberForm
from base.models import Location
from base.constant import LEVEL
from base.functions import send_email
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.fonts import addMapping
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape
from PIL import Image, ImageDraw
from io import BytesIO

class EventListView(ListView):
    """!
    Clase que permite a un usuario listar los eventos que ha registrado

    @author William Páez (wpaez at cenditel.gob.ve)
    @copyright <a href='http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/'>Licencia de Software CENDITEL versión 1.2</a>
    @date 30-05-2018
    """

    model = Event
    template_name = 'event/list.html'

    def dispatch(self, request, *args, **kwargs):
        """!
        Función que valida si el usuario del sistema tiene permisos para entrar a esta vista

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/'>Licencia de Software CENDITEL versión 1.2</a>
        @date 30-05-2018
        @param self <b>{object}</b> Objeto que instancia la clase
        @param request <b>{object}</b> Objeto que contiene la petición
        @param *args <b>{tupla}</b> Tupla de valores, inicialmente vacia
        @param **kwargs <b>{dict}</b> Diccionario de datos, inicialmente vacio
        @return Redirecciona al usuario a la página de error de permisos en caso de no pertenecer a este nivel
        """

        if self.request.user.profile.level == 1:
            return super(EventListView, self).dispatch(request, *args, **kwargs)
        else:
            return redirect('base:error_403')

    def get_queryset(self):
        """!
        Función que obtiene la lista de eventos que están asociados al usuario

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/'>Licencia de Software CENDITEL versión 1.2</a>
        @date 20-06-2018
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Lista de objetos evento que el usuario registró
        """

        queryset = Event.objects.filter(user=self.request.user)
        return queryset

class EventCreateView(CreateView):
    """!
    Clase que permite a un usuario registrar eventos

    @author William Páez (wpaez at cenditel.gob.ve)
    @copyright <a href='http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/'>Licencia de Software CENDITEL versión 1.2</a>
    @date 30-05-2018
    """

    model = Event
    form_class = EventForm
    template_name = 'event/create.html'
    success_url = reverse_lazy('event:list')

    def dispatch(self, request, *args, **kwargs):
        """!
        Función que valida si el usuario del sistema tiene permisos para entrar a esta vista

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/'>Licencia de Software CENDITEL versión 1.2</a>
        @date 08-06-2018
        @param self <b>{object}</b> Objeto que instancia la clase
        @param request <b>{object}</b> Objeto que contiene la petición
        @param *args <b>{tupla}</b> Tupla de valores, inicialmente vacia
        @param **kwargs <b>{dict}</b> Diccionario de datos, inicialmente vacio
        @return Redirecciona al usuario a la página de error de permisos en caso de no pertenecer a este nivel
        """

        if self.request.user.profile.level == 1:
            return super(EventCreateView, self).dispatch(request, *args, **kwargs)
        else:
            return redirect('base:error_403')

    def form_valid(self, form):
        """!
        Función que valida si el formulario es correcto

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/'>Licencia de Software CENDITEL versión 1.2</a>
        @date 30-05-2018
        @param self <b>{object}</b> Objeto que instancia la clase
        @param form <b>{object}</b> Objeto que contiene el formulario de registro
        @return Formulario validado
        """

        location = Location.objects.create(
            address = form.cleaned_data['address'],
            parish = form.cleaned_data['parish']
        )

        self.object = form.save(commit=False)
        self.object.location = location
        self.object.user = self.request.user
        self.object.save()

        return super(EventCreateView, self).form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return super(EventCreateView, self).form_invalid(form)

class EventUpdateView(UpdateView):
    """!
    Clase que permite a un usuario actualizar los datos de los eventos que ha registrado

    @author William Páez (wpaez at cenditel.gob.ve)
    @copyright <a href='http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/'>Licencia de Software CENDITEL versión 1.2</a>
    @date 30-05-2018
    """

    model = Event
    form_class = EventForm
    template_name = 'event/create.html'
    success_url = reverse_lazy('event:list')

    def dispatch(self, request, *args, **kwargs):
        """!
        Función que valida si el usuario del sistema tiene permisos para entrar a esta vista

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/'>Licencia de Software CENDITEL versión 1.2</a>
        @date 30-05-2018
        @param self <b>{object}</b> Objeto que instancia la clase
        @param request <b>{object}</b> Objeto que contiene la petición
        @param *args <b>{tupla}</b> Tupla de valores, inicialmente vacia
        @param **kwargs <b>{dict}</b> Diccionario de datos, inicialmente vacio
        @return Redirecciona al usuario a la página de error de permisos si no es su perfil
        """

        event = Event.objects.filter(pk=self.kwargs['pk'],user__pk=self.request.user.id)
        if event and self.request.user.profile.level == 1:
            return super(EventUpdateView, self).dispatch(request, *args, **kwargs)
        else:
            return redirect('base:error_403')

    def get_initial(self):
        """!
        Función que agrega valores predeterminados a los campos del formulario

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/'>Licencia de Software CENDITEL versión 1.2</a>
        @date 30-05-2018
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Diccionario con los valores predeterminados
        """

        initial_data = super(EventUpdateView, self).get_initial()
        initial_data['name'] = self.object.name
        initial_data['summary'] = self.object.summary
        initial_data['email'] = self.object.email
        initial_data['logo'] = self.object.logo
        initial_data['video'] = self.object.video
        initial_data['twitter_account'] = self.object.twitter_account
        initial_data['facebook_account'] = self.object.facebook_account
        initial_data['presentation'] = self.object.presentation
        initial_data['subscription'] = self.object.subscription
        initial_data['publication'] = self.object.publication
        initial_data['commentary'] = self.object.commentary
        initial_data['time'] = self.object.time
        initial_data['start_date'] = self.object.start_date
        initial_data['end_date'] = self.object.end_date
        initial_data['state'] = self.object.location.parish.municipality.state
        initial_data['municipality'] = self.object.location.parish.municipality
        initial_data['parish'] = self.object.location.parish
        initial_data['address'] = self.object.location.address
        return initial_data

    def form_valid(self, form):
        """!
        Función que valida si el formulario es correcto

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/'>Licencia de Software CENDITEL versión 1.2</a>
        @date 30-05-2018
        @param self <b>{object}</b> Objeto que instancia la clase
        @param form <b>{object}</b> Objeto que contiene el formulario de registro
        @return Formulario validado
        """

        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()

        location = Location.objects.get(pk=self.object.location.pk)
        location.address = form.cleaned_data['address']
        location.parish = form.cleaned_data['parish']
        location.save()

        return super(EventUpdateView, self).form_valid(form)

class EventDeleteView(DeleteView):
    """!
    Clase que permite a un usuario eliminar los datos de los eventos que ha registrado

    @author William Páez (wpaez at cenditel.gob.ve)
    @copyright <a href='http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/'>Licencia de Software CENDITEL versión 1.2</a>
    @date 08-06-2018
    """

    model = Event
    template_name = 'event/delete.html'
    success_url = reverse_lazy('event:list')

    def dispatch(self, request, *args, **kwargs):
        """!
        Función que valida si el usuario del sistema tiene permisos para entrar a esta vista

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/'>Licencia de Software CENDITEL versión 1.2</a>
        @date 09-06-2018
        @param self <b>{object}</b> Objeto que instancia la clase
        @param request <b>{object}</b> Objeto que contiene la petición
        @param *args <b>{tupla}</b> Tupla de valores, inicialmente vacia
        @param **kwargs <b>{dict}</b> Diccionario de datos, inicialmente vacio
        @return Redirecciona al usuario a la página de error de permisos si no es su perfil
        """

        event = Event.objects.filter(pk=self.kwargs['pk'],user__pk=self.request.user.id)
        if event and self.request.user.profile.level == 1:
            return super(EventDeleteView, self).dispatch(request, *args, **kwargs)
        else:
            return redirect('base:error_403')

class EventDetailView(DetailView):
    """!
    Clase que permite a un usuario ver todos los datos de un evento

    @author William Páez (wpaez at cenditel.gob.ve)
    @copyright <a href='http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/'>Licencia de Software CENDITEL versión 1.2</a>
    @date 11-06-2018
    """

    model = Event
    template_name = 'event/detail.html'

class SubscribeView(TemplateView):
    """!
    Clase que permite a un usuario suscribirse a un evento determinado

    @author William Páez (wpaez at cenditel.gob.ve)
    @copyright <a href='http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/'>Licencia de Software CENDITEL versión 1.2</a>
    @date 09-06-2018
    """

    template_name = 'event/subscribe.html'

    def dispatch(self, request, *args, **kwargs):
        """!
        Función que valida si el usuario del sistema tiene permisos para entrar a esta vista

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/'>Licencia de Software CENDITEL versión 1.2</a>
        @date 20-06-2018
        @param self <b>{object}</b> Objeto que instancia la clase
        @param request <b>{object}</b> Objeto que contiene la petición
        @param *args <b>{tupla}</b> Tupla de valores, inicialmente vacia
        @param **kwargs <b>{dict}</b> Diccionario de datos, inicialmente vacio
        @return Redirecciona al usuario a la página de error de permisos si no es su perfil y si el evento no esta abierto para suscripciones
        """

        event = Event.objects.filter(pk=self.kwargs['pk'],subscription=True,user__pk=self.request.user.id)
        if event and self.request.user.profile.level == 1:
            return super(SubscribeView, self).dispatch(request, *args, **kwargs)
        else:
            return redirect('base:error_403')

    def get_context_data(self, **kwargs):
        """!
        Método que suscribe a un usuario en un evento

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/'>Licencia de Software CENDITEL versión 1.2</a>
        @date 09-06-2018
        @param self <b>{object}</b> Objeto que instancia la clase
        @param **kwargs <b>{dict}</b> Diccionario de datos, inicialmente vacio
        @return Diccionario con el valor verdadero o falso. El valor determina si el usuario se suscribió al evento
        """

        context = super(SubscribeView, self).get_context_data(**kwargs)
        event_id = kwargs['pk']
        event = Event.objects.get(pk=event_id)
        if not Subscriber.objects.filter(event=event,profile=self.request.user.profile):
            subscriber = Subscriber(event=event,profile=self.request.user.profile,grant=False)
            subscriber.save()
            context['ok'] = True
        else:
            context['ok'] = False
        return context

class SubscribeReportView(TemplateView):
    """!
    Clase que muestra a todos los suscriptores que están inscritos en algún evento

    @author William Páez (wpaez at cenditel.gob.ve)
    @copyright <a href='http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/'>Licencia de Software CENDITEL versión 1.2</a>
    @date 09-06-2018
    """

    template_name = 'event/subscribe.report.html'

    def dispatch(self, request, *args, **kwargs):
        """!
        Función que valida si el usuario del sistema tiene permisos para entrar a esta vista

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/'>Licencia de Software CENDITEL versión 1.2</a>
        @date 23-06-2018
        @param self <b>{object}</b> Objeto que instancia la clase
        @param request <b>{object}</b> Objeto que contiene la petición
        @param *args <b>{tupla}</b> Tupla de valores, inicialmente vacia
        @param **kwargs <b>{dict}</b> Diccionario de datos, inicialmente vacio
        @return Redirecciona al usuario a la página de error de permisos si no es su perfil y si el evento no esta abierto para suscripciones
        """

        event = Event.objects.filter(pk=self.kwargs['pk'])
        if event:
            return super(SubscribeReportView, self).dispatch(request, *args, **kwargs)
        else:
            return redirect('base:error_403')

    def get_context_data(self, **kwargs):
        """!
        Función que muestra a todos los suscriptores que están en un evento

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/'>Licencia de Software CENDITEL versión 1.2</a>
        @date 09-06-2018
        @param self <b>{object}</b> Objeto que instancia la clase
        @param **kwargs <b>{dict}</b> Diccionario de datos, inicialmente vacio
        @return Diccionario con los suscriptores inscritos en un evento
        """

        context = super(SubscribeReportView, self).get_context_data(**kwargs)
        event_id = kwargs['pk']
        event = Event.objects.get(pk=event_id)
        context['subscriber'] = Subscriber.objects.filter(event=event)
        return context

class CertificateListView(ListView):
    """!
    Clase que permite a un usuario listar los certificados que tienen asignados los eventos

    @author William Páez (wpaez at cenditel.gob.ve)
    @copyright <a href='http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/'>Licencia de Software CENDITEL versión 1.2</a>
    @date 09-06-2018
    """

    model = Certificate
    template_name = 'event/certificate.list.html'

    def dispatch(self, request, *args, **kwargs):
        """!
        Función que valida si el usuario del sistema tiene permisos para entrar a esta vista

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/'>Licencia de Software CENDITEL versión 1.2</a>
        @date 30-05-2018
        @param self <b>{object}</b> Objeto que instancia la clase
        @param request <b>{object}</b> Objeto que contiene la petición
        @param *args <b>{tupla}</b> Tupla de valores, inicialmente vacia
        @param **kwargs <b>{dict}</b> Diccionario de datos, inicialmente vacio
        @return Redirecciona al usuario a la página de error de permisos en caso de no pertenecer a este nivel
        """

        if self.request.user.profile.level == 1:
            return super(CertificateListView, self).dispatch(request, *args, **kwargs)
        else:
            return redirect('base:error_403')

    def get_queryset(self):
        """!
        Función que obtiene la lista de certificados que están asociados a los eventos que registró el usuario

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/'>Licencia de Software CENDITEL versión 1.2</a>
        @date 20-06-2018
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Lista de objetos certificado asociados a los eventos que el usuario registró
        """

        queryset = Certificate.objects.filter(event__user=self.request.user)
        return queryset

class CertificateCreateView(CreateView):
    """!
    Clase que permite a un usuario registrar el diseño de los certificados para los eventos

    @author William Páez (wpaez at cenditel.gob.ve)
    @copyright <a href='http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/'>Licencia de Software CENDITEL versión 1.2</a>
    @date 09-06-2018
    """

    model = Certificate
    form_class = CertificateForm
    template_name = 'event/certificate.create.html'
    success_url = reverse_lazy('event:certificate_list')

    def dispatch(self, request, *args, **kwargs):
        """!
        Función que valida si el usuario del sistema tiene permisos para entrar a esta vista

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/'>Licencia de Software CENDITEL versión 1.2</a>
        @date 09-06-2018
        @param self <b>{object}</b> Objeto que instancia la clase
        @param request <b>{object}</b> Objeto que contiene la petición
        @param *args <b>{tupla}</b> Tupla de valores, inicialmente vacia
        @param **kwargs <b>{dict}</b> Diccionario de datos, inicialmente vacio
        @return Redirecciona al usuario a la página de error de permisos en caso de no pertenecer a este nivel
        """

        if self.request.user.profile.level == 1:
            return super(CertificateCreateView, self).dispatch(request, *args, **kwargs)
        else:
            return redirect('base:error_403')

    def get_form_kwargs(self):
        """!
        Función que permite pasar el usuario actualmente logueado al formulario

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/'>Licencia de Software CENDITEL versión 1.2</a>
        @date 09-06-2018
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Diccionario con el usuario actualmente logueado
        """

        kwargs = super(CertificateCreateView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        """!
        Función que valida si el formulario es correcto

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/'>Licencia de Software CENDITEL versión 1.2</a>
        @date 09-06-2018
        @param self <b>{object}</b> Objeto que instancia la clase
        @param form <b>{object}</b> Objeto que contiene el formulario de registro
        @return Formulario validado
        """

        self.object = form.save(commit=False)
        event = Event.objects.get(pk=form.cleaned_data['event'])
        self.object.event = event
        self.object.save()

        return super(CertificateCreateView, self).form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return super(CertificateCreateView, self).form_invalid(form)

class CertificateUpdateView(UpdateView):
    """!
    Clase que permite a un usuario actualizar los datos de los certificados

    @author William Páez (wpaez at cenditel.gob.ve)
    @copyright <a href='http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/'>Licencia de Software CENDITEL versión 1.2</a>
    @date 09-06-2018
    """

    model = Certificate
    form_class = CertificateForm
    template_name = 'event/certificate.create.html'
    success_url = reverse_lazy('event:certificate_list')

    def dispatch(self, request, *args, **kwargs):
        """!
        Función que valida si el usuario del sistema tiene permisos para entrar a esta vista

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/'>Licencia de Software CENDITEL versión 1.2</a>
        @date 30-05-2018
        @param self <b>{object}</b> Objeto que instancia la clase
        @param request <b>{object}</b> Objeto que contiene la petición
        @param *args <b>{tupla}</b> Tupla de valores, inicialmente vacia
        @param **kwargs <b>{dict}</b> Diccionario de datos, inicialmente vacio
        @return Redirecciona al usuario a la página de error de permisos si no es su perfil
        """

        certificate = Certificate.objects.filter(pk=self.kwargs['pk'],event__user__pk=self.request.user.id)

        if certificate and self.request.user.profile.level == 1:
            return super(CertificateUpdateView, self).dispatch(request, *args, **kwargs)
        else:
            return redirect('base:error_403')

    def get_form_kwargs(self):
        """!
        Función que permite pasar el usuario actualmente logueado al formulario

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/'>Licencia de Software CENDITEL versión 1.2</a>
        @date 09-06-2018
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Diccionario con el usuario actualmente logueado
        """

        kwargs = super(CertificateUpdateView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def get_initial(self):
        """!
        Función que agrega valores predeterminados a los campos del formulario

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/'>Licencia de Software CENDITEL versión 1.2</a>
        @date 09-06-2018
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Diccionario con los valores predeterminados
        """

        initial_data = super(CertificateUpdateView, self).get_initial()
        initial_data['front_image'] = self.object.front_image
        initial_data['back_image'] = self.object.back_image
        initial_data['coordinate_y_name'] = self.object.coordinate_y_name
        initial_data['thematic'] = self.object.thematic
        initial_data['event'] = self.object.event.id
        return initial_data

class CertificateDeleteView(DeleteView):
    """!
    Clase que permite a un usuario eliminar los datos de los certificados

    @author William Páez (wpaez at cenditel.gob.ve)
    @copyright <a href='http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/'>Licencia de Software CENDITEL versión 1.2</a>
    @date 09-06-2018
    """

    model = Certificate
    template_name = 'event/certificate.delete.html'
    success_url = reverse_lazy('event:certificado_list')

    def dispatch(self, request, *args, **kwargs):
        """!
        Función que valida si el usuario del sistema tiene permisos para entrar a esta vista

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/'>Licencia de Software CENDITEL versión 1.2</a>
        @date 08-06-2018
        @param self <b>{object}</b> Objeto que instancia la clase
        @param request <b>{object}</b> Objeto que contiene la petición
        @param *args <b>{tupla}</b> Tupla de valores, inicialmente vacia
        @param **kwargs <b>{dict}</b> Diccionario de datos, inicialmente vacio
        @return Redirecciona al usuario a la página de error de permisos si no es su perfil
        """

        certificate = Certificate.objects.filter(pk=self.kwargs['pk'],event__user__pk=self.request.user.id)

        if certificate and self.request.user.profile.level == 1:
            return super(CertificateDeleteView, self).dispatch(request, *args, **kwargs)
        else:
            return redirect('base:error_403')

class CertificateView(TemplateView):
    """!
    Clase que permite a un usuario otorgar los certificados a los suscriptores que participaron en el evento

    @author William Páez (wpaez at cenditel.gob.ve)
    @copyright <a href='http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/'>Licencia de Software CENDITEL versión 1.2</a>
    @date 09-06-2018
    """

    template_name = 'event/certificate.html'

    def dispatch(self, request, *args, **kwargs):
        """!
        Función que valida si el usuario del sistema tiene permisos para entrar a esta vista

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/'>Licencia de Software CENDITEL versión 1.2</a>
        @date 09-06-2018
        @param self <b>{object}</b> Objeto que instancia la clase
        @param request <b>{object}</b> Objeto que contiene la petición
        @param *args <b>{tupla}</b> Tupla de valores, inicialmente vacia
        @param **kwargs <b>{dict}</b> Diccionario de datos, inicialmente vacio
        @return Redirecciona al usuario a la página de error de permisos en caso de no pertenecer a este nivel
        """

        event = Event.objects.filter(pk=self.kwargs['pk'],user=self.request.user)
        if event and self.request.user.profile.level == 1:
            return super(CertificateView, self).dispatch(request, *args, **kwargs)
        else:
            return redirect('base:error_403')

    def get_context_data(self, **kwargs):
        """!
        Función que muestra a todos los suscriptores para otorgarles certificados

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/'>Licencia de Software CENDITEL versión 1.2</a>
        @date 09-06-2018
        @param self <b>{object}</b> Objeto que instancia la clase
        @param **kwargs <b>{dict}</b> Diccionario de datos, inicialmente vacio
        @return Retorna un diccionario con los suscriptores
        """

        context = super(CertificateView, self).get_context_data(**kwargs)
        event_id = kwargs['pk']
        event = Event.objects.get(pk=event_id)
        context['subscriber'] = Subscriber.objects.filter(event=event)
        return context

class SubscriberUpdateView(UpdateView):
    """!
    Clase que permite a un usuario cambiar el estado del certificado

    @author William Páez (wpaez at cenditel.gob.ve)
    @copyright <a href='http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/'>Licencia de Software CENDITEL versión 1.2</a>
    @date 09-06-2018
    """

    model = Subscriber
    form_class = SubscriberForm
    template_name = 'event/subscriber.update.html'
    success_url = reverse_lazy('event:certificate_list')

    def dispatch(self, request, *args, **kwargs):
        """!
        Función que valida si el usuario del sistema tiene permisos para entrar a esta vista

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/'>Licencia de Software CENDITEL versión 1.2</a>
        @date 09-06-2018
        @param self <b>{object}</b> Objeto que instancia la clase
        @param request <b>{object}</b> Objeto que contiene la petición
        @param *args <b>{tupla}</b> Tupla de valores, inicialmente vacia
        @param **kwargs <b>{dict}</b> Diccionario de datos, inicialmente vacio
        @return Redirecciona al usuario a la página de error de permisos si no es su perfil
        """

        event = Event.objects.filter(user__pk=self.request.user.id)
        if event and self.request.user.profile.level == 1:
            return super(SubscriberUpdateView, self).dispatch(request, *args, **kwargs)
        else:
            return redirect('base:error_403')

    def get_initial(self):
        """!
        Método que agrega valores predeterminados a los campos del formulario

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/'>Licencia de Software CENDITEL versión 1.2</a>
        @date 09-06-2018
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Diccionario con los valores predeterminados
        """

        initial_data = super(SubscriberUpdateView, self).get_initial()
        initial_data['grant'] = self.object.grant
        initial_data['event'] = self.object.event
        initial_data['profile'] = self.object.profile
        return initial_data

    def form_valid(self, form):
        """!
        Función que valida si el formulario es correcto

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/'>Licencia de Software CENDITEL versión 1.2</a>
        @date 31-10-2018
        @param self <b>{object}</b> Objeto que instancia la clase
        @param form <b>{object}</b> Objeto que contiene el formulario de registro
        @return Formulario validado
        """

        self.object = form.save(commit=False)
        self.object.grant = form.cleaned_data['grant']
        self.object.save()

        admin, admin_email = '', ''
        if settings.ADMINS:
            admin = settings.ADMINS[0][0]
            admin_email = settings.ADMINS[0][1]

        if self.object.grant:
            sent = send_email(self.object.profile.user.email, 'user/certificate.download.mail', 'Sofi - Descarga de Certificado', {'url':get_current_site(self.request).name,
                'event_id':self.object.event.id,'admin':admin, 'admin_email':admin_email,
            })

        return super(SubscriberUpdateView, self).form_valid(form)

class CertificateDownloadView(View):
    """!
    Clase que permite a un usuario descargar el certificado que tiene asociado a un evento

    @author Alexander Olivares (olivaresa at cantv.net)
    @author William Páez (wpaez at cenditel.gob.ve)
    @copyright <a href='http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/'>Licencia de Software CENDITEL versión 1.2</a>
    @date 09-06-2018
    """

    def dispatch(self, request, *args, **kwargs):
        """!
        Función que valida si el usuario del sistema tiene permisos para entrar a esta vista

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/'>Licencia de Software CENDITEL versión 1.2</a>
        @date 09-06-2018
        @param self <b>{object}</b> Objeto que instancia la clase
        @param request <b>{object}</b> Objeto que contiene la petición
        @param *args <b>{tupla}</b> Tupla de valores, inicialmente vacia
        @param **kwargs <b>{dict}</b> Diccionario de datos, inicialmente vacio
        @return Redirecciona al usuario a la página de error de permisos en caso de no pertenecer a este nivel
        """

        if not Subscriber.objects.filter(event=self.kwargs['evento'],profile=self.request.user.profile):
            return redirect('base:error_403')
        subscriber = Subscriber.objects.get(event=self.kwargs['evento'],profile=self.request.user.profile)
        if subscriber.grant:
            return super(CertificateDownloadView, self).dispatch(request, *args, **kwargs)
        else:
            return redirect('base:error_403')

    def get(self, request, *args, **kwargs):
        """!
        Función que construye el certificado con los datos del usuario

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/'>Licencia de Software CENDITEL versión 1.2</a>
        @date 20-06-2018
        @param self <b>{object}</b> Objeto que instancia la clase
        @param request <b>{object}</b> Objeto que contiene la petición
        @param *args <b>{tupla}</b> Tupla de valores, inicialmente vacia
        @param **kwargs <b>{dict}</b> Diccionario de datos, inicialmente vacio
        @return Certificado del usuario en un pdf
        """

        response = HttpResponse(content_type='application/pdf')
        if Subscriber.objects.filter(event=kwargs['evento'],profile=self.request.user.profile):
            subscriber = Subscriber.objects.get(event=kwargs['evento'],profile=self.request.user.profile)
            front_image = subscriber.event.certificate.front_image.path
            #print(imagen_delantera)

            if subscriber.event.certificate.back_image:
                back_image = subscriber.event.certificate.back_image.path
                #print(imagen_tracera)
            else:
                back_image = None

            certificate_width = subscriber.event.certificate.front_image.width / 2
            #print('ancho certificado: ' + str(ancho_certificado))

            name = subscriber.profile.user.first_name + subscriber.profile.user.last_name
            if len(name) <= 18:
                name_width = (len(name) * 22) / 2
            else:
                name_width = (len(name) * 14) / 2
            #print('ancho nombre: ' + str(ancho_nombre))

            coordinate_x_name = certificate_width - name_width
            #print(coordenada_x_nombre)

            coordinate_name = coordinate_x_name, subscriber.event.certificate.coordinate_y_name
            #print(coordenada_nombre)

            u = subscriber.profile.user.username[0] + '-' + subscriber.profile.user.username[1:3] + '.' + subscriber.profile.user.username[3:6] + '.' + subscriber.profile.user.username[6:]
            username = 'C.I.: %s' % u
            #print(len(username))

            username_width = (len(username) * 14) / 2
            #print(ancho_username)

            coordinate_x_username = certificate_width - username_width
            #print(coordenada_x_username)

            coordinate_username = coordinate_x_username, subscriber.event.certificate.coordinate_y_name - 40
            #print(coordenada_username)

            role_width = (len(LEVEL[subscriber.profile.level][1]) * 14) / 2
            #print(ancho_rol)
            coordinate_x_role = certificate_width - role_width
            coordinate_role = coordinate_x_role, subscriber.event.certificate.coordinate_y_name - 70
            #print(coordenada_rol)
            role =  LEVEL[subscriber.profile.level][1]

            thematic = subscriber.event.certificate.thematic

            pdfmetrics.registerFont(TTFont('Roboto-Regular','static/css/font/Roboto/Roboto-Regular.ttf'))
            addMapping('Roboto-Regular', 0, 0, 'Roboto-Regular')
            buffer = BytesIO()
            pdf = canvas.Canvas(buffer, landscape(letter), bottomup=50)
            front_img = Image.open(front_image)
            draw = ImageDraw.Draw(front_img)
            pdf.setTitle('%s-%s' % (subscriber.profile.user.username, subscriber.event.id))
            pdf.setAuthor('Sofi')
            #pdf.setSubject('')
            pdf.setCreator('CENDITEL')
            pdf.drawInlineImage(front_img,0,0)
            pdf.setFillColorRGB(0,0,0)
            pdf.setFont('Roboto-Regular', 30)
            pdf.drawString(coordinate_name[0],coordinate_name[1], subscriber.profile.user.first_name + ' ' + subscriber.profile.user.last_name)
            pdf.setFont('Roboto-Regular', 25)
            pdf.drawString(coordinate_username[0],coordinate_username[1], username)

            pdf.setFont('Roboto-Regular', 20)
            pdf.drawString(coordinate_role[0],coordinate_role[1], role)

            pdf.showPage()

            if back_image:
                back_img = Image.open(back_image)
                draw = ImageDraw.Draw(back_img)
                pdf.drawInlineImage(back_img,0,0)
                thematic_pdf = pdf.beginText(50,562)
                thematic_pdf.textLines(thematic.splitlines())
                pdf.drawText(thematic_pdf)
                pdf.showPage()

            pdf.save()
            pdf = buffer.getvalue()
            buffer.close()
            response['Content-Disposition'] = 'attachment; filename=%s-%s.pdf' % (subscriber.profile.user.username, subscriber.event.id)
            response.write(pdf)
        return response
