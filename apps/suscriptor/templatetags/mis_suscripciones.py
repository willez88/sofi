# -*- coding: utf-8 -*-

from django import template
from django.utils.translation import ugettext as _

from suscriptor.models import Suscriptores, UserProfile



register = template.Library()

@register.inclusion_tag("suscriptor/mis_suscripciones.html")
def show_suscripciones(user):
    suscriptor_profile = UserProfile.objects.filter(user=user)
    suscripciones = Suscriptores.objects.filter(suscriptor=suscriptor_profile)
    return {'mis_suscripciones': suscripciones,}
