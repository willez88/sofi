from base.constant import YESNO
from base.forms import LocationForm
from django import forms

from .models import Certificate, Event


class EventForm(forms.ModelForm, LocationForm):
    """!
    Clase que contiene los campos del formulario del evento

    @author William Páez <wpaez@cenditel.gob.ve>
    @copyright <a href='https://tinyurl.com/y3tfnema'>
        Licencia de Software CENDITEL versión 1.2</a>
    """

    # Nombre del evento
    name = forms.CharField(
        label='Nombre:', max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control input-sm', 'data-toggle': 'tooltip',
                'title': 'Indique el nombre del evento',
            }
        )
    )

    # Resumen del evento
    summary = forms.CharField(
        label='Resumen:', max_length=100,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control input-sm', 'data-toggle': 'tooltip',
                'cols': '40', 'rows': '10',
                'title': 'Indique el resumen del evento',
            }
        )
    )

    # Correo del evento
    email = forms.EmailField(
        label='Correo Electrónico:', max_length=100,
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control input-sm email-mask',
                'data-toggle': 'tooltip',
                'title': 'Indique el correo electrónico del evento'
            }
        )
    )

    # Logo que representa al evento
    logo = forms.ImageField(required=False)

    # Url del vídeo del evento
    video = forms.URLField(
        label='Video de Presentación:', max_length=100,
        widget=forms.URLInput(
            attrs={
                'class': 'form-control input-sm', 'data-toggle': 'tooltip',
                'title': 'Indique la url de la presentación'
            }
        ), required=False
    )

    # Cuenta twitter del evento
    twitter_account = forms.CharField(
        label='Cuenta Twitter:', max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control input-sm', 'data-toggle': 'tooltip',
                'title': 'Indique la cuenta twitter del evento',
            }
        ), required=False
    )

    # Cuenta facebook del evento
    facebook_account = forms.CharField(
        label='Cuenta Facebook:', max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control input-sm', 'data-toggle': 'tooltip',
                'title': 'Indique la cuenta facebook del evento',
            }
        ), required=False
    )

    # Permitir presentaciones en el evento
    presentation = forms.ChoiceField(
        label='¿Permitir Presentaciones?',
        choices=YESNO,
        widget=forms.Select(
            attrs={
                'class': 'form-control select2', 'data-toggle': 'tooltip',
                'title': 'Seleccione la opción correcta',
            }
        ),
    )

    # Permitir que los usuarios se suscriban a los eventos
    subscription = forms.ChoiceField(
        label='¿Permitir Suscripciones?',
        choices=YESNO,
        widget=forms.Select(
            attrs={
                'class': 'form-control select2', 'data-toggle': 'tooltip',
                'title': 'Seleccione la opción correcta',
            }
        ),
    )

    # Permitir que los usuarios se suscriban a los eventos
    publication = forms.ChoiceField(
        label='¿Permitir Publicación?',
        choices=YESNO,
        widget=forms.Select(
            attrs={
                'class': 'form-control select2', 'data-toggle': 'tooltip',
                'title': 'Seleccione la opción correcta',
            }
        ),
    )

    # Permitir que los usuarios hagan comentarios del evento
    commentary = forms.ChoiceField(
        label='¿Permitir Comentarios?',
        choices=YESNO,
        widget=forms.Select(
            attrs={
                'class': 'form-control select2', 'data-toggle': 'tooltip',
                'title': 'Seleccione la opción correcta',
            }
        ),
    )

    # Fecha del evento
    time = forms.CharField(
        label='Hora:',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control input-sm',
                'title': 'Seleccione la hora que se realiza el evento',
            }
        ), help_text='Formato militar: hh:mm'
    )

    # Fecha de inicio del evento
    start_date = forms.DateField(
        label='Fecha Inicial:',
        widget=forms.DateInput(
            format='%Y-%m-%d',
            attrs={
                'class': 'form-control input-sm datepicker',
                'readonly': 'true',
                'title': 'Seleccione la fecha inicial del evento',
            }
        )
    )

    # Fecha de inicio del evento
    end_date = forms.DateField(
        label='Fecha Final:',
        widget=forms.DateInput(
            format='%Y-%m-%d',
            attrs={
                'class': 'form-control input-sm datepicker',
                'readonly': 'true',
                'title': 'Seleccione la fecha final del evento',
            }
        )
    )

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        if start_date > end_date:
            # print('hola entra')
            self.add_error('start_date', 'La fecha inicial del evento no puede\
                ser mayor que la final.')

    class Meta:
        """!
        Meta clase del formulario que establece algunas propiedades

        @author William Páez <wpaez@cenditel.gob.ve>
        @copyright <a href='https://tinyurl.com/y3tfnema'>
            Licencia de Software CENDITEL versión 1.2</a>
        """

        model = Event
        fields = [
            'name', 'summary', 'email', 'logo', 'video', 'twitter_account',
            'facebook_account', 'presentation', 'subscription', 'publication',
            'commentary', 'time', 'start_date', 'end_date'
        ]


class CertificateForm(forms.ModelForm):
    """!
    Clase que contiene los campos del formulario del evento

    @author William Páez <wpaez@cenditel.gob.ve>
    @copyright <a href='https://tinyurl.com/y3tfnema'>
        Licencia de Software CENDITEL versión 1.2</a>
    """

    def __init__(self, *args, **kwargs):
        """!
        Método que permite inicializar el campo evento con la lista de eventos
        que el usuario ha registrado

        @author William Páez <wpaez@cenditel.gob.ve>
        @copyright <a href='https://tinyurl.com/y3tfnema'>
            Licencia de Software CENDITEL versión 1.2</a>
        @param self <b>{object}</b> Objeto que instancia la clase
        @param *args <b>{tupla}</b> Tupla de valores, inicialmente vacia
        @param *kwargs <b>{dict}</b> Diccionario de datos, inicialmente vacio
        @return Retorna el formulario con una configuración inicializada
            de forma manual
        """

        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

        event_list = [('', 'Selecione...')]
        for el in Event.objects.filter(user=user):
            event_list.append((el.id, el))
        self.fields['event'].choices = event_list

    # Imagen delantera del cetificado
    front_image = forms.ImageField(
        label='Imagen Delantera:',
        help_text='Tamaño recomendado: 800x664 pixeles.'
    )

    # Imagen tracera del certificado
    back_image = forms.ImageField(
        label='Imagen Tracera:', required=False,
        help_text='Tamaño recomendado: 800x664 pixeles.'
    )

    # Coordenada Y para posicionar el nombre del suscriptor
    coordinate_y_name = forms.CharField(
        label='Coordenada Y del Nombre:',
        widget=forms.NumberInput(attrs={
            'class': 'form-control input-md', 'data-toggle': 'tooltip',
            'title': 'Indique la coordenada Y para posicionar el nombre \
                del suscriptor',
            'min': '0', 'step': '1', 'value': '0',
        }),
        help_text='Indica que tan arriba o abajo se muestran los datos del \
            usuario. Valor recomendado: 435 pixeles.'
    )

    # Temática del evento
    thematic = forms.CharField(
        label='Temática:', max_length=100,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control input-sm', 'data-toggle': 'tooltip',
                'cols': '40', 'rows': '10',
                'title': 'Indique la temática que tiene el evento',
            }
        ), required=False
    )

    # Contiene los eventos que el usuario ha registrado
    event = forms.ChoiceField(
        label='Evento:',
        widget=forms.Select(
            attrs={
                'class': 'form-control select2', 'data-toggle': 'tooltip',
                'title': 'Seleccione el evento',
            }
        )
    )

    class Meta:
        """!
        Meta clase del formulario que establece algunas propiedades

        @author William Páez <wpaez@cenditel.gob.ve>
        @copyright <a href='https://tinyurl.com/y3tfnema'>
            Licencia de Software CENDITEL versión 1.2</a>
        """

        model = Certificate
        fields = [
            'front_image', 'back_image', 'coordinate_y_name', 'thematic',
        ]
