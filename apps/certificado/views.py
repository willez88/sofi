# Create your views here.
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
from evento.models import Evento
from certificado.models import CertificadoSuscriptor
from tools.certificado.certificado import Certificado
from django.template import RequestContext

def descargar(request, evento, key, encuesta=None):

    certificado =  CertificadoSuscriptor()
    try:
        suscriptor = CertificadoSuscriptor.objects.get(key=key)
    except Exception, error:
        suscriptor = None

    if suscriptor and suscriptor.otorgar:
        if suscriptor.certificado.evento.id == int(evento):
            gen_certificado = Certificado()
            url = suscriptor.certificado.imagen_de_fondo_delantera.path

            if suscriptor.certificado.imagen_de_fondo_delantera.path:
                url1 = suscriptor.certificado.imagen_de_fondo_tracera.path
            else:
                url1 = None

            nombre_suscriptor = suscriptor.suscriptor.nombre_completo()

            ancho_certificado = suscriptor.certificado.imagen_de_fondo_delantera.width / 2
            ancho_nombre = (len(nombre_suscriptor) * 22 ) / 2
            posicion_x_nombre = ancho_certificado - ancho_nombre
            posicion_nombre = posicion_x_nombre, suscriptor.certificado.posicion_y_nombre

            posicion_key = suscriptor.certificado.posicion_x_key, suscriptor.certificado.posicion_y_key

            cedula_id = "ID: %s" % str(suscriptor.suscriptor.suscriptor.cedula)
            ancho_cedula_id = (len(cedula_id) * 14 ) / 2
            posicion_x_cedula_id = ancho_certificado - ancho_cedula_id
            posicion_cedula_id = posicion_x_cedula_id, suscriptor.certificado.posicion_y_nombre - 44

            key = suscriptor.key
            tematica = suscriptor.certificado.tematica
            pdf = gen_certificado.generar(url, url1,nombre_suscriptor, posicion_nombre, cedula_id, posicion_cedula_id, key, posicion_key, tematica)
            response = HttpResponse(mimetype='application/pdf')
            response['Content-Disposition'] = ('attachment; filename=%s.pdf' % key)
            response.write(pdf)
            return response

    raise Http404()

def obtenerCertificados(request):
    print "ejecutada obtenerCertificados"

    try:
        all_suscriptor = CertificadoSuscriptor.objects.all()
        for e in all_suscriptor:
            #print(e.key)
            #print(e.certificado_id)

            suscriptor = CertificadoSuscriptor.objects.get(key=e.key)
            #print "luego de suscriptor"
            if suscriptor: # and suscriptor.otorgar:
                #print "suscriptor != None"
                if suscriptor.certificado.evento.id == int(e.certificado_id):
                    gen_certificado = Certificado()
                    url = suscriptor.certificado.imagen_de_fondo_delantera.path
                    #print "url %s" % url
                    if suscriptor.certificado.imagen_de_fondo_delantera.path:
                        url1 = suscriptor.certificado.imagen_de_fondo_tracera.path
                    else:
                        url1 = None

                    nombre_suscriptor = suscriptor.suscriptor.nombre_completo()

                    ancho_certificado = suscriptor.certificado.imagen_de_fondo_delantera.width / 2
                    ancho_nombre = (len(nombre_suscriptor) * 22 ) / 2
                    posicion_x_nombre = ancho_certificado - ancho_nombre
                    posicion_nombre = posicion_x_nombre, suscriptor.certificado.posicion_y_nombre

                    posicion_key = suscriptor.certificado.posicion_x_key, suscriptor.certificado.posicion_y_key

                    cedula_id = "C.I.: %s" % str(suscriptor.suscriptor.suscriptor.cedula)
                    ancho_cedula_id = (len(cedula_id) * 14 ) / 2
                    posicion_x_cedula_id = ancho_certificado - ancho_cedula_id
                    posicion_cedula_id = posicion_x_cedula_id, suscriptor.certificado.posicion_y_nombre - 44

                    key = suscriptor.key
                    tematica = suscriptor.certificado.tematica

                    #print "antes de gen_certificado.generar"
                    pdf = gen_certificado.generar(url, url1,nombre_suscriptor, posicion_nombre, cedula_id, posicion_cedula_id, key, posicion_key, tematica)
                    #print "luego de certificado.generar "
                    #print pdf

    except Exception, error:
        suscriptor = None

    response = HttpResponse(mimetype='text/plain')
    response.write(pdf)
    return response
