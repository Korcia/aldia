#coding=UTF-8

import re
import time
from datetime import date, timedelta
import datetime
#import pdb
from django.shortcuts import render_to_response
from django.template import RequestContext
from katche.models import Ficha
from django.views.decorators.csrf import csrf_exempt
from .forms import ContactForm
from django.db.models import Q
from django.core.mail import send_mail
from jarrett.models import Resumen as jResumen
from coltrane.models import Resumen
from utils.pyparsing import makeHTMLTags, SkipTo
from core.forms import SearchFormKeyword

stopwords = ('a','b','c','d','e','f','g','h','i','j','k','l','m','n','ñ','o','p','q','r',
             's','t','u','v','w','x','y','z','á','é','í','ó','ú','ante','bajo','cabe',
             'con','contra','de','desde','durante','en','entre','excepto','hacia','hasta',
             'mediante','para','por','pro','salvo','según','segun','sin','so','sobre',
             'tras','vía','via','que','qué','manera','así','asi','fin','por','más','pese',
             'antes','después','despues','ni','pero','sino','si','sí','no','luego','tan',
             'tanto','el','él','la','lo','las','los','este','éste','ese','aquel','esta',
             'ésta','esa','aquella','estos','esos','aquellos','estas','esas','aquellas'
             'un','una','unos','unas','al','del')

def inicio(request):
    fichas_inicio = Ficha.objects.filter(pagina='inicio')
    return render_to_response('inicio.html', locals(), context_instance=RequestContext(request))

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
                ['aldia@laprensadehoy.es'],
            )
            return render_to_response('gracias.html')
    else:
        form = ContactForm()
    return render_to_response('contacto.html', {'form': form}, context_instance=RequestContext(request))

def suscripcion(request):
    return render_to_response('suscripcion.html', locals(), context_instance=RequestContext(request))

def gracias(request):
    return render_to_response('gracias.html', locals(), context_instance=RequestContext(request))

def monthdelta(date, delta):
    m, y = (date.month+delta) % 12, date.year + ((date.month)+delta-1) // 12
    if not m: m = 12
    d = min(date.day, [31,
        29 if y%4==0 and not y%400==0 else 28,31,30,31,30,31,31,30,31,30,31][m-1])
    return date.replace(day=d,month=m, year=y)

def buscador(request):
    
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
        keywords_sinfiltrar = id_keywords.split() #quito atributo .lower()
        keywords_low_sinfiltrar = [x.lower() for x in keywords_sinfiltrar]
        #añado funcionalidad para la restricción en periodo de tiempo
        id_periodo = request.GET['fecha_periodo'].strip()
        q1 = Q()
        #if id_periodo == 'DI':
        #    hoy1 = date.today()
        #    hoy = datetime.date(hoy1)
        #    q1 = q1 | Q(fecha_publicacion = hoy)
        if id_periodo == 'ME':
            hoy = date.today()
            start_date = monthdelta(date.today(), -1)
            end_date = datetime.date(hoy.year, hoy.month, hoy.day)
            q1 = q1 | Q(fecha_publicacion__range = (start_date, end_date))
        elif id_periodo == 'TR':
            hoy = date.today()
            start_date = monthdelta(date.today(), -3)
            end_date = datetime.date(hoy.year, hoy.month, hoy.day)
            q1 = q1 | Q(fecha_publicacion__range = (start_date, end_date))            
        elif id_periodo == 'SE':
            hoy = date.today()
            start_date = monthdelta(date.today(), -6)
            end_date = datetime.date(hoy.year, hoy.month, hoy.day)
            q1 = q1 | Q(fecha_publicacion__range = (start_date, end_date))            
        elif id_periodo == 'AN':
            hoy = date.today()
            start_date = monthdelta(date.today(), -12)
            end_date = datetime.date(hoy.year, hoy.month, hoy.day)
            q1 = q1 | Q(fecha_publicacion__range = (start_date, end_date))
        elif id_periodo == 'TO':
            hoy = date.today()
            start_date = datetime.date(2012, 01, 23)
            end_date = datetime.date(hoy.year, hoy.month, hoy.day)
            q1 = q1 | Q(fecha_publicacion__range = (start_date, end_date))
        else:
            hoy = date.today()
            start_date = monthdelta(date.today(), -1)
            end_date = datetime.date(hoy.year, hoy.month, hoy.day)
            q1 = q1 | Q(fecha_publicacion__range = (start_date, end_date))
        #keywords = id_keywords.split()
        errors = False
        keywords = [w for w in keywords_low_sinfiltrar if not w in stopwords]
        for keyword in keywords:
            if not re.search(r'^\w+$', keyword, re.UNICODE):
                errors = True
                found = False
                lista_resultados = []
                lista_parrafos = ["Por favor, introduzca sólo letras y/o números."]
                lista_resultados.append([lista_parrafos])
                variables = {'lista_resultados': lista_resultados, 'errors': errors, 'found': found}
                return render_to_response('resultados.html', variables, context_instance=RequestContext(request))
        #q1 = Q()
        for keyword in keywords:
            #q1 = q1 | Q(contenido__iexact=keyword)
            q2 = q1 | Q(contenido__icontains=keyword)
        #resumenes = Resumen.objects.filter(q1)
        if request.user.is_authenticated():
            resumenes = Resumen.objects.filter(q2)
        else:
            resumenes = jResumen.objects.filter(q2)
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
        ### ------------------ BUSQUEDA CON COMILLAS -------------------- ##
        #pdb.set_trace()
        id_keywords = request.GET['query'].strip()
        #añado funcionalidad para la restricción en periodo de tiempo
        if request.GET['fecha_periodo'] != '':
            id_periodo = request.GET['fecha_periodo'].strip()
        
        q1 = Q()
        if id_periodo == 'ME':
            hoy = date.today()
            start_date = monthdelta(date.today(), -1)
            end_date = datetime.date(hoy.year, hoy.month, hoy.day)
            q1 = q1 | Q(fecha_publicacion__range = (start_date, end_date))
        elif id_periodo == 'TR':
            hoy = date.today()
            start_date = monthdelta(date.today(), -3)
            end_date = datetime.date(hoy.year, hoy.month, hoy.day)
            q1 = q1 | Q(fecha_publicacion__range = (start_date, end_date))            
        elif id_periodo == 'SE':
            hoy = date.today()
            start_date = monthdelta(date.today(), -6)
            end_date = datetime.date(hoy.year, hoy.month, hoy.day)
            q1 = q1 | Q(fecha_publicacion__range = (start_date, end_date))            
        elif id_periodo == 'AN':
            hoy = date.today()
            start_date = monthdelta(date.today(), -12)
            end_date = datetime.date(hoy.year, hoy.month, hoy.day)
            q1 = q1 | Q(fecha_publicacion__range = (start_date, end_date))
        elif id_periodo == 'TO':
            hoy = date.today()
            start_date = datetime.date(2012, 01, 23)
            end_date = datetime.date(hoy.year, hoy.month, hoy.day)
            q1 = q1 | Q(fecha_publicacion__range = (start_date, end_date))
        else:
            hoy = date.today()
            start_date = monthdelta(date.today(), -1)
            end_date = datetime.date(hoy.year, hoy.month, hoy.day)
            q1 = q1 | Q(fecha_publicacion__range = (start_date, end_date))
        
        if re.search(r'"([^"]*)"', id_keywords, re.UNICODE):
            grupo_comillas = re.search(r'"([^"]*)"', id_keywords, re.UNICODE)
            keywords_comillas = grupo_comillas.group()
            #string_comillas = str(keywords_comillas)
            string_comillas = keywords_comillas
            string_sin_comillas = string_comillas.strip('"')
            #str_sin_comillas_uni = u'string_sin_comillas'
            q2 = Q()
            q2 = Q(contenido__icontains= string_sin_comillas)
            #q1 = q1 | Q(contenido__icontains= "NH Hoteles")
            if request.user.is_authenticated():
                resumenes = Resumen.objects.filter(q1).filter(q2)
            else:
                resumenes = jResumen.objects.filter(q1).filter(q2)
            if resumenes:
                found = True
                lista_resultados = []
                for p in resumenes:
                    liTag, endliTag = makeHTMLTags("li")
                    anchor = liTag + SkipTo(endliTag).setResultsName("cuerpo") + endliTag
                    lista_parrafos = []
                    for tokens,start,end in anchor.scanString(p.contenido):
                        #string_con_acentos = unicode(string_sin_comillas)
                        if string_sin_comillas.lower() in tokens.cuerpo.lower():
                            lista_parrafos.append(tokens.cuerpo)
                    #pdb.set_trace()
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
            errors = False
            variables = {'lista_resultados': lista_resultados,'errors': errors, 'found': found}
            return render_to_response('resultados_ajax.html', variables)

        keywords_sinfiltrar = id_keywords.split()
        keywords_low_sinfiltrar = [x.lower() for x in keywords_sinfiltrar]
        #keywords = id_keywords.split()
        errors = False
        keywords = [w for w in keywords_low_sinfiltrar if not w in stopwords]
        #for keyword in keywords:
            #pdb.set_trace()
            #if not re.search(r'^(\w|\')+$', keyword, re.UNICODE):
            #if not re.search(r'^(áéíóúñ"\'\’zA-Z0-9-\s)+$', keyword, re.UNICODE):
            #    found = False
            #    errors = True
            #    lista_resultados = []
            #    lista_parrafos = ["Introduzca solo palabra y/o numeros."]
            #    lista_resultados.append([lista_parrafos])
            #    variables = {'lista_resultados': lista_resultados,'errors': errors, 'found': found}
            #    return render_to_response('resultados_ajax.html', variables, context_instance=RequestContext(request))
        q2 = Q()
        for keyword in keywords:
            #q1 = q1 | Q(contenido__iexact=keyword)
            q2 =  Q(contenido__icontains=keyword)
        #resumenes = Resumen.objects.filter(q1)
        if request.user.is_authenticated():
            resumenes = Resumen.objects.filter(q1).filter(q2)
        else:
            resumenes = jResumen.objects.filter(q1).filter(q2)
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
    return render_to_response('busqueda.html', variables, context_instance=RequestContext(request))
