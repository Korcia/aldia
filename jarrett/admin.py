from django.contrib import admin

from jarrett.models import Resumen


class ResumenAdmin(admin.ModelAdmin):
    prepopulated_fields = { 'slug': ['titulo'] }

admin.site.register(Resumen, ResumenAdmin)
