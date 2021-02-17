import os
from io import BytesIO

from base.functions import send_email
from base.models import Location
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView
)
from PIL import Image
from reportlab.lib.fonts import addMapping
from reportlab.lib.pagesizes import landscape, letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from user.forms import SubscriberForm
from user.models import Subscriber

from .forms import CertificateForm, EventForm
from .models import Certificate, Event


class EventListView(LoginRequiredMixin, ListView):
    """!
    Clase que permite a un usuario listar los eventos que ha registrado

    @author William Páez <wpaez@cenditel.gob.ve>
    @copyright <a href='https://tinyurl.com/y3tfnema'>
        Licencia de Software CENDITEL versión 1.2</a>
    """

    model = Event
    template_name = 'event/list.html'

    def dispatch(self, *args, **kwargs):
        """!
        Función que valida si el usuario del sistema tiene permisos para entrar
        a esta vista

        @author William Páez <wpaez@cenditel.gob.ve>
        @copyright <a href='https://tinyurl.com/y3tfnema'>
            Licencia de Software CENDITEL versión 1.2</a>
        @param self <b>{object}</b> Objeto que instancia la clase
        @param *args <b>{tupla}</b> Tupla de valores, inicialmente vacia
        @param **kwargs <b>{dict}</b> Diccionario de datos, inicialmente vacio
        @return Redirecciona al usuario a la página de error de permisos en
            caso de no pertenecer a este nivel
        """

        if self.request.user.groups.filter(name='Organizador'):
            return super().dispatch(*args, **kwargs)
        else:
            return redirect('base:error_403')

    def get_queryset(self):
        """!
        Función que obtiene la lista de eventos que están asociados al usuario

        @author William Páez <wpaez@cenditel.gob.ve>
        @copyright <a href='https://tinyurl.com/y3tfnema'>
            Licencia de Software CENDITEL versión 1.2</a>
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Lista de objetos evento que el usuario registró
        """

        queryset = Event.objects.filter(user=self.request.user)
        return queryset


class EventCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """!
    Clase que permite a un usuario registrar eventos

    @author William Páez <wpaez@cenditel.gob.ve>
    @copyright <a href='https://tinyurl.com/y3tfnema'>
        Licencia de Software CENDITEL versión 1.2</a>
    """

    model = Event
    form_class = EventForm
    template_name = 'event/create.html'
    success_url = reverse_lazy('event:list')
    success_message = 'Los datos fueron registrados correctamente.'

    def dispatch(self, *args, **kwargs):
        """!
        Función que valida si el usuario del sistema tiene permisos para entrar
        a esta vista

        @author William Páez <wpaez@cenditel.gob.ve>
        @copyright <a href='https://tinyurl.com/y3tfnema'>
            Licencia de Software CENDITEL versión 1.2</a>
        @param self <b>{object}</b> Objeto que instancia la clase
        @param *args <b>{tupla}</b> Tupla de valores, inicialmente vacia
        @param **kwargs <b>{dict}</b> Diccionario de datos, inicialmente vacio
        @return Redirecciona al usuario a la página de error de permisos en
            caso de no pertenecer a este nivel
        """

        if self.request.user.groups.filter(name='Organizador'):
            return super().dispatch(*args, **kwargs)
        else:
            return redirect('base:error_403')

    def form_valid(self, form):
        """!
        Función que valida si el formulario es correcto

        @author William Páez <wpaez@cenditel.gob.ve>
        @copyright <a href='https://tinyurl.com/y3tfnema'>
            Licencia de Software CENDITEL versión 1.2</a>
        @param self <b>{object}</b> Objeto que instancia la clase
        @param form <b>{object}</b> Objeto que contiene el formulario de
            registro
        @return Formulario validado
        """

        location = Location.objects.create(
            address=form.cleaned_data['address'],
            parish=form.cleaned_data['parish']
        )

        self.object = form.save(commit=False)
        self.object.location = location
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)


class EventUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """!
    Clase que permite a un usuario actualizar los datos de los eventos que ha
    registrado

    @author William Páez <wpaez@cenditel.gob.ve>
    @copyright <a href='https://tinyurl.com/y3tfnema'>
        Licencia de Software CENDITEL versión 1.2</a>
    """

    model = Event
    form_class = EventForm
    template_name = 'event/create.html'
    success_url = reverse_lazy('event:list')
    success_message = 'Los datos fueron actualizados correctamente.'

    def dispatch(self, *args, **kwargs):
        """!
        Función que valida si el usuario del sistema tiene permisos para entrar
        a esta vista

        @author William Páez <wpaez@cenditel.gob.ve>
        @copyright <a href='https://tinyurl.com/y3tfnema'>
            Licencia de Software CENDITEL versión 1.2</a>
        @param self <b>{object}</b> Objeto que instancia la clase
        @param *args <b>{tupla}</b> Tupla de valores, inicialmente vacia
        @param **kwargs <b>{dict}</b> Diccionario de datos, inicialmente vacio
        @return Redirecciona al usuario a la página de error de permisos si no
            es su perfil
        """

        event = Event.objects.filter(
            pk=self.kwargs['pk'], user__pk=self.request.user.id
        )
        if event and self.request.user.groups.filter(name='Organizador'):
            return super().dispatch(*args, **kwargs)
        else:
            return redirect('base:error_403')

    def get_initial(self):
        """!
        Función que agrega valores predeterminados a los campos del formulario

        @author William Páez <wpaez@cenditel.gob.ve>
        @copyright <a href='https://tinyurl.com/y3tfnema'>
            Licencia de Software CENDITEL versión 1.2</a>
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Diccionario con los valores predeterminados
        """

        initial_data = super().get_initial()
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

        @author William Páez <wpaez@cenditel.gob.ve>
        @copyright <a href='https://tinyurl.com/y3tfnema'>
            Licencia de Software CENDITEL versión 1.2</a>
        @param self <b>{object}</b> Objeto que instancia la clase
        @param form <b>{object}</b> Objeto que contiene el formulario de
            registro
        @return Formulario validado
        """

        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        location = Location.objects.get(pk=self.object.location.pk)
        location.address = form.cleaned_data['address']
        location.parish = form.cleaned_data['parish']
        location.save()
        return super().form_valid(form)


class EventDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    """!
    Clase que permite a un usuario eliminar los datos de los eventos que ha
    registrado

    @author William Páez <wpaez@cenditel.gob.ve>
    @copyright <a href='https://tinyurl.com/y3tfnema'>
        Licencia de Software CENDITEL versión 1.2</a>
    """

    model = Event
    template_name = 'event/delete.html'
    success_url = reverse_lazy('event:list')
    success_message = 'El registro seleccionado fue eliminado correctamente.'

    def dispatch(self, *args, **kwargs):
        """!
        Función que valida si el usuario del sistema tiene permisos para entrar
        a esta vista

        @author William Páez <wpaez@cenditel.gob.ve>
        @copyright <a href='https://tinyurl.com/y3tfnema'>
            Licencia de Software CENDITEL versión 1.2</a>
        @param self <b>{object}</b> Objeto que instancia la clase
        @param *args <b>{tupla}</b> Tupla de valores, inicialmente vacia
        @param **kwargs <b>{dict}</b> Diccionario de datos, inicialmente vacio
        @return Redirecciona al usuario a la página de error de permisos si no
            es su perfil
        """

        event = Event.objects.filter(
            pk=self.kwargs['pk'], user__pk=self.request.user.id
        )
        if event and self.request.user.groups.filter(name='Organizador'):
            return super().dispatch(*args, **kwargs)
        else:
            return redirect('base:error_403')


class EventDetailView(DetailView):
    """!
    Clase que permite a un usuario ver todos los datos de un evento

    @author William Páez <wpaez@cenditel.gob.ve>
    @copyright <a href='https://tinyurl.com/y3tfnema'>
        Licencia de Software CENDITEL versión 1.2</a>
    """

    model = Event
    template_name = 'event/detail.html'


class SubscribeView(LoginRequiredMixin, TemplateView):
    """!
    Clase que permite a un usuario suscribirse a un evento determinado

    @author William Páez <wpaez@cenditel.gob.ve>
    @copyright <a href='https://tinyurl.com/y3tfnema'>
        Licencia de Software CENDITEL versión 1.2</a>
    """

    template_name = 'event/subscribe.html'

    def dispatch(self, *args, **kwargs):
        """!
        Función que valida si el usuario del sistema tiene permisos para entrar
        a esta vista

        @author William Páez <wpaez@cenditel.gob.ve>
        @copyright <a href='https://tinyurl.com/y3tfnema'>
            Licencia de Software CENDITEL versión 1.2</a>
        @param self <b>{object}</b> Objeto que instancia la clase
        @param request <b>{object}</b> Objeto que contiene la petición
        @param *args <b>{tupla}</b> Tupla de valores, inicialmente vacia
        @param **kwargs <b>{dict}</b> Diccionario de datos, inicialmente vacio
        @return Redirecciona al usuario a la página de error de permisos si no
            es su perfil y si el evento no esta abierto para suscripciones
        """

        event = Event.objects.filter(
            pk=self.kwargs['pk'],
            subscription=True
        )
        if event and self.request.user.groups.filter(name='Participante'):
            return super().dispatch(*args, **kwargs)
        else:
            return redirect('base:error_403')

    def get_context_data(self, **kwargs):
        """!
        Método que suscribe a un usuario en un evento

        @author William Páez <wpaez@cenditel.gob.ve>
        @copyright <a href='https://tinyurl.com/y3tfnema'>
            Licencia de Software CENDITEL versión 1.2</a>
        @param self <b>{object}</b> Objeto que instancia la clase
        @param **kwargs <b>{dict}</b> Diccionario de datos, inicialmente vacio
        @return Diccionario con el valor verdadero o falso. El valor determina
            si el usuario se suscribió al evento
        """

        context = super().get_context_data(**kwargs)
        event_id = kwargs['pk']
        event = Event.objects.get(pk=event_id)
        if not Subscriber.objects.filter(
            event=event, profile=self.request.user.profile
        ):
            Subscriber.objects.create(
                event=event, profile=self.request.user.profile, grant=False
            )
            context['ok'] = True
        else:
            context['ok'] = False
        return context


class SubscribeReportView(TemplateView):
    """!
    Clase que muestra a todos los suscriptores que están inscritos en algún
    evento

    @author William Páez <wpaez@cenditel.gob.ve>
    @copyright <a href='https://tinyurl.com/y3tfnema'>
        Licencia de Software CENDITEL versión 1.2</a>
    """

    template_name = 'event/subscribe_report.html'

    def dispatch(self, *args, **kwargs):
        """!
        Función que valida si el usuario del sistema tiene permisos para entrar
        a esta vista

        @author William Páez <wpaez@cenditel.gob.ve>
        @copyright <a href='https://tinyurl.com/y3tfnema'>
            Licencia de Software CENDITEL versión 1.2</a>
        @param self <b>{object}</b> Objeto que instancia la clase
        @param *args <b>{tupla}</b> Tupla de valores, inicialmente vacia
        @param **kwargs <b>{dict}</b> Diccionario de datos, inicialmente vacio
        @return Redirecciona al usuario a la página de error de permisos si no
            es su perfil y si el evento no esta abierto para suscripciones
        """

        event = Event.objects.filter(pk=self.kwargs['pk'])
        if event:
            return super().dispatch(*args, **kwargs)
        else:
            return redirect('base:error_403')

    def get_context_data(self, **kwargs):
        """!
        Función que muestra a todos los suscriptores que están en un evento

        @author William Páez <wpaez@cenditel.gob.ve>
        @copyright <a href='https://tinyurl.com/y3tfnema'>
            Licencia de Software CENDITEL versión 1.2</a>
        @param self <b>{object}</b> Objeto que instancia la clase
        @param **kwargs <b>{dict}</b> Diccionario de datos, inicialmente vacio
        @return Diccionario con los suscriptores inscritos en un evento
        """

        context = super().get_context_data(**kwargs)
        event_id = kwargs['pk']
        event = Event.objects.get(pk=event_id)
        context['subscribers'] = Subscriber.objects.filter(event=event)
        return context


class CertificateListView(LoginRequiredMixin, ListView):
    """!
    Clase que permite a un usuario listar los certificados que tienen asignados
    los eventos

    @author William Páez <wpaez@cenditel.gob.ve>
    @copyright <a href='https://tinyurl.com/y3tfnema'>
        Licencia de Software CENDITEL versión 1.2</a>
    """

    model = Certificate
    template_name = 'event/certificate_list.html'

    def dispatch(self, *args, **kwargs):
        """!
        Función que valida si el usuario del sistema tiene permisos para entrar
        a esta vista

        @author William Páez <wpaez@cenditel.gob.ve>
        @copyright <a href='https://tinyurl.com/y3tfnema'>
            Licencia de Software CENDITEL versión 1.2</a>
        @param self <b>{object}</b> Objeto que instancia la clase
        @param *args <b>{tupla}</b> Tupla de valores, inicialmente vacia
        @param **kwargs <b>{dict}</b> Diccionario de datos, inicialmente vacio
        @return Redirecciona al usuario a la página de error de permisos en
            caso de no pertenecer a este nivel
        """

        if self.request.user.groups.filter(name='Organizador'):
            return super().dispatch(*args, **kwargs)
        else:
            return redirect('base:error_403')

    def get_queryset(self):
        """!
        Función que obtiene la lista de certificados que están asociados a los
        eventos que registró el usuario

        @author William Páez <wpaez@cenditel.gob.ve>
        @copyright <a href='https://tinyurl.com/y3tfnema'>
            Licencia de Software CENDITEL versión 1.2</a>
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Lista de objetos certificado asociados a los eventos que el
            usuario registró
        """

        queryset = Certificate.objects.filter(event__user=self.request.user)
        return queryset


class CertificateCreateView(
    LoginRequiredMixin, SuccessMessageMixin, CreateView
):
    """!
    Clase que permite a un usuario registrar el diseño de los certificados
    para los eventos

    @author William Páez <wpaez@cenditel.gob.ve>
    @copyright <a href='https://tinyurl.com/y3tfnema'>
        Licencia de Software CENDITEL versión 1.2</a>
    """

    model = Certificate
    form_class = CertificateForm
    template_name = 'event/certificate_create.html'
    success_url = reverse_lazy('event:certificate_list')
    success_message = 'Los datos fueron registrados correctamente.'

    def dispatch(self, *args, **kwargs):
        """!
        Función que valida si el usuario del sistema tiene permisos para entrar
        a esta vista

        @author William Páez <wpaez@cenditel.gob.ve>
        @copyright <a href='https://tinyurl.com/y3tfnema'>
            Licencia de Software CENDITEL versión 1.2</a>
        @param self <b>{object}</b> Objeto que instancia la clase
        @param *args <b>{tupla}</b> Tupla de valores, inicialmente vacia
        @param **kwargs <b>{dict}</b> Diccionario de datos, inicialmente vacio
        @return Redirecciona al usuario a la página de error de permisos en
            caso de no pertenecer a este nivel
        """

        if self.request.user.groups.filter(name='Organizador'):
            return super().dispatch(*args, **kwargs)
        else:
            return redirect('base:error_403')

    def get_form_kwargs(self):
        """!
        Función que permite pasar el usuario actualmente logueado al formulario

        @author William Páez <wpaez@cenditel.gob.ve>
        @copyright <a href='https://tinyurl.com/y3tfnema'>
            Licencia de Software CENDITEL versión 1.2</a>
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Diccionario con el usuario actualmente logueado
        """

        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        """!
        Función que valida si el formulario es correcto

        @author William Páez <wpaez@cenditel.gob.ve>
        @copyright <a href='https://tinyurl.com/y3tfnema'>
            Licencia de Software CENDITEL versión 1.2</a>
        @param self <b>{object}</b> Objeto que instancia la clase
        @param form <b>{object}</b> Objeto que contiene el formulario de
            registro
        @return Formulario validado
        """

        self.object = form.save(commit=False)
        event = Event.objects.get(pk=form.cleaned_data['event'])
        self.object.event = event
        self.object.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)


class CertificateUpdateView(
    LoginRequiredMixin, SuccessMessageMixin, UpdateView
):
    """!
    Clase que permite a un usuario actualizar los datos de los certificados

    @author William Páez <wpaez@cenditel.gob.ve>
    @copyright <a href='https://tinyurl.com/y3tfnema'>
        Licencia de Software CENDITEL versión 1.2</a>
    """

    model = Certificate
    form_class = CertificateForm
    template_name = 'event/certificate_create.html'
    success_url = reverse_lazy('event:certificate_list')
    success_message = 'Los datos fueron actualizados correctamente.'

    def dispatch(self, *args, **kwargs):
        """!
        Función que valida si el usuario del sistema tiene permisos para entrar
        a esta vista

        @author William Páez <wpaez@cenditel.gob.ve>
        @copyright <a href='https://tinyurl.com/y3tfnema'>
            Licencia de Software CENDITEL versión 1.2</a>
        @param self <b>{object}</b> Objeto que instancia la clase
        @param *args <b>{tupla}</b> Tupla de valores, inicialmente vacia
        @param **kwargs <b>{dict}</b> Diccionario de datos, inicialmente vacio
        @return Redirecciona al usuario a la página de error de permisos si no
            es su perfil
        """

        certificate = Certificate.objects.filter(
            pk=self.kwargs['pk'], event__user__pk=self.request.user.id
        )

        if certificate and self.request.user.groups.filter(name='Organizador'):
            return super().dispatch(*args, **kwargs)
        else:
            return redirect('base:error_403')

    def get_form_kwargs(self):
        """!
        Función que permite pasar el usuario actualmente logueado al formulario

        @author William Páez <wpaez@cenditel.gob.ve>
        @copyright <a href='https://tinyurl.com/y3tfnema'>
            Licencia de Software CENDITEL versión 1.2</a>
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Diccionario con el usuario actualmente logueado
        """

        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def get_initial(self):
        """!
        Función que agrega valores predeterminados a los campos del formulario

        @author William Páez <wpaez@cenditel.gob.ve>
        @copyright <a href='https://tinyurl.com/y3tfnema'>
            Licencia de Software CENDITEL versión 1.2</a>
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Diccionario con los valores predeterminados
        """

        initial_data = super().get_initial()
        initial_data['front_image'] = self.object.front_image
        initial_data['back_image'] = self.object.back_image
        initial_data['coordinate_y_name'] = self.object.coordinate_y_name
        initial_data['thematic'] = self.object.thematic
        initial_data['event'] = self.object.event.id
        return initial_data


class CertificateDeleteView(
    LoginRequiredMixin, SuccessMessageMixin, DeleteView
):
    """!
    Clase que permite a un usuario eliminar los datos de los certificados

    @author William Páez <wpaez@cenditel.gob.ve>
    @copyright <a href='https://tinyurl.com/y3tfnema'>
        Licencia de Software CENDITEL versión 1.2</a>
    """

    model = Certificate
    template_name = 'event/certificate_delete.html'
    success_url = reverse_lazy('event:certificado_list')
    success_message = 'El registro seleccionado fue eliminado correctamente.'

    def dispatch(self, *args, **kwargs):
        """!
        Función que valida si el usuario del sistema tiene permisos para entrar
        a esta vista

        @author William Páez <wpaez@cenditel.gob.ve>
        @copyright <a href='https://tinyurl.com/y3tfnema'>
            Licencia de Software CENDITEL versión 1.2</a>
        @param self <b>{object}</b> Objeto que instancia la clase
        @param *args <b>{tupla}</b> Tupla de valores, inicialmente vacia
        @param **kwargs <b>{dict}</b> Diccionario de datos, inicialmente vacio
        @return Redirecciona al usuario a la página de error de permisos si no
            es su perfil
        """

        certificate = Certificate.objects.filter(
            pk=self.kwargs['pk'], event__user__pk=self.request.user.id
        )

        if certificate and self.request.user.groups.filter(name='Organizador'):
            return super().dispatch(*args, **kwargs)
        else:
            return redirect('base:error_403')


class CertificateView(LoginRequiredMixin, TemplateView):
    """!
    Clase que permite a un usuario otorgar los certificados a los suscriptores
    que participaron en el evento

    @author William Páez <wpaez@cenditel.gob.ve>
    @copyright <a href='https://tinyurl.com/y3tfnema'>
        Licencia de Software CENDITEL versión 1.2</a>
    """

    template_name = 'event/certificate.html'

    def dispatch(self, *args, **kwargs):
        """!
        Función que valida si el usuario del sistema tiene permisos para entrar
        a esta vista

        @author William Páez <wpaez@cenditel.gob.ve>
        @copyright <a href='https://tinyurl.com/y3tfnema'>
            Licencia de Software CENDITEL versión 1.2</a>
        @param self <b>{object}</b> Objeto que instancia la clase
        @param *args <b>{tupla}</b> Tupla de valores, inicialmente vacia
        @param **kwargs <b>{dict}</b> Diccionario de datos, inicialmente vacio
        @return Redirecciona al usuario a la página de error de permisos en
            caso de no pertenecer a este nivel
        """

        event = Event.objects.filter(
            pk=self.kwargs['pk'], user=self.request.user
        )
        if event and self.request.user.groups.filter(name='Organizador'):
            return super().dispatch(*args, **kwargs)
        else:
            return redirect('base:error_403')

    def get_context_data(self, **kwargs):
        """!
        Función que muestra a todos los suscriptores para otorgarles
        certificados

        @author William Páez <wpaez@cenditel.gob.ve>
        @copyright <a href='https://tinyurl.com/y3tfnema'>
            Licencia de Software CENDITEL versión 1.2</a>
        @param self <b>{object}</b> Objeto que instancia la clase
        @param **kwargs <b>{dict}</b> Diccionario de datos, inicialmente vacio
        @return Retorna un diccionario con los suscriptores
        """

        context = super().get_context_data(**kwargs)
        event_id = kwargs['pk']
        event = Event.objects.get(pk=event_id)
        context['subscribers'] = Subscriber.objects.filter(event=event)
        return context


class SubscriberUpdateView(
    LoginRequiredMixin, SuccessMessageMixin, UpdateView
):
    """!
    Clase que permite a un usuario cambiar el estado del certificado

    @author William Páez <wpaez@cenditel.gob.ve>
    @copyright <a href='https://tinyurl.com/y3tfnema'>
        Licencia de Software CENDITEL versión 1.2</a>
    """

    model = Subscriber
    form_class = SubscriberForm
    template_name = 'event/subscriber_update.html'
    success_url = reverse_lazy('event:certificate_list')
    success_message = 'Los datos fueron actualizados correctamente.'

    def dispatch(self, *args, **kwargs):
        """!
        Función que valida si el usuario del sistema tiene permisos para entrar
        a esta vista

        @author William Páez <wpaez@cenditel.gob.ve>
        @copyright <a href='https://tinyurl.com/y3tfnema'>
            Licencia de Software CENDITEL versión 1.2</a>
        @param self <b>{object}</b> Objeto que instancia la clase
        @param *args <b>{tupla}</b> Tupla de valores, inicialmente vacia
        @param **kwargs <b>{dict}</b> Diccionario de datos, inicialmente vacio
        @return Redirecciona al usuario a la página de error de permisos si no
            es su perfil
        """

        event = Event.objects.filter(user__pk=self.request.user.id)
        if event and self.request.user.groups.filter(name='Organizador'):
            return super().dispatch(*args, **kwargs)
        else:
            return redirect('base:error_403')

    def get_initial(self):
        """!
        Método que agrega valores predeterminados a los campos del formulario

        @author William Páez <wpaez@cenditel.gob.ve>
        @copyright <a href='https://tinyurl.com/y3tfnema'>
            Licencia de Software CENDITEL versión 1.2</a>
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Diccionario con los valores predeterminados
        """

        initial_data = super().get_initial()
        initial_data['grant'] = self.object.grant
        initial_data['event'] = self.object.event
        initial_data['profile'] = self.object.profile
        return initial_data

    def form_valid(self, form):
        """!
        Función que valida si el formulario es correcto

        @author William Páez <wpaez@cenditel.gob.ve>
        @copyright <a href='https://tinyurl.com/y3tfnema'>
            Licencia de Software CENDITEL versión 1.2</a>
        @param self <b>{object}</b> Objeto que instancia la clase
        @param form <b>{object}</b> Objeto que contiene el formulario de
            registro
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
            send_email(
                self.object.profile.user.email,
                'user/certificate_download.mail',
                'Sofi - Descarga de Certificado',
                {
                    'url': get_current_site(self.request).name,
                    'event_id': self.object.event.id, 'admin': admin,
                    'admin_email': admin_email,
                }
            )
        return super().form_valid(form)


class CertificateDownloadView(LoginRequiredMixin, View):
    """!
    Clase que permite a un usuario descargar el certificado que tiene asociado
    a un evento

    @author Alexander Olivares <olivaresa@cantv.net>
    @author William Páez <wpaez@cenditel.gob.ve>
    @copyright <a href='https://tinyurl.com/y3tfnema'>
        Licencia de Software CENDITEL versión 1.2</a>
    """

    def dispatch(self, *args, **kwargs):
        """!
        Función que valida si el usuario del sistema tiene permisos para entrar
        a esta vista

        @author William Páez <wpaez@cenditel.gob.ve>
        @copyright <a href='https://tinyurl.com/y3tfnema'>
            Licencia de Software CENDITEL versión 1.2</a>
        @param self <b>{object}</b> Objeto que instancia la clase
        @param *args <b>{tupla}</b> Tupla de valores, inicialmente vacia
        @param **kwargs <b>{dict}</b> Diccionario de datos, inicialmente vacio
        @return Redirecciona al usuario a la página de error de permisos en
            caso de no pertenecer a este nivel
        """

        if not Subscriber.objects.filter(
            event=self.kwargs['evento'], profile=self.request.user.profile
        ):
            return redirect('base:error_403')
        subscriber = Subscriber.objects.get(
            event=self.kwargs['evento'], profile=self.request.user.profile
        )
        if subscriber.grant:
            return super().dispatch(*args, **kwargs)
        else:
            return redirect('base:error_403')

    def get(self, request, *args, **kwargs):
        """!
        Función que construye el certificado con los datos del usuario

        @author William Páez <wpaez@cenditel.gob.ve>
        @copyright <a href='https://tinyurl.com/y3tfnema'>
            Licencia de Software CENDITEL versión 1.2</a>
        @param self <b>{object}</b> Objeto que instancia la clase
        @param request <b>{object}</b> Objeto que contiene la petición
        @param *args <b>{tupla}</b> Tupla de valores, inicialmente vacia
        @param **kwargs <b>{dict}</b> Diccionario de datos, inicialmente vacio
        @return Certificado del usuario en un pdf
        """

        response = HttpResponse(content_type='application/pdf')
        if Subscriber.objects.filter(
            event=kwargs['evento'], profile=self.request.user.profile
        ):
            subscriber = Subscriber.objects.get(
                event=kwargs['evento'], profile=self.request.user.profile
            )
            front_image = subscriber.event.certificate.front_image.path
            # print(imagen_delantera)

            if subscriber.event.certificate.back_image:
                back_image = subscriber.event.certificate.back_image.path
                # print(imagen_tracera)
            else:
                back_image = None

            width = subscriber.event.certificate.front_image.width
            certificate_width = width / 2
            # print('ancho certificado: ' + str(ancho_certificado))

            first_name = subscriber.profile.user.first_name
            last_name = subscriber.profile.user.last_name
            name = first_name + last_name

            if len(name) <= 18:
                name_width = (len(name) * 22) / 2
            else:
                name_width = (len(name) * 14) / 2
            # print('ancho nombre: ' + str(ancho_nombre))

            coordinate_x_name = certificate_width - name_width
            # print(coordenada_x_nombre)

            coordinate_y_name = subscriber.event.certificate.coordinate_y_name
            coordinate_name = coordinate_x_name, coordinate_y_name
            # print(coordenada_nombre)

            u = subscriber.profile.user.username[0] + '-' +\
                subscriber.profile.user.username[1:3] + '.' +\
                subscriber.profile.user.username[3:6] + '.' +\
                subscriber.profile.user.username[6:]
            username = 'C.I.: %s' % u
            # print(len(username))

            username_width = (len(username) * 14) / 2
            # print(ancho_username)

            coordinate_x_username = certificate_width - username_width
            # print(coordenada_x_username)

            coordinate_y_name = subscriber.event.certificate.coordinate_y_name
            coordinate_username = coordinate_x_username, coordinate_y_name - 40
            # print(coordenada_username)

            group = self.request.user.groups.all()
            role_width = (len(str(group[0])) * 14) / 2
            # print(ancho_rol)
            coordinate_x_role = certificate_width - role_width

            coordinate_y_name = subscriber.event.certificate.coordinate_y_name
            coordinate_role = coordinate_x_role, coordinate_y_name - 70
            # print(coordenada_rol)
            role = str(group[0])

            thematic = subscriber.event.certificate.thematic

            BASE_DIR = os.path.dirname(
                os.path.dirname(os.path.abspath(__file__))
            )
            pdfmetrics.registerFont(
                TTFont(
                    'Roboto-Regular',
                    os.path.join(
                        BASE_DIR, 'static/css/font/Roboto/Roboto-Regular.ttf'
                    )
                )
            )
            addMapping('Roboto-Regular', 0, 0, 'Roboto-Regular')
            buffer = BytesIO()
            pdf = canvas.Canvas(buffer, landscape(letter), bottomup=50)
            front_img = Image.open(front_image)
            # ImageDraw.Draw(front_img)
            # draw = ImageDraw.Draw(front_img)
            pdf.setTitle(
                '%s-%s' %
                (subscriber.profile.user.username, subscriber.event.id)
            )
            pdf.setAuthor('Sofi')
            # pdf.setSubject('')
            pdf.setCreator('CENDITEL')
            pdf.drawInlineImage(front_img, 0, 0)
            pdf.setFillColorRGB(0, 0, 0)
            pdf.setFont('Roboto-Regular', 30)
            first_name = subscriber.profile.user.first_name
            last_name = subscriber.profile.user.last_name
            pdf.drawString(
                coordinate_name[0], coordinate_name[1],
                first_name + ' ' + last_name
            )
            pdf.setFont('Roboto-Regular', 25)
            pdf.drawString(
                coordinate_username[0], coordinate_username[1], username
            )

            pdf.setFont('Roboto-Regular', 20)
            pdf.drawString(coordinate_role[0], coordinate_role[1], role)

            pdf.showPage()

            if back_image:
                back_img = Image.open(back_image)
                # ImageDraw.Draw(back_img)
                # draw = ImageDraw.Draw(back_img)
                pdf.drawInlineImage(back_img, 0, 0)
                thematic_pdf = pdf.beginText(50, 562)
                thematic_pdf.textLines(thematic.splitlines())
                pdf.drawText(thematic_pdf)
                pdf.showPage()

            pdf.save()
            pdf = buffer.getvalue()
            buffer.close()
            username = subscriber.profile.user.username
            id = subscriber.event.id
            response[
                'Content-Disposition'
            ] = 'attachment; filename=%s-%s.pdf' % (username, id)
            response.write(pdf)
        return response
