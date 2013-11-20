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

from user_settings.settings import server_ip, admins, admins_mail,config_file
try:
    from user_settings.settings import assets_url_not_to_track as url_not_to_track
except ImportError:
    url_not_to_track=('',)
try:
    from user_settings.settings import assets_url_one_record as url_one_record
except ImportError:
    url_one_record=('',)

from user_settings.functions import get_option_description,get_section_description
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
    # a=open(os.path.sep.join((os.getcwd(),'user_settings','test_file.py')),'w')
    class Setting():
        def __init__(self,name,value,description):
            self.name = name
            self.value = value
            self.description = description
    class Settings_group():
        def __init__(self,name,description):
            self.name = name
            self.settings = []
            self.description = description
    settings=[]
    import ConfigParser
    config=ConfigParser.RawConfigParser()
    config.read(config_file)
    for section in config.sections():
        setting_goup = Settings_group(section,get_section_description(section))
        for item in config.items(section):
            # Не включаем описания опций
            if item[0][-12:]!='_description':
                setting_goup.settings.append(Setting(item[0],item[1].replace('\n','<p>'),get_option_description(section,item[0])))
        settings.append(setting_goup)
    return (True,('show_settings.html', {},{'settings':settings,},request,app))
@login_required
@multilanguage
@admins_only
def save_edited_setting(request,name):
    lang,user,fio,method = get_info(request)
    try:
        a = Asset.objects.get(id=id)
    except Asset.DoesNotExist:
        add_error(u"Актив с номером %s не найден!" % id,request)
        return (False,(HttpResponseRedirect("/")))
    asset_type = a.asset_type.catalogue_name
    app_module_name = 'assets.models'
    app_module = __import__(app_module_name)
    models_module = getattr(app_module,'models')
    asset_type_catalogue = getattr(models_module, a.asset_type.catalogue_name)
    asset_type_models = asset_type_catalogue.objects.all()
    statuses = Status.objects.all()
    garantys = Garanty.objects.all()
    places = Place.objects.all()
    return (True,('edit_asset.html', {},{'models':asset_type_models,'statuses':statuses,'garantys':garantys,'places':places,'asset_id':id,'item':a},request,app))
    