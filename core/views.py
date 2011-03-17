#coding=UTF-8

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.db.models import Q
from jarrett.models import Resumen
#from django_mobile import set_flavour, get_flavour
#import re
from pyparsing import makeHTMLTags, SkipTo
#import pdb
from minidetector import *
#from django.http import HttpResponse
from core.forms import SearchFormKeyword

def main_page(request):
    return render_to_response('main_page.html', locals(), context_instance=RequestContext(request))

    
def search_page(request):
    
    if (request.method == 'GET') and 'tipobusqueda' in request.GET:
        id_keywords = request.GET['keywords'].strip()
        keywords = id_keywords.split()
        q1 = Q()
        for keyword in keywords:
            q1 = q1 | Q(contenido__icontains=keyword)
        resumenes = Resumen.objects.filter(q1)
        if resumenes:
            lista_resultados = []
            for p in resumenes:
                liTag, endliTag = makeHTMLTags("li")
                anchor = liTag + SkipTo(endliTag).setResultsName("cuerpo") + endliTag
                lista_parrafos = []
                for tokens,start,end in anchor.scanString(p.contenido):
                    for clave in keywords:
                        if clave.lower() in tokens.cuerpo.lower():
                            lista_parrafos.append(tokens.cuerpo)
                fecha_parrafo = p.fecha_publicacion
                enlace = p.get_absolute_url()
                lista_resultados.append([fecha_parrafo,enlace,lista_parrafos])
            lista_resultados = []
            fecha_parrafo = None
            enlace = None
            lista_parrafos = ["No se encontraron resultados"]
            lista_resultados.append([fecha_parrafo,enlace,lista_parrafos])
        ## fin busqueda de parrafo
        #variables = {'rowcolor1': 'impar', 'rowcolor2': 'par', 'resumenes': resumenes, 'parrafos': parrafo}
        variables = {'lista_resultados': lista_resultados}
        return render_to_response('resultados.html', variables, context_instance=RequestContext(request))
    
    form1 = SearchFormKeyword()
    variables = RequestContext(request, {
                'page_body': 'Filtre su búsqueda mediante palabras clave y período de búsqueda.',
                'form_key': form1
                })                
    return render_to_response('search_page.html', variables, context_instance=RequestContext(request))
        