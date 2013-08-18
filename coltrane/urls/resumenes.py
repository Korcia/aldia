from django.conf.urls.defaults import patterns, url
from coltrane.models import Resumen
from coltrane.views import PrivadoResumenLista, PrivadoResumenDia, PrivadoResumenMes, PrivadoResumenYear, PrivadoResumenDetail

urlpatterns = patterns('',
     url(r'^$',
        PrivadoResumenLista.as_view(),
        name = 'privado-resumen-archivo'
    ),
    url(r'^(?P<year>\d{4})/$',
        PrivadoResumenYear.as_view(),
        name = 'privado-resumen-year'
    ),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/$',
        PrivadoResumenMes.as_view(),
        name = 'privado-resumen-mes'
    ),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$',
        PrivadoResumenDia.as_view(),
        name = 'privado-resumen-dia'
    ),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$',
        PrivadoResumenDetail.as_view(),
        name = 'privado-resumen-detalle'
    ),
)
