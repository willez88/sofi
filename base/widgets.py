from django import forms

from .constant import NATIONALITY


class IdentificationCardWidget(forms.MultiWidget):
    """!
    Clase que agrupa los widgets de los campos de nacionalidad y número de
    cédula de identidad

    @author William Páez <paez.william8@gmail.com>
    @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>
        GNU Public License versión 2 (GPLv2)</a>
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
