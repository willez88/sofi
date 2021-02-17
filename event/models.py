from base.constant import YESNO
from base.models import Location
from django.contrib.auth.models import User
from django.db import models


class Event(models.Model):
    """!
    Clase que contiene los datos de un evento

    @author Alexander Olivares <olivaresa@cantv.net>
    @author William Páez <wpaez@cenditel.gob.ve>
    @copyright <a href='https://tinyurl.com/y3tfnema'>
        Licencia de Software CENDITEL versión 1.2</a>
    """

    # Nombre del evento
    name = models.CharField('nombre', max_length=150)

    # Breve descripción del evento
    summary = models.TextField('resumen', blank=True)

    # Correo del evento
    email = models.EmailField('correo', unique=True)

    # Logo del evento
    logo = models.ImageField('logo', upload_to='event/', blank=True)

    # Video sobre el tema del evento
    video = models.URLField('vídeo', blank=True)

    # Cuenta Twitter del evento
    twitter_account = models.CharField(
        'cuenta de twitter', max_length=50, blank=True
    )

    # Clave de la cuenta del twitter
    # password_twitter = models.CharField(max_length=12, blank=True)

    # Cuenta Facebook del evento
    facebook_account = models.CharField(
        'cuenta de facebook', max_length=50, blank=True
    )

    # clave de la cuenta del Facebook
    # password_facebook = models.CharField(max_length=12, blank=True)

    # Permitir mostrar las presentaciones
    presentation = models.BooleanField('presentación', choices=YESNO)

    # Permitir que los usuarios se suscriban al evento
    subscription = models.BooleanField('suscripción', choices=YESNO)

    # Permitir que el evento sea visible para todos los usuario
    publication = models.BooleanField('publicación', choices=YESNO)

    # Permitir a los usuarios dejar comentarios sobre el evento
    commentary = models.BooleanField('comentario', choices=YESNO)

    # Fecha del evento
    time = models.TimeField('Hora')

    # Fecha inicial del evento
    start_date = models.DateField('fecha inicial')

    # Fecha final del evento
    end_date = models.DateField('fecha final')

    # Establece la relación entre la ubicación geográfica y el evento
    location = models.OneToOneField(
        Location, on_delete=models.CASCADE, verbose_name='ubicación'
    )

    # Establece la relación entre usuario del sistema con el evento
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='usuario'
    )

    def __str__(self):
        """!
        Método para representar la clase de forma amigable

        @author William Páez <wpaez@cenditel.gob.ve>
        @copyright <a href='https://tinyurl.com/y3tfnema'>
            Licencia de Software CENDITEL versión 1.2</a>
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Una cadena de caracteres con el nombre del evento
        """

        return self.name

    class Meta:
        """!
        Meta clase del modelo que establece algunas propiedades

        @author William Páez <wpaez@cenditel.gob.ve>
        @copyright <a href='https://tinyurl.com/y3tfnema'>
            Licencia de Software CENDITEL versión 1.2</a>
        """

        verbose_name = 'Evento'
        verbose_name_plural = 'Eventos'


class Certificate(models.Model):
    """!
    Clase que contiene los datos de un certificado que se genera para algún
    usuario cuando es otorgado

    @author Alexander Olivares <olivaresa@cantv.net>
    @author William Páez <wpaez@cenditel.gob.ve>
    @copyright <a href='https://tinyurl.com/y3tfnema'>
        Licencia de Software CENDITEL versión 1.2</a>
    """

    # Imagen delantera del certificado
    front_image = models.ImageField(
        'imagen delantera', upload_to='certificate/'
    )

    # Imagen tracera del certificado
    back_image = models.ImageField('imagen tracera', upload_to='certificate/')

    # encuesta = models.BooleanField(choices=SINO)

    # Coordenada en el eje Y del nombre del suscriptor
    coordinate_y_name = models.IntegerField('coordenada y del nombre')

    # Temática del evento
    thematic = models.TextField('temática')

    # Establece la relación del certificado con el evento
    event = models.OneToOneField(
        Event, on_delete=models.CASCADE, verbose_name='evento'
    )

    def __str__(self):
        """!
        Método para representar la clase de forma amigable

        @author William Páez <wpaez@cenditel.gob.ve>
        @copyright <a href='https://tinyurl.com/y3tfnema'>
            Licencia de Software CENDITEL versión 1.2</a>
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Una cadena de caracteres con el id del certificado y el nombre
            del evento
        """

        return str(self.id) + ' | ' + str(self.event)

    class Meta:
        """!
        Meta clase del modelo que establece algunas propiedades

        @author William Páez <wpaez@cenditel.gob.ve>
        @copyright <a href='https://tinyurl.com/y3tfnema'>
            Licencia de Software CENDITEL versión 1.2</a>
        """

        verbose_name = 'Certificado'
        verbose_name_plural = 'Certificados'
