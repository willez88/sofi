# -*- coding: utf-8 -*-

from django import template
from django.conf import settings
from django.contrib.sites.models import Site
from django.utils.translation import ugettext as _
from configuracion.models import Site

register = template.Library()


@register.simple_tag
def media_url():
    return settings.MEDIA_URL

@register.simple_tag
def theme():
    return settings.THEME

@register.simple_tag
def site_title():
    site = Site.objects.get_current()
    if site.titulo:
        return site.titulo
    else:
        return _(u'Título 1')

@register.simple_tag    
def site_subtitle():
    site = Site.objects.get_current()
    if site.subtitulo:
        return site.subtitulo
    else:
        return _(u'Subtítulo')

@register.simple_tag
def site_informacion():
    site = Site.objects.get_current()
    return site.informacion

@register.simple_tag
def logo():
    site = Site.objects.get_current()
    
    if site.logo.url_120x100:
        logo = site.logo.url_120x100
    else:
        logo = "%sthemes/%s/images/img01.jpg" % (settings.MEDIA_URL, settings.THEME)
    
    return logo

@register.simple_tag
def banner():
        
    site = Site.objects.get_current()
    
    if site.banner.url_160x600:
        banner = site.banner.url_160x600
    else:
        banner = "%sthemes/%s/images/ad160x600.gif" % (settings.MEDIA_URL, settings.THEME)

    return banner
        