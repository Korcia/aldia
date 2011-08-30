from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^ultimo/$', 'moviles.views.ultimo'),
    (r'^archivos/$', 'moviles.views.archivo'),
    #(r'^([A-Z0-9])/$', 'pda.bands.views.bands_letter'),
)
