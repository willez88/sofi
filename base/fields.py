from django import forms

from .constant import NATIONALITY
from .widgets import IdentificationCardWidget


class IdentificationCardField(forms.MultiValueField):
    """!
    Clase que agrupa los campos de una cédula correspondientes a la
    nacionalidad y los números

    @author Ing. Roldan Vargas <rvargas@cenditel.gob.ve>
    @author William Páez <wpaez@cenditel.gob.ve>
    @copyright <a href='https://tinyurl.com/y3tfnema'>
        Licencia de Software CENDITEL versión 1.2</a>
    """

    widget = IdentificationCardWidget
    default_error_messages = {
        'invalid_choices': 'Debe seleccionar una nacionalidad válida'
    }

    def __init__(self, *args, **kwargs):

        error_messages = {
            'required': 'Debe indicar un número de cédula',
            'invalid': 'El valor indicado no es válido',
            'incomplete': 'El número de cédula esta incompleto'
        }

        fields = (
            forms.ChoiceField(choices=NATIONALITY),
            forms.CharField(max_length=8)
        )

        label = 'Cédula de Identidad:'

        super().__init__(
            error_messages=error_messages, fields=fields, label=label,
            require_all_fields=True, *args, **kwargs
        )

    def compress(self, data_list):
        if data_list:
            return ''.join(data_list)
        return ''
