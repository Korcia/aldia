from django.contrib.auth.decorators import login_required
from django.views.generic.date_based import archive_index,archive_year,archive_month,archive_day,object_detail
#from django.views.decorators.csrf import csrf_exempt

@login_required
def limited_archive_index(*args, **kwargs):
    return archive_index(*args, **kwargs)
@login_required
def limited_archive_year(*args, **kwargs):
    return archive_year(*args, **kwargs)
@login_required
def limited_archive_month(*args, **kwargs):
    return archive_month(*args, **kwargs)
@login_required
def limited_archive_day(*args, **kwargs):
    return archive_day(*args, **kwargs)
@login_required
def limited_object_detail(*args, **kwargs):
    return object_detail(*args, **kwargs)
