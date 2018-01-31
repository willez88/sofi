# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError
from django.utils.translation import ugettext as _
from django.core.mail import send_mail

class Command(BaseCommand):

    def handle(self, *args, **options):
        
        try:
            asunto = args[0]
            mensaje = args[1]
            direccion_emisor = args[2]
            direccion_destino = args[3].split(',')
            
            send_mail(asunto, mensaje, direccion_emisor, direccion_destino)
            
            self.stdout.write(_(u'Email enviado'))
        except Exception, error:
            raise CommandError(_(u'Error al enviar email') + ':\n%s' % str(error))
