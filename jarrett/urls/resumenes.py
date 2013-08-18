from django.conf.urls.defaults import patterns, url
from django.views.generic.dates import ArchiveIndexView, YearArchiveView, MonthArchiveView, DayArchiveView, DateDetailView

from jarrett.models import Resumen


urlpatterns = patterns('',
    url(r'^$',
        ArchiveIndexView.as_view(
            date_field = 'fecha_publicacion',
            paginate_by = 15,
            allow_empty = True,
            queryset = Resumen.live.all()
        ),
        name='resumen_archivo'
    ),
     url(r'^(?P<year>\d{4})/$',
        YearArchiveView.as_view(
            date_field = 'fecha_publicacion',
            paginate_by= 15,
            allow_empty= True,
            queryset= Resumen.live.all()),
        name='resumen_year'),
     url(r'^(?P<year>\d{4})/(?P<month>\d{2})/$',
        MonthArchiveView.as_view(
            date_field= 'fecha_publicacion',
            month_format = '%m',
            paginate_by= 15,
            allow_empty= True,
            queryset= Resumen.live.all()),
        name='resumen_mes'),
     url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$',
        DayArchiveView.as_view(
            date_field= 'fecha_publicacion',
            month_format = '%m',
            paginate_by= 15,
            allow_empty= True,
            queryset= Resumen.live.all()),
        name='resumen_dia'),
     url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$',
        DateDetailView.as_view(
            slug_field = 'slug',
            date_field= 'fecha_publicacion',
            month_format = '%m',
            #model= Resumen),
            queryset= Resumen.live.all()),
        name='resumen-detalle'),
)
