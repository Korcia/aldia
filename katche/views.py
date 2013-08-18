#coding=UTF-8

import datetime
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView
from katche.models import Pagina, Ficha
#import pdb

class FichaInicioListView(ListView):
    context_object_name = "fichas_inicio"
    #queryset = Ficha.objects.filter(pagina='inicio')
    queryset = Ficha.objects.all()
    