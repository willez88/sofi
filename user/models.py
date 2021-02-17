from base.constant import YESNO
from base.models import Location
from django.contrib.auth.models import User
from django.db import models
from event.models import Event


class Profile(models.Model):
    """!
    Clase que contiene los datos del perfil de un usuario del sistema

    @author Alexander Olivares <olivaresa@cantv.net>
    @author William Páez <wpaez@cenditel.gob.ve>
    @copyright <a href='https://tinyurl.com/y3tfnema'>
        Licencia de Software CENDITEL versión 1.2</a>
    """

    # Teléfono del usuario
    phone = models.CharField('teléfono', max_length=15)

    # Profesión del usuario
    profession = models.CharField('profesión', max_length=100)

    # Organización al que el usuario pertenece
    organization = models.CharField('organización', max_length=100, blank=True)

    # Cuenta facebook del usuario
    twitter_account = models.CharField(
        'cuenta de twitter', max_length=100, blank=True
    )

    # Cuenta twitter del usuario
    facebook_account = models.CharField(
        'cuenta de facebook', max_length=100, blank=True
    )

    # Establece la relación entre la ubicación geográfica y el perfil
    location = models.OneToOneField(
        Location, on_delete=models.CASCADE, verbose_name='ubicación'
    )

    # Establece la relación entre el usuario del sistema con el perfil
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name='usuario'
    )

    def __str__(self):
        """!
        Función para representar la clase de forma amigable

        @author William Páez <wpaez@cenditel.gob.ve>
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Una cadena de caracteres con el nombre y apellido del usuario
        """

        return '%s %s' % (self.user.first_name, self.user.last_name)

    class Meta:
        """!
        Meta clase del modelo que establece algunas propiedades

        @author William Páez <wpaez@cenditel.gob.ve>
        """

        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfiles'


class Subscriber(models.Model):
    """!
    Clase que relaciona a los suscriptores con los eventos

    @author Alexander Olivares <olivaresa@cantv.net>
    @author William Páez <wpaez@cenditel.gob.ve>
    """

    grant = models.BooleanField('otorgar', choices=YESNO)

    # Establece la relación entre el suscriptor y el evento
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, verbose_name='evento'
    )

    # Establece la relación entre el suscriptor y el usuario del sistema
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, verbose_name='perfil'
    )

    def __str__(self):
        """!
        Método para representar la clase de forma amigable

        @author William Páez <wpaez@cenditel.gob.ve>
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Devuelve una cadena de caracteres con el nombre del evento y el
            nombre de usuario
        """

        return '%s, %s' % (self.event.name, self.profile.user.username)

    class Meta:
        """!
        Meta clase del modelo que establece algunas propiedades

        @author William Páez <wpaez@cenditel.gob.ve>
        """

        verbose_name = 'Suscriptor'
        verbose_name_plural = 'Suscriptores'
