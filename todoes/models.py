# -*- coding:utf-8 -*-
# coding=<utf8>

from django.db import models
import datetime

__version__ = '0.0.1'

    
class ProblemByUser(models.Model):
    name = models.TextField()

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name', ]


class ProblemByWorker(models.Model):
    name = models.TextField()
    weight = models.FloatField(default=0)
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        ordering = ['name', ]


class Categories(models.Model):
    name = models.TextField()

    def __unicode__(self):
        return self.name

        
class Note(models.Model):
    timestamp = models.DateTimeField()
    note = models.TextField()
    author = models.ForeignKey('Person', blank=True, null=True)
    children_note = models.ManyToManyField('Note',
                                           related_name="parent_note",
                                           blank=True)
    
    def __unicode__(self):
        return self.note


class Resource(models.Model):
    name = models.CharField(max_length=140)
    description = models.TextField()


class File(models.Model):
    timestamp = models.DateTimeField()
    file_name = models.CharField(max_length=140)
    # add separation by tasks
    file = models.FileField(upload_to='task_files')
    description = models.TextField()
    
    class Meta:
        ordering = ['timestamp']
        
    def __unicode__(self):
        return unicode(self.id)+u" "+self.file_name
    
    @models.permalink
    def get_absolute_url(self):
        return ('todoes.views.task', ('one_time', self.id), {})


class Person(models.Model):
    fio = models.CharField(max_length=140)
    tel = models.CharField(max_length=10)
    mail = models.EmailField(blank=True, null=True)
    level = models.PositiveSmallIntegerField(default=0)
    boss = models.ForeignKey('Person', blank=True, null=True)
    raiting = models.CharField(max_length=30, blank=True, null=True)
    login = models.CharField(max_length=140, blank=True, null=True)

    def __unicode__(self):
        return ";".join((self.fio, str(self.login)))

    class Meta:
        ordering = ['fio', ]


class Task(models.Model):
    name = models.CharField(max_length=140)
    description = models.TextField()
    priority = models.PositiveSmallIntegerField()
    category = models.ForeignKey(Categories)
    start_date = models.DateTimeField()
    # к какой дате сделать
    due_date = models.DateTimeField()
    # поля для решения конфликтов по срокам выполнения задачи
    due_date_editor_level = models.PositiveSmallIntegerField(
        default=99)
    request_due_date = models.DateTimeField(blank=True, null=True)
    due_date_request_reason = models.TextField(blank=True, null=True)
    # поля для эскалации вопроса
    escalated_to = models.ManyToManyField(Person,
                                          blank=True)
    reason_to_escalation = models.TextField(blank=True)
    escalation_timestamp = models.DateTimeField(blank=True, null=True)
    # когда сделано
    done_date = models.DateTimeField(blank=True, null=True)
    when_to_reminder = models.DateTimeField()
    worker = models.ForeignKey(Person, related_name="worker_for_task")
    client = models.ForeignKey(Person, related_name="client_for_task")
    resource = models.ForeignKey(Resource, blank=True, null=True)
    note = models.ManyToManyField(Note, related_name="for_task",
                                  blank=True)
    notifications = models.TextField(blank=True, null=True)
    file = models.ManyToManyField(File, related_name="for_task",
                                  blank=True)
    percentage = models.PositiveSmallIntegerField()
    pbu = models.ForeignKey(ProblemByUser)
    pbw = models.ForeignKey(ProblemByWorker, blank=True, null=True)
    confirmed = models.BooleanField(default=False)
    confirmed_date = models.DateTimeField(blank=True, null=True)
    children_task = models.ManyToManyField('Task',
                                           related_name="parent_task",
                                           blank=True)
    deleted = models.BooleanField(default=False)
    acl = models.TextField(default=False)
    # история изменений
    temp_change_history = models.TextField(blank=True, null=True)
    change_history = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return u";".join((unicode(self.id),
                          self.name,
                          u"\t"+self.worker.fio))

    class Meta:
        ordering = ['priority', 'due_date']

    def build_history(self):
        # """
        # Формат записи истории такой:
        # |||user||timestamp||record1||record2|||
        # record:
        # key|old_val|new_val
        # """
        # class HistoryRecord:
        #     def __init__(self, record):
        #         temp = record.split(u'||')
        #         self.user = temp[0]
        #         self.timestamp = temp[1]
        #         self.items = []
        #         self.length = len(temp[2:])
        #         for number, item in enumerate(temp[2:]):
        #             self.items.append(HistoryItem(number, item))
        #
        # class HistoryItem:
        #     def __init__(self, number, item):
        #         self.key, self.old_value, self.new_value =\
        #             item.split('|')
        #         self.number = number
        #
        # if self.change_history:
        #     records = self.change_history.split(u'|||')
        #     res = []
        #     for record in records:
        #         if record:
        #             res.append(HistoryRecord(record))
        #     self.history = res
        # else:
        #     self.history = None
        pass
# TODO: ошибка при создании новой задачи
#     def save(self, *args, **kwargs):
#         """
#         Формат записи истории такой:
#         |||user||timestamp||record1||record2|||
#         record:
#         key|old_val|new_val
#         """
#         user = kwargs.pop('user', None)
# #         if user is not None:
# #             if self.temp_change_history:
# #                 if self.temp_change_history[:2] == u'||':
# #                     self.temp_change_history =\
# #                         self.temp_change_history[2:]
# #                     # чтобы не было
# # # |||ishayahu||2015-07-31 15:40:24.686081||||done_date|None|None||...
# #                 if self.change_history[-3:] != u'|||':
# #                         self.change_history += u'|||'
# #                 self.change_history += u'||'.join((
# #                                     unicode(user),
# #                                     unicode(datetime.datetime.now()),
# #                                     unicode(self.temp_change_history),
# #                 ))
# #                 self.temp_change_history = u''
#         super(Task, self).save(*args, **kwargs)
    def save(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(Task, self).save(*args, **kwargs)
#
#     def __setattr__(self, key, value):
#         """
#         Формат записи истории такой:
#         |||user||timestamp||record1||record2|||
#         record:
#         key|old_val|new_val
#         """
#         if key not in ('change_history', 'temp_change_history'):
#             # old_value = None
#             new_value = value
#             try:
#                 old_value = self.__dict__[key]
#                 if old_value != new_value:
#                     try:
#                         if self.__dict__['temp_change_history'][-2:]\
#                                 != u"||":
#                             self.__dict__['temp_change_history'] +=\
#                                 u'||'
#                     except (KeyError, TypeError):
#                         self.__dict__['temp_change_history'] = u''
#                     self.__dict__['temp_change_history'] +=\
#                         u'|'.join((
#                             unicode(key),
#                             unicode(old_value),
#                             unicode(new_value)
#                         ))
#             except KeyError:
#                 pass
#             self.__dict__[key] = value
#         else:
#             self.__dict__[key] = value


class RegularTask(models.Model):
    name = models.CharField(max_length=140)
    description = models.TextField(blank=True, null=True)
    priority = models.PositiveSmallIntegerField()
    category = models.ForeignKey(Categories)
    start_date = models.DateTimeField()
    stop_date = models.DateTimeField(blank=True, null=True)
    next_date = models.DateTimeField()
    when_to_reminder = models.DateTimeField()
    worker = models.ForeignKey(Person,
                               related_name="worker_for_regular_task",
                               blank=True, null=True)
    client = models.ForeignKey(Person,
                               related_name="client_for_regular_task",
                               blank=True, null=True)
    resource = models.ForeignKey(Resource, blank=True, null=True)
    note = models.ManyToManyField(Note,
                                  related_name="for_regular_task",
                                  blank=True)
    file = models.ManyToManyField(File,
                                  related_name="for_regular_task",
                                  blank=True)
    children_task = models.ManyToManyField('Task',
                                   related_name="parent_regular_task",
                                   blank=True)
    deleted = models.BooleanField(default=False)
    acl = models.TextField(default=False)
    period = models.TextField()

    def __unicode__(self):
        return u";".join((
            unicode(self.id),
            self.name,
            u"\t"+self.worker.fio))

    class Meta:
        ordering = ['priority', 'next_date']


class Message(models.Model):
    name = models.CharField(max_length=140)
    text = models.TextField()
    author = models.ForeignKey(Person, related_name="message_author")
    timestamp = models.DateTimeField()

    def __unicode__(self):
        return u';'.join((str(self.id), self.name, self.author.login))


class Message_Visit(models.Model):
    worker = models.ForeignKey(Person)
    message = models.ForeignKey(Message)

    def __unicode__(self):
        return u';'.join((str(self.id), self.message.name,
                          self.worker.login))


class Activity(models.Model):
    login = models.CharField(max_length=140, blank=True, null=True)
    last_page = models.CharField(max_length=200)
    timestamp = models.DateTimeField()

    def __unicode__(self):
        return u";".join((str(self.id),
                          self.login,
                          self.last_page,
                          str(self.timestamp)))

    class Meta:
        ordering = ['-timestamp', ]
