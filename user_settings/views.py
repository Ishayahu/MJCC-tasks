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

from user_settings.functions import  get_section_description, get_full_bd_option, get_full_option
from user_settings.functions import get_bd_option_variants
import codecs
from djlib.error_utils import FioError, ErrorMessage, add_error, shows_errors

# Делаем переводы
from djlib.multilanguage_utils import select_language,\
    multilanguage,register_lang#,register_app
from djlib.auxiliary import get_info

import ConfigParser
from ConfigParser import DEFAULTSECT
import codecs

register_lang('ru','RUS')
register_lang('eng','ENG')
app='user_settings'

class UnicodeConfigParser(ConfigParser.RawConfigParser):
    def __init__(self, defaults=None, dict_type=dict):
        ConfigParser.RawConfigParser.__init__(self, defaults, dict_type)
    def write(self, fp):
        """Fixed for Unicode output"""
        if self._defaults:
            fp.write("[%s]\n" % DEFAULTSECT)
            for (key, value) in self._defaults.items():
                fp.write("%s = %s\n" % (key, unicode(value).replace('\n', '\n\t')))
            fp.write("\n")
        for section in self._sections:
            fp.write("[%s]\n" % section)
            for (key, value) in self._sections[section].items():
                if key != "__name__":
                    fp.write("%s = %s\n" %
                             (key, unicode(value).replace('\n','\n\t')))
            fp.write("\n")
    # This function is needed to override default lower-case conversion
    # of the parameter's names. They will be saved 'as is'.
    def optionxform(self, strOut):
        return strOut


@login_required
@multilanguage
@admins_only
def show_settings(request):
    class Settings_group():
        def __init__(self,name,description):
            self.name = name
            self.settings = []
            self.description = description
    settings=[]
    config=ConfigParser.RawConfigParser()
    config.read(config_file)
    for section in config.sections():
        setting_goup = Settings_group(section,get_section_description(section))
        for item in config.items(section):
            # Не включаем описания и названия опций
            if item[0][-12:]=='_description' or item[0][-5:]=='_name' or item[0][-5:]=='_help':
                continue
            # Настройки, связанные со значениями в БД
            if item[0][:6]=='__bd__':
                if item[0][:12]=='__bd__name__':
                    option = item[0][12:]
                    # return name,opt_id,opt_val,desc
                    # Надо, чтобы при отображении в шаблоне редактировалось оно как список!
                    # name,opt_id,opt_val,desc = get_bd_option_with_description(section,option)
                    full_option = get_full_bd_option(section,option)
                    # setting_goup.settings.append(Setting(option, opt_id+";"+opt_val, name, desc, 1))
                    setting_goup.settings.append(full_option)
            # Все остальные настройки
            else: 
                # setting_goup.settings.append(Setting(*get_option_with_name_and_description(section,item[0]), from_bd=0))
                full_option = get_full_option(section,item[0])
                setting_goup.settings.append(full_option)
        settings.append(setting_goup)
        # получаем список модулей, доступных для подключения в меню
    modules = Settings_group('Модули','Доступные модули для системы')
    import os
    import os.path
    from functions import Option
    # [('assets_name', ''), ('section_description', '\xd0\x9f\xd0\xbe\xd0\xb4\xd0\xba\xd0\xbb\xd1\x8e\xd1\x87\xd1\x91\xd0\xbd\xd0\xbd\xd1\x8b\xd0\xb5 \xd0\xbc\xd0\xbe\xd0\xb4\xd1\x83\xd0\xbb\xd0\xb8'), ('assets_description', ''), ('assets', 'True')]
    # получаем списки модулей, которые находятся в настройках
    try:
        connected_modules = [x[0] for x in config.items('modules')]
    except ConfigParser.NoSectionError:
        connected_modules=[]
    # print connected_modules
    cur_dir = os.getcwd()
    for record in os.listdir('.'):
        if os.path.isdir(record):
            temp_dir = os.path.join(cur_dir,record)
            # os.chdir(temp_dir)
            if 'todoes_module' in os.listdir(temp_dir):
                lines = codecs.open(os.path.join(cur_dir,
                                          record,
                                          'todoes_module'),
                                    'r',
                                    encoding='utf-8').readlines()
                lines = [line.strip() for line in lines]
                if lines and lines[0]==u'MODULE_DESCRIPTION_v_1':
                    # проверяем, не включён ли он
                    if record in connected_modules:
                        modules.settings.append(Option(
                            section=u'Модули',
                            option=record,
                            val='True',
                            name=lines[1],
                            desc=lines[2],
                            help_message=lines[3],
                            from_bd=0,
                            opt_id=None,
                            option_type='CONNECT'
                        ))
                    else:
                        # если не подключён
                        modules.settings.append(Option(
                            section=u'Модули',
                            option=record,
                            val='False',
                            name=lines[1],
                            desc=lines[2],
                            help_message=lines[3],
                            from_bd=0,
                            opt_id=None,
                            option_type='CONNECT'
                        ))
    # для каждого модуля надо проверить, есть ли он в настройках
    # если нет - то можно его подключить и добавить в настройки,
    # если есть показываем статус из настроек. Данные для модуля
    # будем брать из файла todoes_module. Если в нём не правильные
    # данные - выдаём про него отдельное сообщение
    settings.append(modules)
    return (True,('show_settings.html',
                  {},
                  {'settings':settings,
                   # 'modules':modules,
                   },
                  request,
                  app))

@login_required
@multilanguage
def show_user_settings(request,for_user_login):
    class Settings_group():
        def __init__(self,name,description):
            self.name = name
            self.settings = []
            self.description = description
    lang,login,user,method = get_info(request)
    if user not in admins and for_user_login:
        return (False,HttpResponseRedirect('/'))
    settings=[]
    config=ConfigParser.RawConfigParser()
    config.read(config_file)
    section = '{0}_settings'.format(login)
    try:
        setting_goup = Settings_group(section,get_section_description(section))
        for item in config.items(section):
            # Не включаем описания и названия опций
            if item[0][-12:]=='_description' or item[0][-5:]=='_name' or item[0][-5:]=='_help':
                continue
            # Настройки, связанные со значениями в БД
            if item[0][:6]=='__bd__':
                if item[0][:12]=='__bd__name__':
                    option = item[0][12:]
                    # return name,opt_id,opt_val,desc
                    # Надо, чтобы при отображении в шаблоне редактировалось оно как список!
                    # name,opt_id,opt_val,desc = get_bd_option_with_description(section,option)
                    full_option = get_full_bd_option(section,option)
                    # setting_goup.settings.append(Setting(option, opt_id+";"+opt_val, name, desc, 1))
                    setting_goup.settings.append(full_option)
            # Все остальные настройки
            else:
                # setting_goup.settings.append(Setting(*get_option_with_name_and_description(section,item[0]), from_bd=0))
                full_option = get_full_option(section,item[0])
                setting_goup.settings.append(full_option)
        settings.append(setting_goup)
    except ConfigParser.NoSectionError:
        settings=None
    return (True,('show_settings.html', {},{'settings':settings,},request,app))
@login_required
@multilanguage
@admins_only
def save_edited_setting(request,section,option):
    # raise NotImplementedError("Надо корректно обрабатывать настройки, связанные с БД!! например, место по умолчанию, статус по умолчанию+сделать, чтобы при редактировании всё было правильно")

    lang,user,fio,method = get_info(request)
    if request.method == 'POST':
        value = request.POST.get('new_value')
        config=UnicodeConfigParser()
        config.readfp(codecs.open(config_file, encoding='utf-8', mode='r'))
        config.set(section,option,value)
        config.write(codecs.open(config_file, encoding='utf-8', mode='w'))
        return (True,('OK.html', {},{'html':value},request,app))
    return (True,('Error.html', {},{'html':'метод не POST! Нифига не сделано!'},request,app))
@login_required
@multilanguage
@admins_only
def save_from_bd(request,section,option):
    # raise NotImplementedError("Надо корректно обрабатывать настройки, связанные с БД!! например, место по умолчанию, статус по умолчанию+сделать, чтобы при редактировании всё было правильно")
    lang,user,fio,method = get_info(request)
    if request.method == 'POST':
        value = request.POST.get('new_value')
        config=UnicodeConfigParser()
        config.readfp(codecs.open(config_file, encoding='utf-8', mode='r'))
        config.set(section,"__bd__option__"+option,value)
        config.write(codecs.open(config_file, encoding='utf-8', mode='w'))
        # name,opt_id,opt_val,desc = get_bd_option_with_description(section,option)
        opt_id = get_full_bd_option(section,option).id
        opt_val = get_full_bd_option(section,option).value
        returning_value = str(opt_id)+";"+opt_val
        return (True,('OK.html', {},{'html':returning_value},request,app))
    return (True,('Error.html', {},{'html':'метод не POST! Нифига не сделано!'},request,app))
@login_required
@multilanguage
@admins_only
def edit_from_bd(request,section,option):
    lang,user,fio,method = get_info(request)
    config=ConfigParser.RawConfigParser()
    config.read(config_file)
    # name,opt_id,opt_val,desc = get_bd_option_with_description(section,option)
    opt_id = get_full_bd_option(section,option).id
    opts = get_bd_option_variants(section,option)
    for opt in opts:
        if str(opt.id) == str(opt_id):
            opt.selected = True
    # raise NotImplementedError("Надо корректно обрабатывать настройки, связанные с БД!! например, место по умолчанию, статус по умолчанию+сделать, чтобы при редактировании всё было правильно")
    return (True,('edit_from_bd.html', {},{'opts':opts,'option':option},request,app))
@login_required
@multilanguage
@admins_only
def run_module(request,module_name):
    lang,user,fio,method = get_info(request)
    config=UnicodeConfigParser()
    config.readfp(codecs.open(config_file, encoding='utf-8', mode='r'))
    try:
        config.set('modules',module_name,'True')
        config.set('modules',module_name+"_description",'')
        config.set('modules',module_name+"_name",'')
    except ConfigParser.NoSectionError:
        config.add_section('modules')
        config.set('modules','section_description',u'Подключённые модули')
        config.set('modules',module_name,'True')
        config.set('modules',module_name+"_description",'')
        config.set('modules',module_name+"_name",'')
    config.write(codecs.open(config_file, encoding='utf-8', mode='w'))
    return (False,HttpResponseRedirect('/settings/'))
@login_required
@multilanguage
@admins_only
def stop_module(request,module_name):
    lang,user,fio,method = get_info(request)
    config=UnicodeConfigParser()
    config.readfp(codecs.open(config_file, encoding='utf-8', mode='r'))
    config.remove_option('modules',module_name)
    config.remove_option('modules',module_name+"_description")
    config.remove_option('modules',module_name+"_name")
    config.write(codecs.open(config_file, encoding='utf-8', mode='w'))
    return (False,HttpResponseRedirect('/settings/'))
