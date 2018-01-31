# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.http import HttpResponse
from organizador.models import Tarea
from django.forms import ModelForm, Textarea
from django.template import RequestContext
from django.views.generic.simple import redirect_to
from django.contrib.auth.decorators import login_required

class TareaForm(ModelForm):
    class Meta:
        model = Tarea
        fields = ('descripcion', 'porcentaje')
        
        widgets = {
            'descripcion': Textarea(attrs={'readonly': 'readonly'}),
        }
        
@login_required
def actualizar_tarea(request, tarea):

    tarea = Tarea.objects.get(id=tarea)
    evento = tarea.organizador.evento
    
    if not request.POST:
        
        form = TareaForm(instance=tarea)
        
        return render_to_response('organizador/actualizar_tarea.html',{'form': form, 'evento': evento}, context_instance=RequestContext(request))
    
    else:
        
        
        form = TareaForm(request.POST, instance=tarea)
        
        if form.is_valid:
            form.save()
            return redirect_to(request, '/organizador/mis_tareas/')
            
        
        