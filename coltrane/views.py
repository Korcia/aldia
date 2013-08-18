from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Resumen
from django.views.generic import dates
#from django.views.decorators.csrf import csrf_exempt


class PrivadoResumenDetail(dates.DateDetailView):
    slug_field = 'slug'
    date_field = 'fecha_publicacion'
    queryset = Resumen.live.all()
    month_format = '%m'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(PrivadoResumenDetail, self).dispatch(request, *args, **kwargs)

class PrivadoResumenYear(dates.YearArchiveView):
    date_field = 'fecha_publicacion'
    queryset = Resumen.live.all()

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(PrivadoResumenYear, self).dispatch(request, *args, **kwargs)

class PrivadoResumenMes(dates.MonthArchiveView):
    month_format = '%m'
    date_field = 'fecha_publicacion'
    queryset = Resumen.live.all()

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(PrivadoResumenMes, self).dispatch(request, *args, **kwargs)

class PrivadoResumenDia(dates.DayArchiveView):
    month_format = '%m'
    date_field = 'fecha_publicacion'
    queryset = Resumen.live.all()

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(PrivadoResumenDia, self).dispatch(request, *args, **kwargs)

class PrivadoResumenLista(dates.ArchiveIndexView):
    date_field = 'fecha_publicacion'
    queryset = Resumen.live.all()
    paginate_by = 10

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(PrivadoResumenLista, self).dispatch(request, *args, **kwargs)
