from django.contrib import admin

from coltrane.models import Resumen


class ResumenAdmin(admin.ModelAdmin):
    #class Media:
    #    js = ('/static/js/tiny_mce/tiny_mce.js', '/static/js/textareas.js')
    prepopulated_fields = { 'slug': ['titulo'] }

admin.site.register(Resumen, ResumenAdmin)
