# -*- coding:utf-8 -*-
# coding=<utf8>

from django.db import models

STATUSES = ((0, 'OK'),
            (1, 'INFO'),
            (2, 'WARNING'),
            (3, 'ERROR'))


# Модели для хранения статуса и сообщения к нему
class Status(models.Model):
    key = models.CharField(max_length=140)
    group = models.CharField(max_length=140)
    source = models.TextField(blank=True, null=True, max_length=140)
    status = models.PositiveSmallIntegerField(choices=STATUSES)
    message = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField()
    next_report = models.DateTimeField()
    def __unicode__(self):
        return u';'.join((str(self.id),
                              self.group,
                              self.key,
                              self.source,
                              str(self.status),
                              str(self.timestamp)))
#
# class Message(models.Model):
#     for_status = models.ForeignKey(Status,
#                                    related_name="message_for_status")
#     def __unicode__(self):
#         return str(self.id)+';'.join((str(self.for_status.id),
#                                       str(self.timestamp)))
