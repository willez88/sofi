from django import forms

from .constant import NATIONALITY


class IdentificationCardWidget(forms.MultiWidget):
    """!
    Clase que agrupa los widgets de los campos de nacionalidad y número de
    cédula de identidad

    @author Ing. Roldan Vargas <rvargas@cenditel.gob.ve>
    @author William Páez <wpaez@cenditel.gob.ve>
    @copyright <a href='https://tinyurl.com/y3tfnema'>
        Licencia de Software CENDITEL versión 1.2</a>
    """

    def __init__(self, *args, **kwargs):

        widgets = (
            forms.Select(
                attrs={
                    'class': 'select2 form-control', 'data-toggle': 'tooltip',
                    'title': 'Seleccione la nacionalidad'
                }, choices=NATIONALITY
            ),
            forms.TextInput(
                attrs={
                    'class': 'form-control text-center input-sm',
                    'placeholder': '00000000', 'data-mask': '00000000',
                    'data-toggle': 'tooltip',
                    'title': 'Indique el número de cédula de identidad'
                }
            )
        )

        super().__init__(widgets, *args, **kwargs)

    def format_output(self, rendered_widgets):
        return ' - '.join(rendered_widgets)

    def decompress(self, value):
        if value:
            return [value[0], value[1:]]
        return [None, None]
