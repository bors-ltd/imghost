# -*- coding: utf-8 -*-
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Tag'
        db.create_table(u'images_tag', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=256)),
        ))
        db.send_create_signal(u'images', ['Tag'])

        # Adding M2M table for field tags on 'Image'
        m2m_table_name = db.shorten_name(u'images_image_tags')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('image', models.ForeignKey(orm[u'images.image'], null=False)),
            ('tag', models.ForeignKey(orm[u'images.tag'], null=False))
        ))
        db.create_unique(m2m_table_name, ['image_id', 'tag_id'])

    def backwards(self, orm):
        # Deleting model 'Tag'
        db.delete_table(u'images_tag')

        # Removing M2M table for field tags on 'Image'
        db.delete_table(db.shorten_name(u'images_image_tags'))

    models = {
        u'images.image': {
            'Meta': {'ordering': "(u'-created_on',)", 'object_name': 'Image'},
            'created_on': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'extension': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '5', 'blank': 'True'}),
            'height': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'is_meme': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'source': ('django.db.models.fields.URLField', [], {'max_length': '2048', 'null': 'True', 'blank': 'True'}),
            'source_image': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'related_memes'", 'null': 'True', 'to': u"orm['images.Image']"}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "u'tags'", 'symmetrical': 'False', 'to': u"orm['images.Tag']"}),
            'thumb_large': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'thumb_small': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'unique_key': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20', 'blank': 'True'}),
            'width': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'blank': 'True'})
        },
        u'images.tag': {
            'Meta': {'object_name': 'Tag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '256'})
        }
    }

    complete_apps = ['images']