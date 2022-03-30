from base.constant import YESNO
from base.fields import IdentificationCardField
from base.forms import LocationForm
from captcha.fields import CaptchaField, CaptchaTextInput
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core import validators

from .models import Subscriber


class ProfileForm(forms.ModelForm, LocationForm):
    """!
    @author William Páez <paez.william8@gmail.com>
    @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>
        GNU Public License versión 2 (GPLv2)</a>
    """

    # Username para identificar al usuario con su cédula
    username = IdentificationCardField(
        validators=[
            validators.RegexValidator(
                r'^[VE][\d]{8}$',
                'Introduzca un número de cédula válido. Solo se permiten \
                    números y una longitud de 8 carácteres. Se agregan ceros \
                    (0) si la longitud es de 7 o menos caracteres.'
            ),
        ], help_text='V00000000 ó E00000000'
    )

    # Nombres del usuario
    first_name = forms.CharField(
        label='Nombres:', max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control input-sm', 'data-toggle': 'tooltip',
                'title': 'Indique los Nombres',
            }
        )
    )

    # Apellidos del usuario
    last_name = forms.CharField(
        label='Apellidos:', max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control input-sm', 'data-toggle': 'tooltip',
                'title': 'Indique los Apellidos',
            }
        )
    )

    # Correo del usuario
    email = forms.EmailField(
        label='Correo Electrónico:', max_length=100,
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control input-sm email-mask',
                'data-toggle': 'tooltip', 'data-rule-required': 'true',
                'title': 'Indique el correo electrónico de contacto'
            }
        )
    )

    # Teléfono del usuario
    phone = forms.CharField(
        label='Teléfono:',
        max_length=15,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control input-sm', 'data-toggle': 'tooltip',
                'title': 'Indique el número telefónico de contacto',
                'data-mask': '+00-000-0000000'
            }
        ),
        validators=[
            validators.RegexValidator(
                r'^\+\d{2}-\d{3}-\d{7}$',
                'Número telefónico inválido. Solo se permiten números \
                    y los símbolos: + -'
            ),
        ],
        help_text='+58-416-0000000'
    )

    # Profesión del usuario
    profession = forms.CharField(
        label='Profesión:', max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control input-sm', 'data-toggle': 'tooltip',
                'title': 'Indique la profesión',
            }
        ), required=False
    )

    # Organización que pertenece el usuario
    organization = forms.CharField(
        label='Organización:', max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control input-sm', 'data-toggle': 'tooltip',
                'title': 'Indique la organización',
            }
        ), required=False
    )

    # Cuenta de twitter del usuario
    twitter_account = forms.CharField(
        label='Cuenta de Twitter:', max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control input-sm', 'data-toggle': 'tooltip',
                'title': 'Indique la cuenta de twitter',
            }
        ), required=False
    )

    # Cuenta de facebook del usuario
    facebook_account = forms.CharField(
        label='Cuenta de Facebook:', max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control input-sm', 'data-toggle': 'tooltip',
                'title': 'Indique la cuenta de facebook',
            }
        ), required=False
    )

    # Clave de acceso del usuario
    password = forms.CharField(
        label='Contraseña:', max_length=128,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control input-sm', 'data-toggle': 'tooltip',
                'title': 'Indique una contraseña de aceso al sistema'
            }
        )
    )

    # Confirmación de clave de acceso del usuario
    confirm_password = forms.CharField(
        label='Confirmar Contraseña:', max_length=128,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control input-sm', 'data-toggle': 'tooltip',
                'title': 'Indique nuevamente la contraseña de aceso al sistema'
            }
        )
    )

    # Campo de validación de captcha
    captcha = CaptchaField(
        label='Captcha:', widget=CaptchaTextInput(attrs={
            'class': 'form-control input-sm',
            'placeholder': 'texto de la imagen',
            'data-toggle': 'tooltip',
            'title': 'Indique el texto de la imagen'
        })
    )

    def clean_email(self):
        """!
        Función que permite validar si el correo del usuario ya esta registrado
        en el sistema

        @author William Páez <paez.william8@gmail.com>
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Mensaje de error en caso de que el correo ya esté registrado
            en el sistema
        """

        email = self.cleaned_data['email']
        if User.objects.filter(email=email):
            raise forms.ValidationError('El correo ya esta registrado')
        return email

    def clean_confirm_password(self):
        """!
        Función que permite validar si ambas contraseñas son iguales

        @author William Páez <paez.william8@gmail.com>
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Mensaje de error en caso de que las contraseñas sean distintas
        """

        confirm_password = self.cleaned_data['confirm_password']
        password = self.cleaned_data.get('password')
        if password != confirm_password:
            raise forms.ValidationError('La contraseña no es la misma')

        return confirm_password

    class Meta:
        """!
        Meta clase del formulario que establece algunas propiedades

        @author William Páez <paez.william8@gmail.com>
        """

        model = User
        fields = [
            'username', 'first_name', 'last_name', 'email', 'phone',
            'profession', 'organization', 'twitter_account',
            'facebook_account', 'password', 'confirm_password', 'captcha'
        ]


class ProfileUpdateForm(ProfileForm):
    """!
    Clase que contiene los campos del formulario de perfil del usuario para
    actualizar los datos

    @author William Páez <paez.william8@gmail.com>
    @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>
        GNU Public License versión 2 (GPLv2)</a>
    """

    def __init__(self, *args, **kwargs):
        """!
        Función que inicializa la clase del formulario para actualizar los
        datos

        @author William Páez <paez.william8@gmail.com>
        @param self <b>{object}</b> Objeto que instancia la clase
        @param *args <b>{tupla}</b> Tupla de valores, inicialmente vacia
        @param *kwargs <b>{dict}</b> Diccionario de datos, inicialmente vacio
        """

        super().__init__(*args, **kwargs)
        self.fields['password'].required = False
        self.fields['confirm_password'].required = False
        self.fields['password'].widget.attrs['disabled'] = True
        self.fields['confirm_password'].widget.attrs['disabled'] = True

    def clean_email(self):
        """!
        función que permite validar el campo de correo electronico

        @author William Páez <paez.william8@gmail.com>
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Mensaje de error en caso de que el correo electronico ya se
            encuentre registrado
        """

        email = self.cleaned_data['email']
        username = self.cleaned_data.get('username')
        if User.objects.filter(email=email).exclude(username=username):
            raise forms.ValidationError('El correo ya esta registrado')
        return email

    class Meta:
        """!
        Meta clase del formulario que establece algunas propiedades

        @author William Páez <paez.william8@gmail.com>
        """

        model = User
        fields = [
            'username', 'first_name', 'last_name', 'email', 'phone',
            'profession', 'organization', 'twitter_account',
            'facebook_account', 'captcha'
        ]


class LoginForm(forms.Form):
    """!
    Clase que autentica usuarios en el sistema.

    @author William Páez <paez.william8@gmail.com>
    @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>
        GNU Public License versión 2 (GPLv2)</a>
    """

    # Username para identificar al usuario con su cédula
    username = IdentificationCardField(
        validators=[
            validators.RegexValidator(
                r'^[VE][\d]{8}$',
                'Introduzca un número de cédula válido. Solo se permiten \
                    números y una longitud de 8 carácteres. Se agregan ceros \
                    (0) si la longitud es de 7 o menos caracteres.'
            ),
        ], help_text='V00000000 ó E00000000'
    )

    # Clave de acceso del usuario
    password = forms.CharField(
        label='Contraseña:', max_length=128,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control input-sm', 'data-toggle': 'tooltip',
                'title': 'Indique una contraseña de aceso al sistema'
            }
        )
    )

    # Campo de validación de captcha
    captcha = CaptchaField(
        label='Captcha:', widget=CaptchaTextInput(attrs={
            'class': 'form-control input-sm',
            'placeholder': 'texto de la imagen',
            'data-toggle': 'tooltip', 'title': 'Indique el texto de la imagen'
        })
    )

    def clean(self):
        """!
        Método que valida si el usuario a autenticar es correcto

        @author William Páez <paez.william8@gmail.com>
        """

        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        user = authenticate(username=username, password=password)
        if(not user):
            msg = 'Verifique su usuario o contraseña'
            self.add_error('username', msg)

    class Meta:
        """!
        Meta clase del formulario que establece algunas propiedades

        @author William Páez <paez.william8@gmail.com>
        """

        fields = '__all__'


class SubscriberForm(forms.ModelForm):
    """!
    Clase que contiene los datos de las suscipciones de los usuarios a los
    eventos

    @author William Páez <paez.william8@gmail.com>
    @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>
        GNU Public License versión 2 (GPLv2)</a>
    """

    # Muestra el evento al que el usuario está suscrito
    event = forms.CharField(
        label='Evento:',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control input-sm', 'data-toggle': 'tooltip',
                'readonly': 'true',
                'title': 'Muestra el evento',
            }
        )
    )

    # Muestra al suscriptor
    profile = forms.CharField(
        label='Perfil:',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control input-sm', 'data-toggle': 'tooltip',
                'readonly': 'true',
                'title': 'Muestra el perfil',
            }
        )
    )

    # Variable que indica si el usuario puede descargar el certificado
    grant = forms.ChoiceField(
        label='Otorgar:',
        choices=YESNO,
        widget=forms.Select(
            attrs={
                'class': 'form-control select2', 'data-toggle': 'tooltip',
                'title': 'Seleccione la opción correcta',
            }
        ),
    )

    class Meta:
        """!
        Meta clase del formulario que establece algunas propiedades

        @author William Páez <paez.william8@gmail.com>
        """

        model = Subscriber
        fields = [
            'grant'
        ]
