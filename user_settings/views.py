#-------------------------------------------------------------------------------
# Name:        tasks.user_settings.views
# Purpose:     Настройки для сайта
#
# Author:      Ishayahu
#
# Created:     28.08.2013
# Copyright:   (c) Ishayahu 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import datetime
from itertools import chain

from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render_to_response
##from assets.models import Asset, Payment, Cash, Cashless, Contractor, Garanty, Asset_type, Status, Budget, Repair, Place_Asset, Place, Cartridge, Cartridge_Model_General_Model, Cartridge_General_Model_Printer_Model, Cartridge_Printer, ROM, Cooler, Storage, Acoustics, Telephone, Battery, Optical_Drive, Printer, Power_suply, Motherboard, CPU, Case
from todoes.models import  Person #, Task, ProblemByWorker, ProblemByUser, Categories, RegularTask, Activity, Note, Resource, File,
# from assets.forms_rus import NewAssetForm_RUS, NewCashBillForm_RUS
# from assets.forms_eng import NewAssetForm_ENG, NewCashBillForm_ENG
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

# Делаем переводы
from djlib.multilanguage_utils import select_language,multilanguage,register_lang#,register_app

register_lang('ru','RUS')
register_lang('eng','ENG')
app='user_settings'

@login_required
@multilanguage
@admins_only
def show_settings(request):
    a=open(os.path.sep.join((os.getcwd(),'user_settings','test_file.py')),'w')