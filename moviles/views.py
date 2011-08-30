#coding=UTF-8

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.db.models import Q
from jarrett.models import Resumen
from utils.BeautifulSoup import BeautifulSoup
#from minidetector import *

def ultimo(request):
    resumen = Resumen.objects.all()[0]
    #lista_resultados = []
    soup = BeautifulSoup(resumen.contenido)
    divisiones =soup.findAll("div", attrs={"id": "Section2"})
    division = divisiones[0]
    cadena = division.renderContents()
    #lista_resultados.append(divisiones)
    variable = {'resumen': cadena }
    #pdb.set_trace()
    return render_to_response('mobile/resumen_ultimo.html', variable)

def archivo(request):
    
    if (request.method == 'GET') and 'tipobusqueda' in request.GET:
        fecha = request.GET['fecha'].strip()
        variables = {'fecha_resultado': fecha }
        return render_to_response('mobile/archivo_fecha.html', variables, context_instance=RequestContext(request))
