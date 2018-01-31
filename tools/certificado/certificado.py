#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, StringIO
from PIL import ImageFont, ImageDraw, Image
from hashlib import md5
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter,landscape
import os.path
from reportlab.lib.fonts import addMapping
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

RUTA = os.path.join(os.path.dirname(__file__))


class Certificado():
    def __init__(self):
        self.directorio = False
        pdfmetrics.registerFont(TTFont('DejaVuSans', 'tools/certificado/font/DejaVuSans.ttf'))
        pdfmetrics.registerFont(TTFont('DejaVuSans-Bold', 'tools/certificado/font/DejaVuSans-Bold.ttf'))
        addMapping('DejaVuSans', 0, 0, 'DejaVuSans')
        addMapping('DejaVuSans-Bold', 0, 0, 'DejaVuSans-Bold')


    def generar(self, certificado_img_delantera, certificado_img_tracera, suscriptor, suscriptor_xy, id, id_xy, key, key_xy, tematica):
        certificado = StringIO.StringIO()
        pdf = canvas.Canvas(certificado, landscape(letter), bottomup=50)

        fuente = Image.open(certificado_img_delantera)
        draw = ImageDraw.Draw(fuente)
        pdf.drawInlineImage(fuente,0,0)

        pdf.setFillColorRGB(0,0,128)
        pdf.setFont('DejaVuSans-Bold', 40)
        pdf.drawString(suscriptor_xy[0],suscriptor_xy[1], suscriptor)
        pdf.setFont('DejaVuSans-Bold', 25)
        pdf.drawString(id_xy[0],id_xy[1], id)
        pdf.setFillColorRGB(0,0,0)
        pdf.setFont('DejaVuSans', 10)
        pdf.drawString(key_xy[0],key_xy[1], key)
        pdf.showPage()



        fuente = Image.open(certificado_img_tracera)
        draw = ImageDraw.Draw(fuente)
        pdf.drawInlineImage(fuente,0,0)

        tematica_pdf = pdf.beginText(50,562)
        tematica_pdf.textLines(tematica.splitlines())
        pdf.drawText(tematica_pdf)
        pdf.drawString(key_xy[0],10, key)
        pdf.showPage()

        pdf.save()
        return certificado.getvalue()
