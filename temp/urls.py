#coding=UTF-8
from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib.auth.views import login, logout
from core.views import inicio, contact, buscador, suscripcion, gracias
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', inicio),
    (r'^contacto/$', contact),
    (r'^demo/', include('jarrett.urls.resumenes')),
    (r'^resumenes/', include('coltrane.urls.resumenes')),
    (r'^usuario/login/', login),
    (r'^usuario/logout/', logout, {'next_page': '/' }),
    (r'^buscar/$', buscador),
    (r'^suscripcion/$', suscripcion),
    (r'^gracias/$', gracias),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^admin/', include(admin.site.urls)),
    #url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
    #    'document_root': settings.MEDIA_ROOT,
    #    }),
)

urlpatterns += patterns('',
    #url(r'^aviso-legal/$', 'flatpage', {'url': '/aviso-legal/'}, name='legal'),
    #url(r'^privacidad/$', 'flatpage', {'url': '/privacidad/'}, name='privacidad'),
    ('^privacidad/', include('django.contrib.flatpages.urls')),
    ('^devolucion/', include('django.contrib.flatpages.urls')),
)
