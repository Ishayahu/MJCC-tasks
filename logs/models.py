# -*- coding:utf-8 -*-
# coding=<utf8>

from django.db import models

# Модели для логирования действий пользователей с активами
class Logging(models.Model):
    user = models.CharField(max_length=140)
    request = models.TextField(blank = True, null = True)
    goal = models.TextField(blank = True, null = True)
    done = models.BooleanField(default=False)
    datetime = models.DateTimeField()
    def __unicode__(self):
        return str(self.id)+';'.join((str(self.datetime),self.user,self.goal,str(self.done)))  