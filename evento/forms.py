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
## @namespace evento.forms
#
# Contiene las clases, atributos y métodos para los formularios a implementar en el módulo de eventos
# @author William Páez (wpaez at cenditel.gob.ve)
# @author <a href='http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/'>Licencia de Software CENDITEL versión 1.2</a>
# @date 30-05-2018
# @version 2.0

from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from .models import Evento
from base.constant import SINO

class EventoForm(forms.ModelForm):
    """!
    Clase que contiene los campos del formulario del evento

    @author William Páez (wpaez at cenditel.gob.ve)
    @copyright <a href='http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/'>Licencia de Software CENDITEL versión 1.2</a>
    @date 30-05-2018
    """

    ## Nombre del evento
    nombre = forms.CharField(
        label=_("Nombre:"), max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control input-sm', 'data-toggle': 'tooltip',
                'title': _("Indique el nombre del evento"),
            }
        )
    )

    ## Resumen del evento
    resumen = forms.CharField(
        label=_("Resumen:"), max_length=100,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control input-sm', 'data-toggle': 'tooltip', 'cols': '40', 'rows': '10',
                'title': _("Indique el resumen del evento"),
            }
        )
    )

    ## Lugar donde se realiza el evento
    lugar = forms.CharField(
        label=_("Lugar:"), max_length=100,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control input-sm', 'data-toggle': 'tooltip', 'cols': '40', 'rows': '10',
                'title': _("Indique el lugar donde se realiza el evento"),
            }
        )
    )

    ## Correo del evento
    correo = forms.EmailField(
        label=_("Correo Electrónico:"), max_length=100,
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control input-sm email-mask', 'data-toggle': 'tooltip', 'data-rule-required': 'true',
                'title': _("Indique el correo electrónico del evento")
            }
        )
    )

    ## Cuenta twitter del evento
    cuenta_twitter = forms.CharField(
        label=_("Cuenta Twitter:"), max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control input-sm', 'data-toggle': 'tooltip',
                'title': _("Indique la cuenta twitter del evento"),
            }
        )
    )

    ## Cuenta facebook del evento
    cuenta_facebook = forms.CharField(
        label=_("Cuenta Facebook:"), max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control input-sm', 'data-toggle': 'tooltip',
                'title': _("Indique la cuenta facebook del evento"),
            }
        )
    )

    ## Permitir presentaciones en el evento
    presentacion = forms.ChoiceField(
        label= _("¿Permitir Presentaciones?"),
        choices= SINO,
        widget=forms.Select(
            attrs={
                'class': 'form-control select2', 'data-toggle': 'tooltip',
                'title': _("Seleccione la opción correcta"),
            }
        ),
    )

    ## Permitir que los usuarios se suscriban a los eventos
    suscripcion = forms.ChoiceField(
        label= _("¿Permitir Suscripciones?"),
        choices= SINO,
        widget=forms.Select(
            attrs={
                'class': 'form-control select2', 'data-toggle': 'tooltip',
                'title': _("Seleccione la opción correcta"),
            }
        ),
    )

    ## Permitir que los usuarios se suscriban a los eventos
    publicacion = forms.ChoiceField(
        label= _("¿Permitir Publicación?"),
        choices= SINO,
        widget=forms.Select(
            attrs={
                'class': 'form-control select2', 'data-toggle': 'tooltip',
                'title': _("Seleccione la opción correcta"),
            }
        ),
    )

    ## Permitir que los usuarios hagan comentarios del evento
    comentario = forms.ChoiceField(
        label= _("¿Permitir Comentarios?"),
        choices= SINO,
        widget=forms.Select(
            attrs={
                'class': 'form-control select2', 'data-toggle': 'tooltip',
                'title': _("Seleccione la opción correcta"),
            }
        ),
    )

    ## Fecha del evento
    fecha = forms.CharField(
        label=_("Fecha:"),
        widget=forms.TextInput(
            attrs={
                'class': 'form-control input-sm datepicker','readonly':'true',
                'title': _("Seleccione la fecha que se realiza el evento"),
            }
        )
    )

    ## Fecha de inicio del evento
    fecha_inicial = forms.CharField(
        label=_("Fecha Inicial:"),
        widget=forms.TextInput(
            attrs={
                'class': 'form-control input-sm datepicker','readonly':'true',
                'title': _("Seleccione la fecha inicial del evento"),
            }
        )
    )

    ## Fecha de inicio del evento
    fecha_final = forms.CharField(
        label=_("Fecha Final:"),
        widget=forms.TextInput(
            attrs={
                'class': 'form-control input-sm datepicker','readonly':'true',
                'title': _("Seleccione la fecha final del evento"),
            }
        )
    )

    logo = forms.ImageField()

    def clean_email(self):
        """!
        Método que permite validar si el correo del evento ya esta registrado en el sistema

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/'>Licencia de Software CENDITEL versión 1.2</a>
        @date 30-05-2018
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Devuelve un mensaje de error en caso de que el correo ya esté registrado en el sistema
        """

        email = self.cleaned_data['email']
        if Evento.objects.filter(email=email):
            raise forms.ValidationError(_("El correo ya esta registrado"))
        return email

    class Meta:
        """!
        Meta clase del formulario que establece algunas propiedades

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/'>Licencia de Software CENDITEL versión 1.2</a>
        @date 30-05-2018
        """

        model = Evento
        exclude = ['user',]
