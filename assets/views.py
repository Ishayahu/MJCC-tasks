# -*- coding:utf-8 -*-
# coding=<utf8>

import datetime
from itertools import chain

from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render_to_response
from assets.models import Asset, Payment, Cash, Cashless, Contractor, Garanty, Asset_type, Status, Budget, Repair, Place_Asset, Place, Cartridge, Cartridge_Model_General_Model, Cartridge_General_Model_Printer_Model, Cartridge_Printer, ROM, Cooler, Storage, Acoustics, Telephone, Battery, Optical_Drive, Printer, Power_suply, Motherboard, CPU, Case
from todoes.models import  Person #, Task, ProblemByWorker, ProblemByUser, Categories, RegularTask, Activity, Note, Resource, File,
from assets.forms import NewAssetForm
from django.contrib.auth.decorators import login_required
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.template import RequestContext


from djlib.cron_utils import decronize, crontab_to_russian, generate_next_reminder
from djlib.text_utils import htmlize
from djlib.acl_utils import acl
from djlib.user_tracking import set_last_activity_model, get_last_activities
from djlib.mail_utils import send_email_alternative

from user_settings.settings import server_ip, admins, admins_mail
try:
    from user_settings.settings import assets_url_not_to_track as url_not_to_track
except ImportError:
    url_not_to_track=('',)
try:
    from user_settings.settings import assets_url_one_record as url_one_record
except ImportError:
    url_one_record=('',)


from djlib.error_utils import FioError

# Делаем переводы
from djlib.multilanguage_utils import select_language
languages={'ru':'RUS/',
            'eng':'ENG/'}
forms_RUS = {'NewClientForm':NewClientForm, 'EditClientForm':EditClientForm, 'ClientSearchForm':ClientSearchForm, 'NoteToClientAddForm':NoteToClientAddForm, 'UserCreationFormMY':UserCreationFormMY}
forms_ENG = {'NewClientForm':NewClientForm_ENG, 'EditClientForm':EditClientForm_ENG, 'ClientSearchForm':ClientSearchForm_ENG, 'NoteToClientAddForm':NoteToClientAddForm_ENG, 'UserCreationFormMY':UserCreationFormMY_ENG}
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
def asset_add(request,asset_category):
    user = request.user.username
    try:
        fio = Person.objects.get(login=user)
    except Person.DoesNotExist:
        fio = FioError()
    method = request.method
    if request.method == 'POST':
        form = NewAssetForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            try:
                asset_type = Asset_type.objects.get(id=asset_category)
            except Asset_type.DoesNotExist:
                request.session['my_error'] = u'Неправильно указан тип категории в адресной строке!'+str(asset_category)
                return HttpResponseRedirect('/tasks/')
            a=Asset(asset_type = Asset_type.objects.get(id=asset_category),
                    payment = data['payment'],
                    garanty = data['garanty'],
                    current_place = data['current_place'],
                    model = data['model'],
                    status = data['status'],
                    claim = data['claim'],
                    guarantee_period = data['guarantee_period'],
                    note = data['note'])
                
            """    model = forms.CharField(max_length=140, label='Модель')
    asset_type = forms.ModelChoiceField(queryset  = Asset_type.objects.all(), label='Тип актива')
    payment = forms.ModelChoiceField(queryset  = Payment.objects.all(), label='Оплата')    
    garanty = forms.ModelChoiceField(queryset  = Garanty.objects.all(), label='Номер гарантии')
    current_place = forms.ModelChoiceField(queryset  = Place_Asset.objects.all(), label='Место расположения')
    status = forms.ModelChoiceField(queryset  = Status.objects.all(), label='Статус')
    claim = forms.ModelChoiceField(queryset  = Claim.objects.all(), label='Заявка',required=False)
    guarantee_period = forms.DecimalField(min_value=0, max_value=9999, label='Срок гарантии, месяцев')    
    note = forms.CharField(widget=forms.Textarea, label='Примечания')    
    
    asset_type = models.ForeignKey('Asset_type')
    payment = models.ForeignKey('Payment')
    date_of_write_off = models.DateTimeField()
    garanty = models.ForeignKey('Garanty')
    current_place = models.ForeignKey('Place_Asset')
    model = models.CharField(max_length=140)
    status = models.ForeignKey('Status')
    claim = models.ForeignKey('Claim')
    guarantee_period = models.IntegerField()
    note = models.TextField()"""
            a.save()
            return HttpResponseRedirect('/tasks/')
    else:
        form = NewAssetForm({})
    return render_to_response('new_asset.html', {'form':form, 'method':method},RequestContext(request))    