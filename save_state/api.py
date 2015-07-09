# -*- coding:utf-8 -*-
# coding=<utf8>

import datetime
from itertools import chain

from django.http import HttpResponse, Http404, HttpResponseRedirect,\
    HttpResponseForbidden
from django.shortcuts import render_to_response
from save_state.models import Status
from todoes.models import Person
from django.contrib.auth.decorators import login_required
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.template import RequestContext


from djlib.cron_utils import decronize, crontab_to_russian, generate_next_reminder
from djlib.text_utils import htmlize
from djlib.acl_utils import acl, for_admins, admins_only
from djlib.user_tracking import set_last_activity_model, get_last_activities
from djlib.mail_utils import send_email_alternative
from djlib.auxiliary import get_info
from djlib.logging_utils import log, confirm_log, make_request_with_logging

from user_settings.settings import server_ip, admins, admins_mail
try:
    from user_settings.settings import assets_url_not_to_track as url_not_to_track
except ImportError:
    url_not_to_track=('',)
try:
    from user_settings.settings import assets_url_one_record as url_one_record
except ImportError:
    url_one_record=('',)


from djlib.error_utils import FioError, ErrorMessage, add_error, shows_errors

from djlib.multilanguage_utils import select_language,multilanguage,register_lang#,register_app

register_lang('ru','RUS')
register_lang('eng','ENG')
app='save_state'

# @login_required
# @multilanguage
# @shows_errors
# @admins_only
# def show_last_logs(request,number_to_select):
#     if not number_to_select:
#         number_to_select = 50
#     logs = Status.objects.all()[:number_to_select]
#     return (True,('statuses.html',{},{'logs':logs,'log_number':number_to_select},request,app))

def save_by_http(request, group, key, source, status, message, TTL,
                 api_key_got):
    from user_settings.functions import get_full_option
    # getting API key
    api_key = get_full_option('save_state','api_key').value
    # print api_key.value
    # print api_key_got
    if api_key != api_key_got:
        return HttpResponseForbidden('')
    next_report = datetime.datetime.now() + \
                  datetime.timedelta(minutes=int(TTL))
    status = Status(group=group, key=key,source=source,status=status,
                    message=message,
                    timestamp=datetime.datetime.now(),
                    next_report=next_report)
    status.save()
    return HttpResponse('')

@login_required
@multilanguage
@shows_errors
@admins_only
def show_states(request,div_id):
    from save_state.models import STATUSES
    stat_dict = {k:v for (k,v) in STATUSES}
    human_stat_dict = {v:k for (k,v) in STATUSES}
    class Group:
        def __init__(self,group):
            self.name = group[0]
            self.items = group[1]
    class Status_group:
        def __init__(self):
            self.__group = dict()
            self.warning = 0
        def append(self,item):
            if item.next_report<=datetime.datetime.now():
                item.status = human_stat_dict['ERROR']
                item.message = u'Отчёт просрочен. Должен был придти '\
                               + str(item.next_report)
            item.message = item.message.replace('|','\n')
            item.message = item.message + '\nLast report time: '\
                           + str(item.timestamp) + '\nNext report' \
                           ' time: ' + str(item.next_report)
            if item.status > human_stat_dict['INFO']:
                self.warning+=1
            if item.group in self.__group:
                item.status_name = stat_dict[item.status]
                self.__group[item.group].append(item)
            else:
                self.__group[item.group] = []
                item.status_name = stat_dict[item.status]
                self.__group[item.group].append(item)
        def result(self):
            res = []
            max_length = 0
            for k,v in sorted(self.__group.items()):
                res.append(Group([k,v]))
                if len(v)>max_length:
                    max_length=len(v)
            return res,max_length,self.warning
    pairs = Status.objects.all().values('group','key').distinct()
    #[{'group': u'tasks', 'key': u'backup'},
    #  {'group': u'tasks', 'key': u'test'}]
    statuses = Status_group()
    for pair in pairs:
        # для каждой пары группа/ключ получаем последнее значение
        statuses.append(Status.objects.filter(
            group=pair['group'],
            key=pair['key']).order_by('-timestamp')[0])
    # print statuses
    result,max_length,warning = statuses.result()
    # print result
    return (True,('statuses.html',{},
                  {'statuses':result, 'max_length':max_length,
                   'div_id': div_id,'warning':warning},
                  request,app))
