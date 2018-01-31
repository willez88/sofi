#!/usr/bin/env python
from django.contrib.syndication.feeds import Feed
from django.utils.feedgenerator import Atom1Feed
from evento.models import Evento
from django.contrib.sites.models import Site

class Rss(Feed):
    title = "Eventos"
    link = "/feed/rss"
    description = "Eventos publicados en http://%s" % (Site.objects.get(id=1).domain)

    def item_link(self, obj):
        return "/detalle/%s" % (str(obj.id))
    
    def items(self, obj):
        return Evento.objects.filter(publicar=True)[:5]
        
class Atom(Rss):
    feed_type = Atom1Feed
