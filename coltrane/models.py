#coding=UTF-8
import datetime
import locale
locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

from django.contrib.auth.models import User
from django.db import models
from django.db.models import permalink
from utils.views import get_weather 

#Define mapeo de digitos a numeración romana
romanNumeralMap = (('M',  1000),
                   ('CM', 900),
                   ('D',  500),
                   ('CD', 400),
                   ('C',  100),
                   ('XC', 90),
                   ('L',  50),
                   ('XL', 40),
                   ('X',  10),
                   ('IX', 9),
                   ('V',  5),
                   ('IV', 4),
                   ('I',  1))

class LiveResumenManager(models.Manager):
    def get_query_set(self):
        return super(LiveResumenManager, self).get_query_set().filter(status=self.model.LIVE_STATUS)

class PrivadoResumenManager(models.Manager):
    def get_query_set(self):
        return super(PrivadoResumenManager, self).get_query_set().filter(status=self.model.HIDDEN_STATUS)

class Resumen(models.Model):
    LIVE_STATUS = 1
    DRAFT_STATUS = 2
    HIDDEN_STATUS = 3
    STATUS_CHOICES = (
        (LIVE_STATUS, 'Publico'),
        (DRAFT_STATUS, 'Draft'),
        (HIDDEN_STATUS, 'Privado'),
    )

    # Core fields.
    titulo = models.CharField(max_length=250,
                             help_text="Máximo 250 caracteres.")
    contenido = models.TextField()
    fecha_publicacion = models.DateTimeField(default=datetime.datetime.now)
    autor = models.ForeignKey(User, related_name='+')
    slug = models.SlugField(unique_for_date='fecha_publicacion',
                            help_text="Valor sugerido generado automaticamente por el título. Debe ser único para la fecha de publicación.")
    status = models.IntegerField(choices=STATUS_CHOICES, default=LIVE_STATUS,
                                 help_text="Sólo noticias con estado Publica serán mostradas.")
    num_romano = models.CharField(max_length=20)
    tiempo = models.TextField(blank=True)

    objects = models.Manager()
    live = LiveResumenManager()
    privado = PrivadoResumenManager()

    class Meta:
        ordering = ['-fecha_publicacion']
        verbose_name_plural = "Resúmenes"

    def __unicode__(self):
        return self.titulo

    def crear_slug_unico(self):
        if not len(self.slug.strip()):
            year = self.fecha_publicacion.strftime("%Y")
            month = self.fecha_publicacion.strftime("%b").lower()
            day = self.fecha_publicacion.strftime("%d")
            self.slug = 'lpdh-' + day + '-' + month +'-' + year

    def fecha_to_roman(self):
        year = self.fecha_publicacion.strftime("%Y")
        numero = year[2:]
        n = int(numero)
        if not (0 < n < 5000):
            self.num_romano = "LPDH"
        if int(n) <> n:
            self.num_romano = "LPDH"
        resultado = ""
        for numeral, integer in romanNumeralMap:
            while n >= integer:
                resultado += numeral
                n -= integer
        self.num_romano = resultado
        
    def save(self, force_insert=False, force_update=False):
        self.tiempo = get_weather()
        self.crear_slug_unico()
        self.fecha_to_roman()
        super(Resumen, self).save(force_insert, force_update)

    @permalink
    def get_absolute_url(self):
        return ('coltrane_resumen_detail', (), { 'year': self.fecha_publicacion.strftime("%Y"),
                                               'month': self.fecha_publicacion.strftime("%b").lower(),
                                               'day': self.fecha_publicacion.strftime("%d"),
                                               'slug': self.slug })
