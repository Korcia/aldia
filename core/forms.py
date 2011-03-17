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
    keywords = forms.CharField(label='Palabras Clave', max_length=40, required=False, widget=forms.TextInput(attrs={'size':'30'}))
    fecha_periodo = forms.ChoiceField(label='Periodo de Busqueda', choices=RADIO_PERIODO_CHOICES)
    def clean_keywords(self):
        keywords = self.cleaned_data['keywords']
        if not re.search(r'^\w+$', keywords):
            raise forms.ValidationError(u'Las palabras solo pueden tener caracteres alfanumericos y guion bajo.')
