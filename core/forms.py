#coding=UTF-8

from django import forms
import re

class SearchFormKeyword(forms.Form):
    RADIO_PERIODO_CHOICES = (
        ('DI', 'Diario'),
        ('SE', 'Semanal'),
        ('ME', 'Mensual'),
        ('AN', 'Anual'),
    )
    keywords = forms.CharField(max_length=40, required=False, widget=forms.TextInput(attrs={'size':'14'}))
    fecha_periodo = forms.ChoiceField(label='Periodo de Busqueda', choices=RADIO_PERIODO_CHOICES)
    def clean_keywords(self):
        keywords = self.cleaned_data['keywords']
        if not re.search(r'^\w+$', keywords):
            raise forms.ValidationError(u'Las palabras solo pueden tener caracteres alfanumericos y guion bajo.')

class ContactForm(forms.Form):
    TIPO_CHOICES = (
        ('', '--- Elija tipo de asunto ---'),
        ('SUGERENCIA', 'Sugerencias'),
        ('INFORMACIÓN', 'Información'),
        ('PROBLEMAS', 'Problemas'),
        ('OTROS', 'Otros'),
    )
    tipo = forms.ChoiceField(label='', choices=TIPO_CHOICES)    
    asunto = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'size':'30'}))
    email = forms.EmailField(required=False, max_length=30, widget=forms.TextInput(attrs={'size':'25'}))
    mensaje = forms.CharField(widget=forms.Textarea(attrs={'cols':'35','rows':'10' }), max_length=200)

class RegistroForm(forms.Form):
    email = forms.EmailField(required=False, max_length=30, widget=forms.TextInput(attrs={'size':'25'}))
    mensaje = forms.CharField(widget=forms.Textarea(attrs={'cols':'35','rows':'10' }), max_length=200)
