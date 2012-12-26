# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting model 'Client'
        # db.delete_table('todoes_client')

        # Deleting model 'Worker'
        # db.delete_table('todoes_worker')
        # Rename 'name' field to 'full_name'
        db.rename_column('todoes_task', 'worker_new_id', 'worker_id')
        db.rename_column('todoes_task', 'client_new_id', 'client_id')
        
        # Deleting field 'Task.client_new'
        # db.delete_column('todoes_task', 'client_new_id')

        # Deleting field 'Task.worker_new'
        # db.delete_column('todoes_task', 'worker_new_id')

        # Adding field 'Task.worker'
        # db.add_column('todoes_task', 'worker', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='worker_for_task', null=True, to=orm['todoes.Person']), keep_default=False)

        # Adding field 'Task.client'
        # db.add_column('todoes_task', 'client', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='client_for_task', null=True, to=orm['todoes.Person']), keep_default=False)


    def backwards(self, orm):
        
        # Adding model 'Client'
        db.create_table('todoes_client', (
            ('tel', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('mail', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True, blank=True)),
            ('login', self.gf('django.db.models.fields.CharField')(max_length=140, null=True, blank=True)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('raiting', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('fio', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('todoes', ['Client'])

        # Adding model 'Worker'
        db.create_table('todoes_worker', (
            ('tel', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('raiting', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('mail', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True, blank=True)),
            ('login', self.gf('django.db.models.fields.CharField')(max_length=140, null=True, blank=True)),
            ('fio', self.gf('django.db.models.fields.CharField')(max_length=140)),
        ))
        db.send_create_signal('todoes', ['Worker'])

        # Adding field 'Task.client_new'
        db.add_column('todoes_task', 'client_new', self.gf('django.db.models.fields.related.ForeignKey')(related_name='client_for_task', null=True, to=orm['todoes.Person'], blank=True), keep_default=False)

        # Adding field 'Task.worker_new'
        db.add_column('todoes_task', 'worker_new', self.gf('django.db.models.fields.related.ForeignKey')(related_name='worker_for_task', null=True, to=orm['todoes.Person'], blank=True), keep_default=False)

        # Deleting field 'Task.worker'
        db.delete_column('todoes_task', 'worker_id')

        # Deleting field 'Task.client'
        db.delete_column('todoes_task', 'client_id')


    models = {
        'todoes.categories': {
            'Meta': {'object_name': 'Categories'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {})
        },
        'todoes.file': {
            'Meta': {'object_name': 'File'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'file_name': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {})
        },
        'todoes.joker': {
            'Meta': {'object_name': 'Joker'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '140'})
        },
        'todoes.joker_visit': {
            'Meta': {'object_name': 'Joker_Visit'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'joker': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['todoes.Joker']"}),
            'worker': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['todoes.Person']"})
        },
        'todoes.note': {
            'Meta': {'object_name': 'Note'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'note': ('django.db.models.fields.TextField', [], {}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {})
        },
        'todoes.person': {
            'Meta': {'object_name': 'Person'},
            'fio': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'login': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'mail': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'raiting': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'tel': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        'todoes.problembyuser': {
            'Meta': {'ordering': "['name']", 'object_name': 'ProblemByUser'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {})
        },
        'todoes.problembyworker': {
            'Meta': {'ordering': "['name']", 'object_name': 'ProblemByWorker'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {})
        },
        'todoes.resource': {
            'Meta': {'object_name': 'Resource'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '140'})
        },
        'todoes.task': {
            'Meta': {'ordering': "['priority', 'due_date']", 'object_name': 'Task'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['todoes.Categories']"}),
            'children_task': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'parent_task'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['todoes.Task']"}),
            'client': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'client_for_task'", 'null': 'True', 'to': "orm['todoes.Person']"}),
            'confirmed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'confirmed_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'done_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'due_date': ('django.db.models.fields.DateTimeField', [], {}),
            'file': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['todoes.File']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'note': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'for_task'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['todoes.Note']"}),
            'pbu': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['todoes.ProblemByUser']"}),
            'pbw': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['todoes.ProblemByWorker']", 'null': 'True', 'blank': 'True'}),
            'percentage': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'priority': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'resource': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['todoes.Resource']", 'null': 'True', 'blank': 'True'}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {}),
            'worker': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'worker_for_task'", 'null': 'True', 'to': "orm['todoes.Person']"})
        }
    }

    complete_apps = ['todoes']
