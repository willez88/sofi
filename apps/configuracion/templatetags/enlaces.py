# -*- coding: utf-8 -*-

from django import template
from django.utils.translation import ugettext as _
from configuracion.models import Enlaces

register = template.Library()

@register.inclusion_tag("configuracion/enlaces.html")
def show_enlaces(ubicacion):
    return {'enlaces': Enlaces.objects.filter(ubicacion=bool(ubicacion)),}
   


