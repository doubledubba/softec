# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Agent'
        db.create_table(u'notifications_agent', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('startHours', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('endHours', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, blank=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=11, blank=True)),
        ))
        db.send_create_signal(u'notifications', ['Agent'])

        # Adding model 'Owner'
        db.create_table(u'notifications_owner', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('startHours', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('endHours', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, blank=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=11, blank=True)),
        ))
        db.send_create_signal(u'notifications', ['Owner'])

        # Adding model 'Restaurant'
        db.create_table(u'notifications_restaurant', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('startHours', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('endHours', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=11, blank=True)),
            ('refusalMsg', self.gf('django.db.models.fields.CharField')(max_length=80, null=True, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True, blank=True)),
            ('notes', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('alert', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'notifications', ['Restaurant'])

        # Adding M2M table for field agents on 'Restaurant'
        m2m_table_name = db.shorten_name(u'notifications_restaurant_agents')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('restaurant', models.ForeignKey(orm[u'notifications.restaurant'], null=False)),
            ('agent', models.ForeignKey(orm[u'notifications.agent'], null=False))
        ))
        db.create_unique(m2m_table_name, ['restaurant_id', 'agent_id'])

        # Adding M2M table for field owners on 'Restaurant'
        m2m_table_name = db.shorten_name(u'notifications_restaurant_owners')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('restaurant', models.ForeignKey(orm[u'notifications.restaurant'], null=False)),
            ('owner', models.ForeignKey(orm[u'notifications.owner'], null=False))
        ))
        db.create_unique(m2m_table_name, ['restaurant_id', 'owner_id'])

        # Adding model 'Computer'
        db.create_table(u'notifications_computer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('cid', self.gf('django.db.models.fields.IntegerField')(default=0, null=True, blank=True)),
        ))
        db.send_create_signal(u'notifications', ['Computer'])


    def backwards(self, orm):
        # Deleting model 'Agent'
        db.delete_table(u'notifications_agent')

        # Deleting model 'Owner'
        db.delete_table(u'notifications_owner')

        # Deleting model 'Restaurant'
        db.delete_table(u'notifications_restaurant')

        # Removing M2M table for field agents on 'Restaurant'
        db.delete_table(db.shorten_name(u'notifications_restaurant_agents'))

        # Removing M2M table for field owners on 'Restaurant'
        db.delete_table(db.shorten_name(u'notifications_restaurant_owners'))

        # Deleting model 'Computer'
        db.delete_table(u'notifications_computer')


    models = {
        u'notifications.agent': {
            'Meta': {'object_name': 'Agent'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'endHours': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '11', 'blank': 'True'}),
            'startHours': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        u'notifications.computer': {
            'Meta': {'object_name': 'Computer'},
            'cid': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'})
        },
        u'notifications.owner': {
            'Meta': {'object_name': 'Owner'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'endHours': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '11', 'blank': 'True'}),
            'startHours': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        u'notifications.restaurant': {
            'Meta': {'object_name': 'Restaurant'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'address': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'agents': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['notifications.Agent']", 'symmetrical': 'False', 'blank': 'True'}),
            'alert': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'endHours': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'owners': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['notifications.Owner']", 'symmetrical': 'False', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '11', 'blank': 'True'}),
            'refusalMsg': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True', 'blank': 'True'}),
            'startHours': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '80'})
        }
    }

    complete_apps = ['notifications']