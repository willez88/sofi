from django import forms

from .models import Municipality, Parish, State


class LocationForm(forms.Form):
    """!
    Clase que muestra el formulario de ubicación geográfica

    @author William Páez <wpaez@cenditel.gob.ve>
    @copyright <a href='https://tinyurl.com/y3tfnema'>
        Licencia de Software CENDITEL versión 1.2</a>
    """

    # Estado o Entidad en donde se encuentra ubicado el municipio
    state = forms.ModelChoiceField(
        label='Estado:', queryset=State.objects.all(),
        empty_label='Seleccione...',
        widget=forms.Select(attrs={
            'class': 'form-control select2', 'data-toggle': 'tooltip',
            'title': 'Seleccione el estado en donde se encuentra ubicado',
            'onchange': "combo_update(this.value, 'base', 'Municipality',\
                'state', 'pk', 'name', 'id_municipality')"
        })
    )

    # Municipio en el que se encuentra ubicada la parroquia
    municipality = forms.ModelChoiceField(
        label='Municipio:', queryset=Municipality.objects.all(),
        empty_label='Seleccione...',
        widget=forms.Select(attrs={
            'class': 'form-control select2', 'data-toggle': 'tooltip',
            'disabled': 'true',
            'title': 'Seleccione el municipio en donde se encuentra ubicado',
            'onchange': "combo_update(this.value, 'base', 'Parish',\
                'municipality', 'pk', 'name', 'id_parish')"
        })
    )

    # Parroquia en donde se encuentra ubicada la dirección suministrada
    parish = forms.ModelChoiceField(
        label='Parroquia:', queryset=Parish.objects.all(),
        empty_label='Seleccione...',
        widget=forms.Select(attrs={
            'class': 'form-control select2', 'data-toggle': 'tooltip',
            'disabled': 'true',
            'title': 'Seleccione la parroquia en donde se encuentra ubicado'
        })
    )

    # Dirección exacta del usuario
    address = forms.CharField(
        label='Dirección:',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control input-sm', 'data-toggle': 'tooltip',
                'title': 'Indique la dirección exacta en donde se encuentra\
                    ubicado',
            }
        )
    )

    def __init__(self, *args, **kwargs):
        """!
        Método que inicializa los atributos de la clase LocationForm

        @author William Páez <wpaez@cenditel.gob.ve>
        @copyright <a href='https://tinyurl.com/y3tfnema'>
            Licencia de Software CENDITEL versión 1.2</a>
        @param self <b>{object}</b> Objeto que instancia la clase
        @param self <b>{*args}</b> Lista de argumentos del método
        @param self <b>{**kwargs}</b> Diccionario de argumentos de la función
        """

        super().__init__(*args, **kwargs)
        # Si se ha seleccionado un estado establece el listado de municipios y
        # elimina el atributo disable
        if 'state' in self.data and self.data['state']:
            self.fields['municipality'].widget.attrs.pop('disabled')
            self.fields['municipality'].queryset = Municipality.objects.filter(
                state=self.data['state']
            )

            # Si se ha seleccionado un municipio establece el listado de
            # parroquias y elimina el atributo disable
            if 'municipality' in self.data and self.data['municipality']:
                self.fields['parish'].widget.attrs.pop('disabled')
                self.fields['parish'].queryset = Parish.objects.filter(
                    municipality=self.data['municipality']
                )
