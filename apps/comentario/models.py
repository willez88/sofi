# -*- coding: utf-8 -*-
#from django.db import models

# Moderando comentarios
from django.db.models.signals import pre_save, post_save, post_init
from django.contrib.comments.models import Comment
from evento.models import Evento
from django.contrib.sites.models import Site
from tools import email
from django.utils.translation import ugettext as _
from django.db import models
from django.contrib.comments.signals import comment_was_posted, comment_will_be_posted

EVENTO = None

# Los comentarios no se publican automaticamente
def pre_save_comment(sender, instance, **kwargs):
    
    
    if not instance.id:
        instance.is_public = False
        instance.instancia_evento = Evento.objects.get(id=EVENTO)
        
        
        
##Despues de cambiar el estado del comentario envia emails
def post_save_comment(sender, instance, **kwargs):
    evento = instance.instancia_evento
    
    site = Site.objects.get(id=1)
    
    if instance.is_public:
        asunto = _('Comentario aprobado')
        para = [instance.user_email]
        mensaje = _('Su comentario sobre el evento') + ' "' + evento.nombre + '" ' + _('ha sido aprobado y publicado en:') + '\n' + site.domain + '/comentario/' +  str(evento.id) + '/\n\n' + _('Gracias...')

    else:
        asunto = _(u'Nuevo comentario en lista de moderación')
        para =  [evento.email]
        mensaje = _('Un nuevo comentario sobre el evento') + ' "' + evento.nombre + '" ' + _('se encuentra en espera para ser aprobado en:') + '\n' + site.domain + '/admin/comments/comment/' +  str(instance.id) + '/\n\n' + _('Gracias...')

        
    
    try:
        email.enviar_mail(asunto, mensaje, evento.email, para)
    except Exception, error:
        pass

def pp(sender, comment, request, **kwargs):
    global EVENTO
    EVENTO = int(request.POST['instancia_evento'])
    
    

comment_will_be_posted.connect(pp)
pre_save.connect(pre_save_comment, sender=Comment)
post_save.connect(post_save_comment, sender=Comment)

Comment.add_to_class('instancia_evento', models.ForeignKey(Evento, verbose_name=_(u'Evento')))