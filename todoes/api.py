# -*- coding:utf-8 -*-
# coding=<utf8>

__version__ = '0.2.3d'
import datetime
from itertools import chain
import json

from django.http import HttpResponse, Http404, HttpResponseRedirect
from todoes.models import Person, Task, ProblemByWorker,\
  ProblemByUser, Categories, RegularTask, Activity, Note, Resource,\
  File
from django.contrib.auth.decorators import login_required
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.template import RequestContext, loader, Context

from djlib.cron_utils import decronize, crontab_to_russian,\
    generate_next_reminder
from djlib.text_utils import htmlize
from djlib.acl_utils import acl, for_admins, admins_only
from djlib.user_tracking import set_last_activity_model,\
    get_last_activities
from djlib.mail_utils import send_email_alternative
from djlib.error_utils import FioError, ErrorMessage, add_error,\
    shows_errors
from djlib.auxiliary import get_info
from djlib.logging_utils import log, confirm_log, \
    make_request_with_logging

from user_settings.settings import server_ip, admins, admins_mail
from user_settings.functions import get_full_option,\
    get_full_bd_option

try:
    from user_settings.settings import assets_url_not_to_track \
        as url_not_to_track
except ImportError:
    url_not_to_track=('',)
try:
    from user_settings.settings import assets_url_one_record \
        as url_one_record
except ImportError:
    url_one_record=('',)

# Делаем переводы
from djlib.multilanguage_utils import select_language,\
    multilanguage, register_lang, get_localized_name,  \
    get_localized_form

register_lang('ru','RUS')
register_lang('eng','ENG')
app='todoes'

# @login_required
@multilanguage
# @admins_only
def crontab_to_human(request,cronized_string):
    response_data = dict()
    response_data['result'] = 'success'
    response_data['message'] = crontab_to_russian(cronized_string)
    return (False,HttpResponse(json.dumps(response_data),
                               content_type="application/json"))
