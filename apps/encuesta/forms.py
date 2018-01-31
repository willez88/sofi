#!/usr/bin/env python
# -*- coding: utf-8 -*-
from encuesta.models import Encuesta, Items
from django import forms
from tools.constantes import MSPN

class EncuestaForm(forms.Form):
    
    def __init__(self, evento, data=None):
        if data:
            forms.Form.__init__(self, data)
        else:
            forms.Form.__init__(self)
        
        self.items = Items.objects.filter(encuesta__evento=evento).order_by('id')
        
        for i in self.items:
            self.fields[str(i.id)] = forms.ChoiceField(choices=MSPN, label=i.nombre)
        
        
        
    


