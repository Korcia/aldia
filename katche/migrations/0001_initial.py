# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Pagina'
        db.create_table(u'katche_pagina', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('fecha_creacion', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'katche', ['Pagina'])

        # Adding model 'Ficha'
        db.create_table(u'katche_ficha', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('titulo', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('imagen', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('texto', self.gf('django.db.models.fields.TextField')()),
            ('texto_html', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('fecha_creacion', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('pagina', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['katche.Pagina'], to_field='nombre')),
        ))
        db.send_create_signal(u'katche', ['Ficha'])


    def backwards(self, orm):
        # Deleting model 'Pagina'
        db.delete_table(u'katche_pagina')

        # Deleting model 'Ficha'
        db.delete_table(u'katche_ficha')


    models = {
        u'katche.ficha': {
            'Meta': {'ordering': "['nombre']", 'object_name': 'Ficha'},
            'fecha_creacion': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imagen': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'nombre': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'pagina': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['katche.Pagina']", 'to_field': "'nombre'"}),
            'texto': ('django.db.models.fields.TextField', [], {}),
            'texto_html': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'titulo': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'katche.pagina': {
            'Meta': {'ordering': "['nombre']", 'object_name': 'Pagina'},
            'fecha_creacion': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'})
        }
    }

    complete_apps = ['katche']