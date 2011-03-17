#coding=UTF-8
import os.path

from django.conf.urls.defaults import *
from core.views import main_page
from django.contrib import admin
admin.autodiscover()
static = os.path.join(os.path.dirname(__file__), 'static')

urlpatterns = patterns('',
    (r'^$', main_page),
    (r'^resumenes/', include('jarrett.urls.resumenes')),
    (r'^admin/', include(admin.site.urls)),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': static}),
)
