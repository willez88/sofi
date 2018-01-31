#!/usr/bin/env python
# -*- coding: utf-8 -*-

import matplotlib
matplotlib.use('Agg')

import numpy as np
import matplotlib.pyplot as plt
from encuesta.models import Encuesta
import os.path
from django.utils.translation import ugettext as _

RUTA = os.path.join(os.path.dirname(__file__))

    
def generar_encuesta(evento_id, evento_nombre, items, mucho, suficiente, poco, nada):
    ind = np.arange(len(items))
    width = 0.2 
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    
    rects1 = ax.bar(ind, mucho, width, color='#bce925', linewidth=0.1)
    rects2 = ax.bar(ind+width, suficiente, width, color='#f0d900', linewidth=0.1)
    rects3 = ax.bar(ind+width*2, poco, width, color='#e85e00', linewidth=0.1)
    rects4 = ax.bar(ind+width*3, nada, width, color='#770000', linewidth=0.1)
    
    ax.set_ylabel(_('Encuestados'))
    ax.set_title(evento_nombre)
    ax.set_xticks(ind+width)
    
    ax.set_yticks((0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100))
    ax.set_yticklabels(('0%', '10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%'))
    
    ax.set_xticklabels( items )
    ax.legend( (rects1[0], rects2[0], rects3[0], rects4[0]), (_('Mucho'), _('Suficiente'), _('Poco'), _('Nada')) )
    
    plt.savefig('%s/../site_media/encuesta/files/%s.png' % (RUTA, evento_id), dpi=60)
    
    return '/site_media/encuesta/files/%s.png' % (evento_id)


