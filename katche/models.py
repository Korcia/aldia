#coding=UTF-8
from django.db import models
from markdown import markdown

class Pagina(models.Model):
    """ clase que contiene información sobre la página a la que irán asociadas un grupo de fichas """ 
    nombre = models.CharField(max_length=50, unique=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['nombre']
        
    def __unicode__(self):
        return self.nombre

class Ficha(models.Model):
    """ clase que contiene información sobre una ficha"""
    nombre = models.CharField(max_length=100, unique=True)
    titulo = models.CharField(max_length=100)
    imagen = models.ImageField(upload_to='fichas')
    texto = models.TextField()
    texto_html = models.TextField(editable=False, blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    pagina = models.ForeignKey(Pagina, to_field="nombre")
    
    
    #objects = models.Manager()
    
    class Meta:
        ordering = ['nombre']
    
    def __unicode__(self):
        return self.nombre

    #def save(self, force_insert=False, force_update=False):
    def save(self, *args, **kwargs):
        self.texto_html = markdown(self.texto)
        #super(Ficha, self).save(force_insert, force_update)
        super(Ficha, self).save(*args, **kwargs)
    