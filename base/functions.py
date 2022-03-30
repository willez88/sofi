import smtplib

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import get_template


def send_email(email, template, subject, vars=None):
    """!
    Función que envía correos electrónicos

    @author William Páez <paez.william8@gmail.com>
    @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>
        GNU Public License versión 2 (GPLv2)</a>
    @param email    <b>{string}</b> Dirección de correo electrónico del
        destinatario.
    @param template <b>{string}</b> Nombre de la plantilla de correo
        electrónico a utilizar.
    @param subject  <b>{string}</b> Texto del asunto que contendrá el correo
        electrónico.
    @param vars     <b>{object}</b> Diccionario de variables que serán pasadas
        a la plantilla de correo. El valor por defecto es Ninguno.
    @return Devuelve verdadero si el correo fue enviado, en caso contrario,
        devuelve falso
    """
    if not vars:
        vars = {}

    try:
        # Obtiene la plantilla de correo a implementar
        t = get_template(template).render(vars)
        send_mail(
            subject, t, settings.EMAIL_HOST_USER, [email], fail_silently=False
        )
        # logger.info("Correo enviado a %s usando la plantilla %s" %
        # (email, template))
        return True
    except smtplib.SMTPException as e:
        print('Error: ', e)
        return False
