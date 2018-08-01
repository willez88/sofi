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
## @namespace base.ajax
#
# Contiene las clases, atributos y métodos básicos del sistema para usarlos mediante ajax
# @author William Páez (wpaez at cenditel.gob.ve)
# @author <a href='http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @author <a href='www.cida.gob.ve/'>Centro de Investigaciones de Astronomía "Francisco J. Duarte"</a>
# @copyright <a href='http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/'>Licencia de Software CENDITEL versión 1.2</a>
# @date 16-06-2018
# @version 2.0

from django.views import View
from django.utils.translation import ugettext_lazy as _
from django.apps import apps
import json
from django.http import HttpResponse
from .constant import MSG_NOT_AJAX

class ComboUpdateView(View):
    """!
    Clase que actualiza los datos de un select dependiente de los datos de otro select

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @author William Páez (wpaez at cenditel.gob.ve)
    @copyright <a href='http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/'>Licencia de Software CENDITEL versión 1.2</a>
    @date 16-06-2018
    """

    def get(self, request, *args, **kwargs):
        """!
        Función que obtiene los datos recibidos por el método get

        @author William Páez (wpaez at cenditel.gob.ve)
        @date 16-06-2018
        @param self <b>{object}</b> Objeto que instancia la clase
        @param request <b>{object}</b> Objeto que contiene los datos de la petición
        @param *args <b>{tuple}</b> Tupla de valores, inicialmente vacia
        @param **kwargs <b>{dict}</b> Diccionario de datos, inicialmente vacio
        @return response <b>{response}</b> Respuesta con los datos en formato json
        """

        try:
            if not request.is_ajax():
                return HttpResponse(json.dumps({'result': False, 'error': str(MSG_NOT_AJAX)}))

            ## Valor del campo que ejecuta la acción
            cod = request.GET.get('option', None)

            ## Nombre de la aplicación del modelo en donde buscar los datos
            app = request.GET.get('app', None)

            ## Nombre del modelo en el cual se va a buscar la información a mostrar
            mod = request.GET.get('mod', None)

            ## Atributo por el cual se va a filtrar la información
            field = request.GET.get('field', None)

            ## Atributo del cual se va a obtener el valor a registrar en las opciones del combo resultante
            n_value = request.GET.get('n_value', None)

            ## Atributo del cual se va a obtener el texto a registrar en las opciones del combo resultante
            n_text = request.GET.get('n_text', None)

            ## Nombre de la base de datos en donde buscar la información, si no se obtiene el valor por defecto es default
            bd = request.GET.get('bd', 'default')

            filtro = {}

            if app and mod and field and n_value and n_text and bd:
                model = apps.get_model(app, mod)

                if cod:
                    filter = {field: cod}

                out = "<option value=''>%s...</option>" % str(_("Seleccione"))

                combo_disabled = "false"

                if cod != "" and cod != "0":
                    for o in model.objects.using(bd).filter(**filter).order_by(n_text):
                        out = "%s<option value='%s'>%s</option>" \
                              % (out, str(o.__getattribute__(n_value)),
                                 o.__getattribute__(n_text))
                else:
                    combo_disabled = "true"

                return HttpResponse(json.dumps({'result': True, 'combo_disabled': combo_disabled, 'combo_html': out}))

            else:
                return HttpResponse(json.dumps({'result': False,
                                                'error': str(_('No se ha especificado el registro'))}))

        except Exception as e:
            return HttpResponse(json.dumps({'result': False, 'error': e}))
