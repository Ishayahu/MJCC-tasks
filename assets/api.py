# -*- coding:utf-8 -*-
# coding=<utf8>

import datetime
from itertools import chain

from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render_to_response
from assets.models import Asset, Payment, Cash, Cashless, Contractor, Garanty, Asset_type, Status, Budget, Repair, Place_Asset, Place, Cartridge, Cartridge_Model_General_Model, Cartridge_General_Model_Printer_Model, Cartridge_Printer, ROM, Cooler, Storage, Acoustics, Telephone, Battery, Optical_Drive, Printer, Power_suply, Motherboard, CPU, Case
from todoes.models import  Person #, Task, ProblemByWorker, ProblemByUser, Categories, RegularTask, Activity, Note, Resource, File,
from assets.forms_rus import NewAssetForm_RUS, NewContractorForm_RUS
from assets.forms_eng import NewAssetForm_ENG, NewContractorForm_ENG
from django.contrib.auth.decorators import login_required
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.template import RequestContext, loader, Context

from djlib.cron_utils import decronize, crontab_to_russian, generate_next_reminder
from djlib.text_utils import htmlize
from djlib.acl_utils import acl
from djlib.user_tracking import set_last_activity_model, get_last_activities
from djlib.mail_utils import send_email_alternative
from djlib.error_utils import FioError, ErrorMessage

from user_settings.settings import server_ip, admins, admins_mail
try:
    from user_settings.settings import assets_url_not_to_track as url_not_to_track
except ImportError:
    url_not_to_track=('',)
try:
    from user_settings.settings import assets_url_one_record as url_one_record
except ImportError:
    url_one_record=('',)




# Делаем переводы
from djlib.multilanguage_utils import select_language
languages={'ru':'RUS/',
            'eng':'ENG/'}
forms_RUS = {'NewAssetForm':NewAssetForm_RUS, 'NewContractorForm':NewContractorForm_RUS}
forms_ENG = {'NewAssetForm':NewAssetForm_ENG, 'NewContractorForm':NewContractorForm_ENG}
l_forms = {'ru':forms_RUS,
           'eng':forms_ENG,
    }
    
    #lang=select_language(request)
    #..........
    #if request.method == 'POST':
        #form = NewClientForm(request.POST)
    #.....................
    #else:
        #form = l_forms[lang]['NewClientForm']()
    #return render_to_response(languages[lang]+'new_ticket.html', {'form':form, 'met......
@login_required
def get_asset_add_form(request,asset_category):
    lang=select_language(request)
    user = request.user.username
    try:
        fio = Person.objects.get(login=user)
    except Person.DoesNotExist:
        fio = FioError()
    method = request.method
    try:
        asset_type = Asset_type.objects.get(id=asset_category)
    except Asset_type.DoesNotExist:
        return ErrorMessage('Неверно указан код категории актива: '+str(asset_category))
    form = l_forms[lang]['NewAssetForm'](number=3)
    return render_to_response(languages[lang]+'get_asset_add_form.html', {'form':form, 'method':method},RequestContext(request))    
@login_required
def get_contractors_list(request,name_to_select='',internal=False):
    lang=select_language(request)
    user = request.user.username
    try:
        fio = Person.objects.get(login=user)
    except Person.DoesNotExist:
        fio = FioError()
    try:
        contractor = Contractor.objects.get(name=name_to_select)
    except Contractor.DoesNotExist:
        contractor = ''
    method = request.method
    contractors = Contractor.objects.all()
    if internal:
        t = loader.get_template(languages[lang]+'get_contractors_list.html')
        c = Context({'contractors':contractors})
        return t.render(c)
    return render_to_response(languages[lang]+'get_contractors_list.html', {'contractors':contractors,'contractor':contractor,'name_to_select':name_to_select},RequestContext(request))
@login_required
def get_new_contractor_add_form(request, contractor_name):
    lang=select_language(request)
    user = request.user.username
    try:
        fio = Person.objects.get(login=user)
    except Person.DoesNotExist:
        fio = FioError()
    method = request.method
    form = l_forms[lang]['NewContractorForm']({'name':contractor_name})
    return render_to_response(languages[lang]+'get_new_contractor_add_form.html', {'form':form, 'method':method},RequestContext(request)) 
@login_required
def save_new_contractor(request):
    lang=select_language(request)
    user = request.user.username
    try:
        fio = Person.objects.get(login=user)
    except Person.DoesNotExist:
        fio = FioError()
    method = request.method
    if request.method == 'POST':
        form = l_forms[lang]['NewContractorForm'](request.POST)
        if form.is_valid():
            data = form.cleaned_data
            c=Contractor(name = data['name'],
                        tel = data['tel'],
                        email = data['email'],
                        tel_of_support = data['tel_of_support'],
                        contact_name = data['contact_name'],)
            c.save()
            return render_to_response(languages[lang]+'OK.html', {'c':c},RequestContext(request))
    return "Произошла какая-то ошибка"