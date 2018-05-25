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
## @namespace base.functions
#
# Contiene las funcionas básicas de la aplicación
# @author William Páez (wpaez at cenditel.gob.ve)
# @author <a href='http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/'>Licencia de Software CENDITEL versión 1.2</a>
# @date 14-01-2018
# @version 2.0

import smtplib
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import get_template

def enviar_correo(email, template, subject, vars = None):
    """!
    Función que envía correos electrónicos

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @copyright <a href='http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/'>Licencia de Software CENDITEL versión 1.2</a>
    @date 22-08-2016
    @param email    <b>{string}</b> Dirección de correo electrónico del destinatario.
    @param template <b>{string}</b> Nombre de la plantilla de correo electrónico a utilizar.
    @param subject  <b>{string}</b> Texto del asunto que contendrá el correo electrónico.
    @param vars     <b>{object}</b> Diccionario de variables que serán pasadas a la plantilla de correo. El valor por defecto es Ninguno.
    @return Devuelve verdadero si el correo fue enviado, en caso contrario, devuelve falso
    """
    if not vars:
        vars = {}

    try:
        ## Obtiene la plantilla de correo a implementar
        t = get_template(template).render(vars)
        send_mail(subject, t, settings.EMAIL_FROM, [email], fail_silently=False)
        #logger.info("Correo enviado a %s usando la plantilla %s" % (email, template))
        return True
    except smtplib.SMTPException as e:
        print("Error al enviar el correo")
        return False
