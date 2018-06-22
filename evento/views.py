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
## @namespace evento.views
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
from .models import Evento, Certificado
from .forms import EventoForm, CertificadoForm
from usuario.models import Suscriptor, Perfil
from usuario.forms import SuscriptorForm
from base.models import Ubicacion
from base.constant import NIVEL

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.fonts import addMapping
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape
from PIL import Image, ImageDraw
from io import BytesIO

class EventoListView(ListView):
    """!
    Clase que permite a un usuario listar los eventos que ha registrado

    @author William Páez (wpaez at cenditel.gob.ve)
    @copyright <a href='http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/'>Licencia de Software CENDITEL versión 1.2</a>
    @date 30-05-2018
    """

    model = Evento
    template_name = 'evento/listar.html'

    def dispatch(self, request, *args, **kwargs):
        """!
        Método que valida si el usuario del sistema tiene permisos para entrar a esta vista

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/'>Licencia de Software CENDITEL versión 1.2</a>
        @date 30-05-2018
        @param self <b>{object}</b> Objeto que instancia la clase
        @param request <b>{object}</b> Objeto que contiene la petición
        @param *args <b>{tupla}</b> Tupla de valores, inicialmente vacia
        @param **kwargs <b>{dict}</b> Diccionario de datos, inicialmente vacio
        @return Redirecciona al usuario a la página de error de permisos en caso de no pertenecer a este nivel
        """

        if self.request.user.perfil.nivel == 1:
            return super(EventoListView, self).dispatch(request, *args, **kwargs)
        else:
            return redirect('base:error_403')

    def get_queryset(self):
        """!
        Método que obtiene la lista de eventos que están asociados al usuario

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/'>Licencia de Software CENDITEL versión 1.2</a>
        @date 20-06-2018
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Retorna la lista de objetos evento que el usuario registró
        """

        queryset = Evento.objects.filter(user=self.request.user)
        return queryset

class EventoCreateView(CreateView):
    """!
    Clase que permite a un usuario registrar eventos

    @author William Páez (wpaez at cenditel.gob.ve)
    @copyright <a href='http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/'>Licencia de Software CENDITEL versión 1.2</a>
    @date 30-05-2018
    """

    model = Evento
    form_class = EventoForm
    template_name = 'evento/registrar.html'
    success_url = reverse_lazy('evento:listar')

    def dispatch(self, request, *args, **kwargs):
        """!
        Método que valida si el usuario del sistema tiene permisos para entrar a esta vista

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/'>Licencia de Software CENDITEL versión 1.2</a>
        @date 08-06-2018
        @param self <b>{object}</b> Objeto que instancia la clase
        @param request <b>{object}</b> Objeto que contiene la petición
        @param *args <b>{tupla}</b> Tupla de valores, inicialmente vacia
        @param **kwargs <b>{dict}</b> Diccionario de datos, inicialmente vacio
        @return Redirecciona al usuario a la página de error de permisos en caso de no pertenecer a este nivel
        """

        if self.request.user.perfil.nivel == 1:
            return super(EventoCreateView, self).dispatch(request, *args, **kwargs)
        else:
            return redirect('base:error_403')

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

        ubicacion = Ubicacion.objects.create(
            direccion = form.cleaned_data['direccion'],
            parroquia = form.cleaned_data['parroquia']
        )

        self.object = form.save(commit=False)
        self.object.ubicacion = ubicacion
        self.object.user = self.request.user
        self.object.save()

        return super(EventoCreateView, self).form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return super(EventoCreateView, self).form_invalid(form)

class EventoUpdateView(UpdateView):
    """!
    Clase que permite a un usuario actualizar los datos de los eventos que ha registrado

    @author William Páez (wpaez at cenditel.gob.ve)
    @copyright <a href='http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/'>Licencia de Software CENDITEL versión 1.2</a>
    @date 30-05-2018
    """

    model = Evento
    form_class = EventoForm
    template_name = 'evento/registrar.html'
    success_url = reverse_lazy('evento:listar')

    def dispatch(self, request, *args, **kwargs):
        """!
        Método que valida si el usuario del sistema tiene permisos para entrar a esta vista

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/'>Licencia de Software CENDITEL versión 1.2</a>
        @date 30-05-2018
        @param self <b>{object}</b> Objeto que instancia la clase
        @param request <b>{object}</b> Objeto que contiene la petición
        @param *args <b>{tupla}</b> Tupla de valores, inicialmente vacia
        @param **kwargs <b>{dict}</b> Diccionario de datos, inicialmente vacio
        @return Redirecciona al usuario a la página de error de permisos si no es su perfil
        """

        evento = Evento.objects.filter(pk=self.kwargs['pk'],user__pk=self.request.user.id)
        if evento and self.request.user.perfil.nivel == 1:
            return super(EventoUpdateView, self).dispatch(request, *args, **kwargs)
        else:
            return redirect('base:error_403')

    def get_initial(self):
        """!
        Método que agrega valores predeterminados a los campos del formulario

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/'>Licencia de Software CENDITEL versión 1.2</a>
        @date 30-05-2018
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Retorna un diccionario con los valores predeterminados
        """

        datos_iniciales = super(EventoUpdateView, self).get_initial()
        evento = Evento.objects.get(pk=self.object.id)
        datos_iniciales['nombre'] = evento.nombre
        datos_iniciales['resumen'] = evento.resumen
        datos_iniciales['correo'] = evento.correo
        datos_iniciales['logo'] = evento.logo
        datos_iniciales['video'] = evento.video
        datos_iniciales['cuenta_twitter'] = evento.cuenta_twitter
        datos_iniciales['cuenta_facebook'] = evento.cuenta_facebook
        datos_iniciales['presentacion'] = evento.presentacion
        datos_iniciales['suscripcion'] = evento.suscripcion
        datos_iniciales['publicacion'] = evento.publicacion
        datos_iniciales['comentario'] = evento.comentario
        datos_iniciales['fecha'] = evento.fecha
        datos_iniciales['fecha_inicial'] = evento.fecha_inicial
        datos_iniciales['fecha_final'] = evento.fecha_final
        datos_iniciales['estado'] = evento.ubicacion.parroquia.municipio.estado
        datos_iniciales['municipio'] = evento.ubicacion.parroquia.municipio
        datos_iniciales['parroquia'] = evento.ubicacion.parroquia
        datos_iniciales['direccion'] = evento.ubicacion.direccion
        return datos_iniciales

    def form_valid(self, form):
        """!
        Método que valida si el formulario es correcto

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

        ubicacion = Ubicacion.objects.get(pk=self.object.ubicacion.pk)
        ubicacion.direccion = form.cleaned_data['direccion']
        ubicacion.parroquia = form.cleaned_data['parroquia']
        ubicacion.save()

        return super(EventoUpdateView, self).form_valid(form)

class EventoDeleteView(DeleteView):
    """!
    Clase que permite a un usuario eliminar los datos de los eventos que ha registrado

    @author William Páez (wpaez at cenditel.gob.ve)
    @copyright <a href='http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/'>Licencia de Software CENDITEL versión 1.2</a>
    @date 08-06-2018
    """

    model = Evento
    template_name = "evento/eliminar.html"
    success_url = reverse_lazy('evento:listar')

    def dispatch(self, request, *args, **kwargs):
        """!
        Método que valida si el usuario del sistema tiene permisos para entrar a esta vista

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/'>Licencia de Software CENDITEL versión 1.2</a>
        @date 09-06-2018
        @param self <b>{object}</b> Objeto que instancia la clase
        @param request <b>{object}</b> Objeto que contiene la petición
        @param *args <b>{tupla}</b> Tupla de valores, inicialmente vacia
        @param **kwargs <b>{dict}</b> Diccionario de datos, inicialmente vacio
        @return Redirecciona al usuario a la página de error de permisos si no es su perfil
        """

        evento = Evento.objects.filter(pk=self.kwargs['pk'],user__pk=self.request.user.id)
        if evento and self.request.user.perfil.nivel == 1:
            return super(EventoDeleteView, self).dispatch(request, *args, **kwargs)
        else:
            return redirect('base:error_403')

class EventoDetailView(DetailView):
    """!
    Clase que permite a un usuario ver todos los datos de un evento

    @author William Páez (wpaez at cenditel.gob.ve)
    @copyright <a href='http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/'>Licencia de Software CENDITEL versión 1.2</a>
    @date 11-06-2018
    """

    model = Evento
    template_name = 'evento/detalle.html'

class SuscribirView(TemplateView):
    """!
    Clase que permite a un usuario suscribirse a un evento determinado

    @author William Páez (wpaez at cenditel.gob.ve)
    @copyright <a href='http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/'>Licencia de Software CENDITEL versión 1.2</a>
    @date 09-06-2018
    """

    template_name = 'evento/suscribir.html'

    def dispatch(self, request, *args, **kwargs):
        """!
        Método que valida si el usuario del sistema tiene permisos para entrar a esta vista

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/'>Licencia de Software CENDITEL versión 1.2</a>
        @date 20-06-2018
        @param self <b>{object}</b> Objeto que instancia la clase
        @param request <b>{object}</b> Objeto que contiene la petición
        @param *args <b>{tupla}</b> Tupla de valores, inicialmente vacia
        @param **kwargs <b>{dict}</b> Diccionario de datos, inicialmente vacio
        @return Redirecciona al usuario a la página de error de permisos si no es su perfil y si el evento no esta abierto para suscripciones
        """

        evento = Evento.objects.filter(pk=self.kwargs['pk'],suscripcion=True,user__pk=self.request.user.id)
        if evento and self.request.user.perfil.nivel == 1:
            return super(SuscribirView, self).dispatch(request, *args, **kwargs)
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
        @return Retorna un diccionario con el valor verdadero o falso. El valor determina si el usuario se suscribió al evento
        """

        context = super(SuscribirView, self).get_context_data(**kwargs)
        evento_id = kwargs['pk']
        evento = Evento.objects.get(pk=evento_id)
        if not Suscriptor.objects.filter(evento=evento,perfil=self.request.user.perfil):
            suscriptor = Suscriptor(evento=evento,perfil=self.request.user.perfil,otorgar=False)
            suscriptor.save()
            context['ok'] = True
        else:
            context['ok'] = False
        return context

class SuscribirReporteView(TemplateView):
    """!
    Clase que muestra a todos los suscriptores que están inscritos en algún evento

    @author William Páez (wpaez at cenditel.gob.ve)
    @copyright <a href='http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/'>Licencia de Software CENDITEL versión 1.2</a>
    @date 09-06-2018
    """

    template_name = 'evento/suscribir.reporte.html'

    def get_context_data(self, **kwargs):
        """!
        Método que muestra a todos los suscriptores que están en un evento

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/'>Licencia de Software CENDITEL versión 1.2</a>
        @date 09-06-2018
        @param self <b>{object}</b> Objeto que instancia la clase
        @param **kwargs <b>{dict}</b> Diccionario de datos, inicialmente vacio
        @return Retorna un diccionario con los suscriptores inscritos en un evento
        """

        context = super(SuscribirReporteView, self).get_context_data(**kwargs)
        evento_id = kwargs['pk']
        evento = Evento.objects.get(pk=evento_id)
        context['suscriptor'] = Suscriptor.objects.filter(evento=evento)
        return context

class CertificadoListView(ListView):
    """!
    Clase que permite a un usuario listar los certificados que tienen asignados los eventos

    @author William Páez (wpaez at cenditel.gob.ve)
    @copyright <a href='http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/'>Licencia de Software CENDITEL versión 1.2</a>
    @date 09-06-2018
    """

    model = Certificado
    template_name = 'evento/certificado.listar.html'

    def dispatch(self, request, *args, **kwargs):
        """!
        Método que valida si el usuario del sistema tiene permisos para entrar a esta vista

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/'>Licencia de Software CENDITEL versión 1.2</a>
        @date 30-05-2018
        @param self <b>{object}</b> Objeto que instancia la clase
        @param request <b>{object}</b> Objeto que contiene la petición
        @param *args <b>{tupla}</b> Tupla de valores, inicialmente vacia
        @param **kwargs <b>{dict}</b> Diccionario de datos, inicialmente vacio
        @return Redirecciona al usuario a la página de error de permisos en caso de no pertenecer a este nivel
        """

        if self.request.user.perfil.nivel == 1:
            return super(CertificadoListView, self).dispatch(request, *args, **kwargs)
        else:
            return redirect('base:error_403')

    def get_queryset(self):
        """!
        Método que obtiene la lista de certificados que están asociados a los eventos que registró el usuario

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/'>Licencia de Software CENDITEL versión 1.2</a>
        @date 20-06-2018
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Retorna la lista de objetos certificado asociados a los eventos que el usuario registró
        """

        queryset = Certificado.objects.filter(evento__user=self.request.user)
        return queryset

class CertificadoCreateView(CreateView):
    """!
    Clase que permite a un usuario registrar el diseño de los certificados para los eventos

    @author William Páez (wpaez at cenditel.gob.ve)
    @copyright <a href='http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/'>Licencia de Software CENDITEL versión 1.2</a>
    @date 09-06-2018
    """

    model = Certificado
    form_class = CertificadoForm
    template_name = 'evento/certificado.registrar.html'
    success_url = reverse_lazy('evento:certificado_listar')

    def dispatch(self, request, *args, **kwargs):
        """!
        Método que valida si el usuario del sistema tiene permisos para entrar a esta vista

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/'>Licencia de Software CENDITEL versión 1.2</a>
        @date 09-06-2018
        @param self <b>{object}</b> Objeto que instancia la clase
        @param request <b>{object}</b> Objeto que contiene la petición
        @param *args <b>{tupla}</b> Tupla de valores, inicialmente vacia
        @param **kwargs <b>{dict}</b> Diccionario de datos, inicialmente vacio
        @return Redirecciona al usuario a la página de error de permisos en caso de no pertenecer a este nivel
        """

        if self.request.user.perfil.nivel == 1:
            return super(CertificadoCreateView, self).dispatch(request, *args, **kwargs)
        else:
            return redirect('base:error_403')

    def get_form_kwargs(self):
        """!
        Método que permite pasar el usuario actualmente logueado al formulario

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/'>Licencia de Software CENDITEL versión 1.2</a>
        @date 09-06-2018
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Retorna un diccionario con el usuario actualmente logueado
        """

        kwargs = super(CertificadoCreateView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        """!
        Metodo que valida si el formulario es correcto

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/'>Licencia de Software CENDITEL versión 1.2</a>
        @date 09-06-2018
        @param self <b>{object}</b> Objeto que instancia la clase
        @param form <b>{object}</b> Objeto que contiene el formulario de registro
        @return Retorna el formulario validado
        """

        self.object = form.save(commit=False)
        evento = Evento.objects.get(pk=form.cleaned_data['evento'])
        self.object.evento = evento
        self.object.save()

        return super(CertificadoCreateView, self).form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return super(CertificadoCreateView, self).form_invalid(form)

class CertificadoUpdateView(UpdateView):
    """!
    Clase que permite a un usuario actualizar los datos de los certificados

    @author William Páez (wpaez at cenditel.gob.ve)
    @copyright <a href='http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/'>Licencia de Software CENDITEL versión 1.2</a>
    @date 09-06-2018
    """

    model = Certificado
    form_class = CertificadoForm
    template_name = 'evento/certificado.registrar.html'
    success_url = reverse_lazy('evento:certificado_listar')

    def dispatch(self, request, *args, **kwargs):
        """!
        Método que valida si el usuario del sistema tiene permisos para entrar a esta vista

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/'>Licencia de Software CENDITEL versión 1.2</a>
        @date 30-05-2018
        @param self <b>{object}</b> Objeto que instancia la clase
        @param request <b>{object}</b> Objeto que contiene la petición
        @param *args <b>{tupla}</b> Tupla de valores, inicialmente vacia
        @param **kwargs <b>{dict}</b> Diccionario de datos, inicialmente vacio
        @return Redirecciona al usuario a la página de error de permisos si no es su perfil
        """

        certificado = Certificado.objects.filter(pk=self.kwargs['pk'],evento__user__pk=self.request.user.id)

        if certificado and self.request.user.perfil.nivel == 1:
            return super(CertificadoUpdateView, self).dispatch(request, *args, **kwargs)
        else:
            return redirect('base:error_403')

    def get_form_kwargs(self):
        """!
        Método que permite pasar el usuario actualmente logueado al formulario

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/'>Licencia de Software CENDITEL versión 1.2</a>
        @date 09-06-2018
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Retorna un diccionario con el usuario actualmente logueado
        """

        kwargs = super(CertificadoUpdateView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def get_initial(self):
        """!
        Método que agrega valores predeterminados a los campos del formulario

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/'>Licencia de Software CENDITEL versión 1.2</a>
        @date 09-06-2018
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Retorna un diccionario con los valores predeterminados
        """

        datos_iniciales = super(CertificadoUpdateView, self).get_initial()
        #certificado = Certificado.objects.get(pk=self.object.id)
        datos_iniciales['imagen_delantera'] = self.object.imagen_delantera
        datos_iniciales['imagen_tracera'] = self.object.imagen_tracera
        datos_iniciales['coordenada_y_nombre'] = self.object.coordenada_y_nombre
        datos_iniciales['tematica'] = self.object.tematica
        datos_iniciales['evento'] = self.object.evento.id
        return datos_iniciales

class CertificadoDeleteView(DeleteView):
    """!
    Clase que permite a un usuario eliminar los datos de los certificados

    @author William Páez (wpaez at cenditel.gob.ve)
    @copyright <a href='http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/'>Licencia de Software CENDITEL versión 1.2</a>
    @date 09-06-2018
    """

    model = Certificado
    template_name = "evento/certificado.eliminar.html"
    success_url = reverse_lazy('evento:certificado_listar')

    def dispatch(self, request, *args, **kwargs):
        """!
        Método que valida si el usuario del sistema tiene permisos para entrar a esta vista

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/'>Licencia de Software CENDITEL versión 1.2</a>
        @date 08-06-2018
        @param self <b>{object}</b> Objeto que instancia la clase
        @param request <b>{object}</b> Objeto que contiene la petición
        @param *args <b>{tupla}</b> Tupla de valores, inicialmente vacia
        @param **kwargs <b>{dict}</b> Diccionario de datos, inicialmente vacio
        @return Redirecciona al usuario a la página de error de permisos si no es su perfil
        """

        certificado = Certificado.objects.filter(pk=self.kwargs['pk'],evento__user__pk=self.request.user.id)

        if certificado and self.request.user.perfil.nivel == 1:
            return super(CertificadoDeleteView, self).dispatch(request, *args, **kwargs)
        else:
            return redirect('base:error_403')

class CertificadoView(TemplateView):
    """!
    Clase que permite a un usuario otorgar los certificados a los suscriptores que participaron en el evento

    @author William Páez (wpaez at cenditel.gob.ve)
    @copyright <a href='http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/'>Licencia de Software CENDITEL versión 1.2</a>
    @date 09-06-2018
    """

    template_name = 'evento/certificado.html'

    def dispatch(self, request, *args, **kwargs):
        """!
        Método que valida si el usuario del sistema tiene permisos para entrar a esta vista

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/'>Licencia de Software CENDITEL versión 1.2</a>
        @date 09-06-2018
        @param self <b>{object}</b> Objeto que instancia la clase
        @param request <b>{object}</b> Objeto que contiene la petición
        @param *args <b>{tupla}</b> Tupla de valores, inicialmente vacia
        @param **kwargs <b>{dict}</b> Diccionario de datos, inicialmente vacio
        @return Redirecciona al usuario a la página de error de permisos en caso de no pertenecer a este nivel
        """

        evento = Evento.objects.filter(pk=self.kwargs['pk'],user=self.request.user)
        if evento and self.request.user.perfil.nivel == 1:
            return super(CertificadoView, self).dispatch(request, *args, **kwargs)
        else:
            return redirect('base:error_403')

    def get_context_data(self, **kwargs):
        """!
        Método que muestra a todos los suscriptores para otorgarles certificados

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/'>Licencia de Software CENDITEL versión 1.2</a>
        @date 09-06-2018
        @param self <b>{object}</b> Objeto que instancia la clase
        @param **kwargs <b>{dict}</b> Diccionario de datos, inicialmente vacio
        @return Retorna un diccionario con los suscriptores
        """

        context = super(CertificadoView, self).get_context_data(**kwargs)
        evento_id = kwargs['pk']
        evento = Evento.objects.get(pk=evento_id)
        context['suscriptor'] = Suscriptor.objects.filter(evento=evento)
        return context

class SuscriptorUpdateView(UpdateView):
    """!
    Clase que permite a un usuario cambiar el estado del certificado

    @author William Páez (wpaez at cenditel.gob.ve)
    @copyright <a href='http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/'>Licencia de Software CENDITEL versión 1.2</a>
    @date 09-06-2018
    """

    model = Suscriptor
    form_class = SuscriptorForm
    template_name = 'evento/suscriptor.actualizar.html'
    success_url = reverse_lazy('evento:certificado_listar')

    def dispatch(self, request, *args, **kwargs):
        """!
        Método que valida si el usuario del sistema tiene permisos para entrar a esta vista

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/'>Licencia de Software CENDITEL versión 1.2</a>
        @date 09-06-2018
        @param self <b>{object}</b> Objeto que instancia la clase
        @param request <b>{object}</b> Objeto que contiene la petición
        @param *args <b>{tupla}</b> Tupla de valores, inicialmente vacia
        @param **kwargs <b>{dict}</b> Diccionario de datos, inicialmente vacio
        @return Redirecciona al usuario a la página de error de permisos si no es su perfil
        """

        evento = Evento.objects.filter(user__pk=self.request.user.id)
        if evento and self.request.user.perfil.nivel == 1:
            return super(SuscriptorUpdateView, self).dispatch(request, *args, **kwargs)
        else:
            return redirect('base:error_403')

    def get_initial(self):
        """!
        Método que agrega valores predeterminados a los campos del formulario

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/'>Licencia de Software CENDITEL versión 1.2</a>
        @date 09-06-2018
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Retorna un diccionario con los valores predeterminados
        """

        datos_iniciales = super(SuscriptorUpdateView, self).get_initial()
        #certificado = Certificado.objects.get(pk=self.object.id)
        datos_iniciales['otorgar'] = self.object.otorgar
        datos_iniciales['evento'] = self.object.evento
        datos_iniciales['perfil'] = self.object.perfil
        return datos_iniciales

class CertificadoDescargarView(View):
    """!
    Clase que permite a un usuario descargar el certificado que tiene asociado a un evento

    @author Alexander Olivares (olivaresa at cantv.net)
    @author William Páez (wpaez at cenditel.gob.ve)
    @copyright <a href='http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/'>Licencia de Software CENDITEL versión 1.2</a>
    @date 09-06-2018
    """

    def dispatch(self, request, *args, **kwargs):
        """!
        Método que valida si el usuario del sistema tiene permisos para entrar a esta vista

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/'>Licencia de Software CENDITEL versión 1.2</a>
        @date 09-06-2018
        @param self <b>{object}</b> Objeto que instancia la clase
        @param request <b>{object}</b> Objeto que contiene la petición
        @param *args <b>{tupla}</b> Tupla de valores, inicialmente vacia
        @param **kwargs <b>{dict}</b> Diccionario de datos, inicialmente vacio
        @return Redirecciona al usuario a la página de error de permisos en caso de no pertenecer a este nivel
        """

        suscriptor = Suscriptor.objects.get(evento=self.kwargs['evento'],perfil=self.request.user.perfil)
        if suscriptor.otorgar:
            return super(CertificadoDescargarView, self).dispatch(request, *args, **kwargs)
        else:
            return redirect('base:error_403')

    def get(self, request, *args, **kwargs):
        """!
        Método que construye el certificado con los datos del usuario

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/'>Licencia de Software CENDITEL versión 1.2</a>
        @date 20-06-2018
        @param self <b>{object}</b> Objeto que instancia la clase
        @param request <b>{object}</b> Objeto que contiene la petición
        @param *args <b>{tupla}</b> Tupla de valores, inicialmente vacia
        @param **kwargs <b>{dict}</b> Diccionario de datos, inicialmente vacio
        @return Retorna el certificado del usuario en un pdf
        """

        response = HttpResponse(content_type='application/pdf')
        if Suscriptor.objects.filter(evento=kwargs['evento'],perfil=self.request.user.perfil):
            suscriptor = Suscriptor.objects.get(evento=kwargs['evento'],perfil=self.request.user.perfil)
            imagen_delantera = suscriptor.evento.certificado.imagen_delantera.path
            #print(imagen_delantera)

            if suscriptor.evento.certificado.imagen_tracera:
                imagen_tracera = suscriptor.evento.certificado.imagen_tracera.path
                #print(imagen_tracera)
            else:
                imagen_tracera = None

            ancho_certificado = suscriptor.evento.certificado.imagen_delantera.width / 2
            #print('ancho certificado: ' + str(ancho_certificado))

            nombre_temp = suscriptor.perfil.user.first_name + suscriptor.perfil.user.last_name
            if len(nombre_temp) <= 18:
                ancho_nombre = (len(nombre_temp) * 22) / 2
            else:
                ancho_nombre = (len(nombre_temp) * 14) / 2
            #print('ancho nombre: ' + str(ancho_nombre))

            coordenada_x_nombre = ancho_certificado - ancho_nombre
            #print(coordenada_x_nombre)

            coordenada_nombre = coordenada_x_nombre, suscriptor.evento.certificado.coordenada_y_nombre
            #print(coordenada_nombre)

            u = suscriptor.perfil.user.username[0] + '-' + suscriptor.perfil.user.username[1:3] + '.' + suscriptor.perfil.user.username[3:6] + '.' + suscriptor.perfil.user.username[6:]
            username = 'C.I.: %s' % u
            #print(len(username))

            ancho_username = (len(username) * 14) / 2
            #print(ancho_username)

            coordenada_x_username = ancho_certificado - ancho_username
            #print(coordenada_x_username)

            coordenada_username = coordenada_x_username, suscriptor.evento.certificado.coordenada_y_nombre - 40
            #print(coordenada_username)

            ancho_rol = (len(NIVEL[suscriptor.perfil.nivel][1]) * 14) / 2
            print(ancho_rol)
            coordenada_x_rol = ancho_certificado - ancho_rol
            coordenada_rol = coordenada_x_rol, suscriptor.evento.certificado.coordenada_y_nombre - 70
            rol =  NIVEL[suscriptor.perfil.nivel][1]

            tematica = suscriptor.evento.certificado.tematica

            pdfmetrics.registerFont(TTFont('Roboto-Regular','static/css/font/Roboto/Roboto-Regular.ttf'))
            addMapping('Roboto-Regular', 0, 0, 'Roboto-Regular')
            buffer = BytesIO()
            pdf = canvas.Canvas(buffer, landscape(letter), bottomup=50)
            img_delantera = Image.open(imagen_delantera)
            draw = ImageDraw.Draw(img_delantera)
            pdf.setTitle('%s-%s' % (suscriptor.perfil.user.username, suscriptor.evento.id))
            pdf.setAuthor('Sofi')
            #pdf.setSubject('')
            pdf.setCreator('CENDITEL')
            pdf.drawInlineImage(img_delantera,0,0)
            pdf.setFillColorRGB(0,0,0)
            pdf.setFont('Roboto-Regular', 30)
            pdf.drawString(coordenada_nombre[0],coordenada_nombre[1], suscriptor.perfil.user.first_name + ' ' + suscriptor.perfil.user.last_name)
            pdf.setFont('Roboto-Regular', 25)
            pdf.drawString(coordenada_username[0],coordenada_username[1], username)

            pdf.setFont('Roboto-Regular', 20)
            pdf.drawString(coordenada_rol[0],coordenada_rol[1], rol)

            pdf.showPage()

            if imagen_tracera:
                img_tracera = Image.open(imagen_tracera)
                draw = ImageDraw.Draw(img_tracera)
                pdf.drawInlineImage(img_tracera,0,0)
                tematica_pdf = pdf.beginText(50,562)
                tematica_pdf.textLines(tematica.splitlines())
                pdf.drawText(tematica_pdf)
                pdf.showPage()

            pdf.save()
            pdf = buffer.getvalue()
            buffer.close()
            response['Content-Disposition'] = 'attachment; filename=%s-%s.pdf' % (suscriptor.perfil.user.username, suscriptor.evento.id)
            response.write(pdf)
        return response
