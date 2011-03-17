#coding=UTF-8
import os.path

from django.conf.urls.defaults import *
from core.views import main_page, contact, search_page
from django.contrib.auth.views import login, logout
from django.contrib import admin
admin.autodiscover()
static = os.path.join(os.path.dirname(__file__), 'static')

urlpatterns = patterns('',
    (r'^$', main_page),
    (r'^buscar/$', search_page),
    (r'^resumenes/', include('coltrane.urls.resumenes')),    
    (r'^contacto/$', contact),
    (r'^demo/', include('jarrett.urls.resumenes')),
    (r'^usuario/login/', login),
    (r'^usuario/logout/', logout, {'next_page': '/' }),
    (r'^admin/', include(admin.site.urls)),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': static}),
)
