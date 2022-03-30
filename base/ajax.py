import json

from django.apps import apps
from django.http import HttpResponse
from django.views import View

from .constant import MSG_NOT_AJAX


class ComboUpdateView(View):
    """!
    Clase que actualiza los datos de un select dependiente de los datos de
    otro select

    @author William Páez <paez.william8@gmail.com>
    @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>
        GNU Public License versión 2 (GPLv2)</a>
    """

    def get(self, request, *args, **kwargs):
        """!
        Función que obtiene los datos recibidos por el método get

        @author William Páez <paez.william8@gmail.com>
        @param self <b>{object}</b> Objeto que instancia la clase
        @param request <b>{object}</b> Objeto que contiene los datos de la
            petición
        @param *args <b>{tuple}</b> Tupla de valores, inicialmente vacia
        @param **kwargs <b>{dict}</b> Diccionario de datos, inicialmente vacio
        @return response <b>{response}</b> Respuesta con los datos en formato
            json
        """

        try:
            if not request.is_ajax():
                return HttpResponse(
                    json.dumps({'result': False, 'error': str(MSG_NOT_AJAX)})
                )

            # Valor del campo que ejecuta la acción
            cod = request.GET.get('option')

            # Nombre de la aplicación del modelo en donde buscar los datos
            app = request.GET.get('app')

            # Nombre del modelo en el cual se va a buscar la información a
            # mostrar
            mod = request.GET.get('mod')

            # Atributo por el cual se va a filtrar la información
            field = request.GET.get('field')

            # Atributo del cual se va a obtener el valor a registrar en las
            # opciones del combo resultante
            n_value = request.GET.get('n_value')

            # Atributo del cual se va a obtener el texto a registrar en las
            # opciones del combo resultante
            n_text = request.GET.get('n_text')

            # Nombre de la base de datos en donde buscar la información,
            # si no se obtiene el valor por defecto es default
            bd = request.GET.get('bd', 'default')

            filter = {}

            if app and mod and field and n_value and n_text and bd:
                model = apps.get_model(app, mod)

                if cod:
                    filter = {field: cod}

                out = "<option value=''>%s...</option>" % str('Seleccione')

                combo_disabled = "false"

                if cod != "" and cod != "0":
                    for o in model.objects.using(bd).filter(**filter).order_by(
                        n_text
                    ):
                        out = "%s<option value='%s'>%s</option>" \
                              % (out, str(o.__getattribute__(n_value)),
                                 o.__getattribute__(n_text))
                else:
                    combo_disabled = "true"

                return HttpResponse(
                    json.dumps({
                        'result': True, 'combo_disabled': combo_disabled,
                        'combo_html': out
                    })
                )

            else:
                return HttpResponse(
                    json.dumps({
                        'result': False,
                        'error': str('No se ha especificado el registro')
                    })
                )

        except Exception as e:
            return HttpResponse(json.dumps({'result': False, 'error': e}))
