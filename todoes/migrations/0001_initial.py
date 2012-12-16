# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'ProblemByUser'
        db.create_table('todoes_problembyuser', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('todoes', ['ProblemByUser'])

        # Adding model 'ProblemByWorker'
        db.create_table('todoes_problembyworker', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('todoes', ['ProblemByWorker'])

        # Adding model 'Categories'
        db.create_table('todoes_categories', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('todoes', ['Categories'])

        # Adding model 'Note'
        db.create_table('todoes_note', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')()),
            ('note', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('todoes', ['Note'])

        # Adding model 'Resource'
        db.create_table('todoes_resource', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('description', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('todoes', ['Resource'])

        # Adding model 'File'
        db.create_table('todoes_file', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')()),
            ('file_name', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('todoes', ['File'])

        # Adding model 'Worker'
        db.create_table('todoes_worker', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('fio', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('tel', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('mail', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True, blank=True)),
            ('raiting', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('login', self.gf('django.db.models.fields.CharField')(max_length=140, null=True, blank=True)),
        ))
        db.send_create_signal('todoes', ['Worker'])

        # Adding model 'Client'
        db.create_table('todoes_client', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('fio', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('tel', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('mail', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True, blank=True)),
            ('raiting', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('login', self.gf('django.db.models.fields.CharField')(max_length=140, null=True, blank=True)),
        ))
        db.send_create_signal('todoes', ['Client'])

        # Adding model 'Task'
        db.create_table('todoes_task', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('client', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['todoes.Client'])),
            ('priority', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['todoes.Categories'])),
            ('start_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('due_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('done_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('worker', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['todoes.Worker'])),
            ('resource', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['todoes.Resource'], null=True, blank=True)),
            ('file', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['todoes.File'], null=True, blank=True)),
            ('percentage', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('pbu', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['todoes.ProblemByUser'])),
            ('pbw', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['todoes.ProblemByWorker'], null=True, blank=True)),
            ('confirmed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('confirmed_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal('todoes', ['Task'])

        # Adding M2M table for field note on 'Task'
        db.create_table('todoes_task_note', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('task', models.ForeignKey(orm['todoes.task'], null=False)),
            ('note', models.ForeignKey(orm['todoes.note'], null=False))
        ))
        db.create_unique('todoes_task_note', ['task_id', 'note_id'])

        # Adding model 'Joker'
        db.create_table('todoes_joker', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('link', self.gf('django.db.models.fields.URLField')(max_length=200)),
        ))
        db.send_create_signal('todoes', ['Joker'])

        # Adding model 'Joker_Visit'
        db.create_table('todoes_joker_visit', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('worker', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['todoes.Worker'])),
            ('joker', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['todoes.Joker'])),
        ))
        db.send_create_signal('todoes', ['Joker_Visit'])


    def backwards(self, orm):
        
        # Deleting model 'ProblemByUser'
        db.delete_table('todoes_problembyuser')

        # Deleting model 'ProblemByWorker'
        db.delete_table('todoes_problembyworker')

        # Deleting model 'Categories'
        db.delete_table('todoes_categories')

        # Deleting model 'Note'
        db.delete_table('todoes_note')

        # Deleting model 'Resource'
        db.delete_table('todoes_resource')

        # Deleting model 'File'
        db.delete_table('todoes_file')

        # Deleting model 'Worker'
        db.delete_table('todoes_worker')

        # Deleting model 'Client'
        db.delete_table('todoes_client')

        # Deleting model 'Task'
        db.delete_table('todoes_task')

        # Removing M2M table for field note on 'Task'
        db.delete_table('todoes_task_note')

        # Deleting model 'Joker'
        db.delete_table('todoes_joker')

        # Deleting model 'Joker_Visit'
        db.delete_table('todoes_joker_visit')


    models = {
        'todoes.categories': {
            'Meta': {'object_name': 'Categories'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {})
        },
        'todoes.client': {
            'Meta': {'object_name': 'Client'},
            'fio': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'login': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'mail': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'raiting': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'tel': ('django.db.models.fields.CharField', [], {'max_length': '10'})
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
            'worker': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['todoes.Worker']"})
        },
        'todoes.note': {
            'Meta': {'object_name': 'Note'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'note': ('django.db.models.fields.TextField', [], {}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {})
        },
        'todoes.problembyuser': {
            'Meta': {'object_name': 'ProblemByUser'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {})
        },
        'todoes.problembyworker': {
            'Meta': {'object_name': 'ProblemByWorker'},
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
            'Meta': {'ordering': "['priority', '-due_date']", 'object_name': 'Task'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['todoes.Categories']"}),
            'client': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['todoes.Client']"}),
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
            'worker': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['todoes.Worker']"})
        },
        'todoes.worker': {
            'Meta': {'object_name': 'Worker'},
            'fio': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'login': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'mail': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'raiting': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'tel': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        }
    }

    complete_apps = ['todoes']
