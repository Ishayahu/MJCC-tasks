# encoding: utf-8
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def forwards(self, orm):
        db.rename_column('todoes_task', 'when_to_remember', 'when_to_reminder')
        for task in orm.Task.objects.all():
            print task.id
            task.when_to_reminder = task.start_date
            task.save()


    def backwards(self, orm):
        raise RuntimeError("Just delete todoes_person table.")


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
            'Meta': {'ordering': "['fio']", 'object_name': 'Person'},
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
            'when_to_remember': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'worker': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'worker_for_task'", 'null': 'True', 'to': "orm['todoes.Person']"})
        }
    }

    complete_apps = ['todoes']
