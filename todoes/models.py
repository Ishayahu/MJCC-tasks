# -*- coding:utf-8 -*-
# coding=<utf8>

from django.db import models

# Create your models here.

# blank = True, null = True
    
class ProblemByUser(models.Model):
    name = models.TextField()
    def __unicode__(self):
        return self.name
    class Meta:
        ordering = ['name',]

class ProblemByWorker(models.Model):
    name = models.TextField()
    def __unicode__(self):
        return self.name
    class Meta:
        ordering = ['name',]

class Categories(models.Model):
    name = models.TextField()
    def __unicode__(self):
        # return u';'.join((str(self.id),self.name))
        return self.name

        
class Note(models.Model):
    timestamp = models.DateTimeField()
    note = models.TextField()
    author = models.ForeignKey('Person',blank = True, null = True)
    children_note = models.ManyToManyField('Note',related_name = "parent_note",blank = True, null = True)
    def __unicode__(self):
        return self.note

class Resource(models.Model):
    name = models.CharField(max_length=140)
    description = models.TextField()

class File(models.Model):
    timestamp = models.DateTimeField()
    file_name = models.CharField(max_length=140)
    file = models.FileField(upload_to='task_files') # add separation by tasks
    description = models.TextField()
    class Meta:
        ordering = ['timestamp']
    def __unicode__(self):
        return str(self.id)+" "+self.file_name
    @models.permalink
    def get_absolute_url(self):
        return ('todoes.views.test_task',('one_time',self.id),{})
        # return ('food.views.restaurant_details', (), {'restaurant_id': [str(self.id)]})
        # return ('food.views.restaurant_details', (str(self.id),), {})

class Person(models.Model):
    fio = models.CharField(max_length=140)
    tel = models.CharField(max_length=10)
    mail = models.EmailField(blank = True, null = True)
    raiting = models.CharField(max_length=30, blank = True, null = True)
    login = models.CharField(max_length=140, blank = True, null = True)
    def __unicode__(self):
        return ";".join((self.fio,str(self.login)))
    class Meta:
        ordering = ['fio',]

class Task(models.Model):
    name = models.CharField(max_length=140)
    description = models.TextField()
    # client = models.ForeignKey(Client)
    priority = models.PositiveSmallIntegerField()
    category = models.ForeignKey(Categories)
    start_date = models.DateTimeField()
    due_date = models.DateTimeField()
    done_date = models.DateTimeField(blank = True, null = True)
    when_to_reminder = models.DateTimeField()
    # worker = models.ForeignKey(Worker)
    #worker = models.ForeignKey(Person, related_name = "worker_for_task",blank = True, null = True)
    #client = models.ForeignKey(Person, related_name = "client_for_task",blank = True, null = True)
    worker = models.ForeignKey(Person)
    client = models.ForeignKey(Person)
    resource = models.ForeignKey(Resource, blank = True, null = True)
    note = models.ManyToManyField(Note, related_name = "for_task",blank = True, null = True)
    file = models.ForeignKey(File, related_name = "for_task", blank = True, null = True)
    percentage = models.PositiveSmallIntegerField()
    pbu = models.ForeignKey(ProblemByUser)
    pbw = models.ForeignKey(ProblemByWorker,blank = True, null = True)
    confirmed = models.BooleanField(default=False)
    confirmed_date = models.DateTimeField(blank = True, null = True)
    children_task = models.ManyToManyField('Task',related_name = "parent_task",blank = True, null = True)
    deleted = models.BooleanField(default=False)
    acl = models.TextField(default=False)
    def __unicode__(self):
        return u";".join((str(self.id),self.name,"\t"+self.worker.fio))
    class Meta:
        ordering = ['priority','due_date']
        
class RegularTask(models.Model):
    name = models.CharField(max_length=140)
    description = models.TextField(blank = True, null = True)
    priority = models.PositiveSmallIntegerField()
    category = models.ForeignKey(Categories)
    start_date = models.DateTimeField()
    stop_date = models.DateTimeField(blank = True, null = True)
    next_date = models.DateTimeField()
    when_to_reminder = models.DateTimeField()
    worker = models.ForeignKey(Person, related_name = "worker_for_regular_task",blank = True, null = True)
    client = models.ForeignKey(Person, related_name = "client_for_regular_task",blank = True, null = True)
    resource = models.ForeignKey(Resource, blank = True, null = True)
    note = models.ManyToManyField(Note, related_name = "for_regular_task",blank = True, null = True)
    file = models.ForeignKey(File,related_name = "for_regular_task", blank = True, null = True)
    children_task = models.ManyToManyField('Task',related_name = "parent_regular_task",blank = True, null = True)
    deleted = models.BooleanField(default=False)
    acl = models.TextField(default=False)
    period = models.TextField()
    def __unicode__(self):
        return u";".join((str(self.id),self.name,"\t"+self.worker.fio))
    class Meta:
        ordering = ['priority','next_date']
        
class Joker(models.Model):
    name = models.CharField(max_length=140)
    link = models.URLField()
    def __unicode__(self):
        return ";".join((self.name,self.link))
    
class Joker_Visit(models.Model):
    worker = models.ForeignKey(Person)
    joker = models.ForeignKey(Joker)

class Activity(models.Model):
    login = models.CharField(max_length=140, blank = True, null = True)
    last_page = models.CharField(max_length=200)
    timestamp = models.DateTimeField()
    def __unicode__(self):
        return u";".join((str(self.id),self.login,self.last_page,str(self.timestamp)))
    class Meta:
        ordering = ['-timestamp',]