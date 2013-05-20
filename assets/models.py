# -*- coding:utf-8 -*-
# coding=<utf8>

from django.db import models

# Модели для подключения активов

class Asset(models.Model):
    asset_type = models.ForeignKey('Asset_types')
    payment
    date_of_write_off
    garanty
    current_place
    model
    status
    claim
    
    
    
    
"""    name = models.CharField(max_length=140)
    description = models.TextField()
    # client = models.ForeignKey(Client)
    priority = models.PositiveSmallIntegerField()
    category = models.ForeignKey(Categories)
    start_date = models.DateTimeField()
    due_date = models.DateTimeField()
    done_date = models.DateTimeField(blank = True, null = True)
    when_to_reminder = models.DateTimeField()
    # worker = models.ForeignKey(Worker)
    worker = models.ForeignKey(Person, related_name = "worker_for_task",blank = True, null = True)
    client = models.ForeignKey(Person, related_name = "client_for_task",blank = True, null = True)
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
"""