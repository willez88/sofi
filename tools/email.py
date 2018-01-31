from django.core.mail import send_mail

def enviar_mail(asunto, mensaje, direccion_emisor, direccion_destino):
    send_mail(asunto, mensaje, direccion_emisor, direccion_destino)
