# -*- coding:utf-8 -*-
# coding=<utf8>

import datetime
from itertools import chain

from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render_to_response
from assets.models import Asset, Payment, Cash, Cashless, Contractor, Garanty, Asset_type, Status, Budget, Repair, Place_Asset, Place, Cartridge, Cartridge_Model_General_Model, Cartridge_General_Model_Printer_Model, Cartridge_Printer, ROM, Cooler, Storage, Acoustics, Telephone, Battery, Optical_Drive, Printer, Power_suply, Motherboard, CPU, Case
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
from user_settings.settings import assets_url_not_to_track as url_not_to_track
from user_settings.settings import assets_url_one_record as url_one_record

from djlib.error_utils import FioError

@login_required
def asset_add(request,asset_category):
    user = request.user.username
    try:
        fio = Person.objects.get(login=user)
    except Person.DoesNotExist:
        fio = FioError()
    method = request.method
    if request.method == 'POST':
        form = NewAsset(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            a=Asset(asset_type = data['asset_type'],
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
        form = NewAsset({})
    return render_to_response('new_asset.html', {'form':form, 'method':method},RequestContext(request))    