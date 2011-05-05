#coding=UTF-8

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from core.forms import ContactForm
from django.db.models import Q
from jarrett.models import Resumen
import datetime
#from django_mobile import set_flavour, get_flavour
import re
from pyparsing import makeHTMLTags, SkipTo
#import pdb
#from minidetector import *
#from django.http import HttpResponse
from core.forms import SearchFormKeyword

def main_page(request):
    return render_to_response('main_page.html', locals(), context_instance=RequestContext(request))

def buscar_page(request):
    
    if (request.method == 'GET') and 'tipobusqueda' in request.GET:
        if (request.GET['keywords'] == u''):
            found = False
            errors = True
            lista_resultados = []
            lista_parrafos = ["Por favor, introduzca una palabra."]
            lista_resultados.append([lista_parrafos])
            variables = {'lista_resultados': lista_resultados, 'errors': errors, 'found': found}
            return render_to_response('resultados.html', variables, context_instance=RequestContext(request))

        id_keywords = request.GET['keywords'].strip()
        keywords = id_keywords.split()
        errors = False
        for keyword in keywords:
            if not re.search(r'^\w+$', keyword):
                errors = True
                found = False
                lista_resultados = []
                lista_parrafos = ["Por favor, introduzca sólo letras y/o números."]
                lista_resultados.append([lista_parrafos])
                variables = {'lista_resultados': lista_resultados, 'errors': errors, 'found': found}
                return render_to_response('resultados.html', variables, context_instance=RequestContext(request))
        q1 = Q()
        for keyword in keywords:
            q1 = q1 | Q(contenido__icontains=keyword)
        resumenes = Resumen.objects.filter(q1)
        if resumenes:
            found = True
            lista_resultados = []
            for p in resumenes:
                liTag, endliTag = makeHTMLTags("li")
                anchor = liTag + SkipTo(endliTag).setResultsName("cuerpo") + endliTag
                lista_parrafos = []
                for tokens,start,end in anchor.scanString(p.contenido):
                    for clave in keywords:
                        if clave.lower() in tokens.cuerpo.lower():
                            lista_parrafos.append(tokens.cuerpo)
                hits = len(lista_parrafos)
                fecha_parrafo = p.fecha_publicacion
                enlace = p.get_absolute_url()
                lista_resultados.append([fecha_parrafo,enlace,lista_parrafos,hits])
        else:
            found = False
            lista_resultados = []
            fecha_parrafo = None
            enlace = None
            lista_parrafos = ["No se encontraron resultados."]
            lista_resultados.append([fecha_parrafo,enlace,lista_parrafos])
        ## fin busqueda de parrafo
        variables = {'lista_resultados': lista_resultados, 'errors': errors, 'found': found}
        return render_to_response('resultados.html', variables, context_instance=RequestContext(request))

    if (request.method == 'GET') and 'ajax' in request.GET and request.is_ajax():
        #is_ajax() es necesario para evitar que alguien ponga en la url ?ajax&query=palabra a pelo
        if (request.GET['query'] == u''):
            found = False
            errors = True
            lista_resultados = []
            lista_parrafos = ["Por favor, introduzca una palabra."]
            lista_resultados.append([lista_parrafos])
            variables = {'lista_resultados': lista_resultados, 'errors': errors, 'found': found}
            return render_to_response('resultados_ajax.html', variables, context_instance=RequestContext(request))
        id_keywords = request.GET['query'].strip()
        keywords = id_keywords.split()
        errors = False
        for keyword in keywords:
            if not re.search(r'^\w+$', keyword):
                found = False
                errors = True
                lista_resultados = []
                lista_parrafos = ["Introduzca solo palabra y/o numeros."]
                lista_resultados.append([lista_parrafos])
                variables = {'lista_resultados': lista_resultados,'errors': errors, 'found': found}
                return render_to_response('resultados_ajax.html', variables, context_instance=RequestContext(request))
        q1 = Q()
        for keyword in keywords:
            q1 = q1 | Q(contenido__icontains=keyword)
        resumenes = Resumen.objects.filter(q1)
        if resumenes:
            found = True
            lista_resultados = []
            for p in resumenes:
                liTag, endliTag = makeHTMLTags("li")
                anchor = liTag + SkipTo(endliTag).setResultsName("cuerpo") + endliTag
                lista_parrafos = []
                for tokens,start,end in anchor.scanString(p.contenido):
                    for clave in keywords:
                        if clave.lower() in tokens.cuerpo.lower():
                            lista_parrafos.append(tokens.cuerpo)
                hits = len(lista_parrafos)
                fecha_parrafo = p.fecha_publicacion
                enlace = p.get_absolute_url()
                lista_resultados.append([fecha_parrafo,enlace,lista_parrafos,hits])
        else:
            found = False
            lista_resultados = []
            fecha_parrafo = None
            enlace = None
            lista_parrafos = ["No se encontraron resultados."]
            lista_resultados.append([fecha_parrafo,enlace,lista_parrafos])
        ## fin busqueda de parrafo
        variables = {'lista_resultados': lista_resultados,'errors': errors, 'found': found}
        return render_to_response('resultados_ajax.html', variables)
    ahora = datetime.datetime.now()
    form1 = SearchFormKeyword()
    variables = RequestContext(request, {
                'ahora': ahora,
                'form_key': form1
                })                
    return render_to_response('buscar_page.html', variables, context_instance=RequestContext(request))

@csrf_exempt
def contact(request):
    #c = {}
    #c.update(csrf(request))
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            send_mail(
                cd['asunto'],
                cd['mensaje'],
                cd.get('email', 'noreply@example.com'),
                ['jmgmontes@gmail.com'],
            )
            return render_to_response('gracias.html')
    else:
        form = ContactForm()
    return render_to_response('contacto.html', {'form': form}, context_instance=RequestContext(request))