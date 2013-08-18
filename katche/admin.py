from django.contrib import admin

from katche.models import Pagina, Ficha


class FichaAdmin(admin.ModelAdmin):
    #class Media:
    #    js = ('/static/js/tiny_mce/tiny_mce.js', '/static/js/textareas.js')
    pass

admin.site.register(Ficha, FichaAdmin)

class PaginaAdmin(admin.ModelAdmin):
    #class Media:
    #    js = ('/static/js/tiny_mce/tiny_mce.js', '/static/js/textareas.js')
    pass

admin.site.register(Pagina, PaginaAdmin)
