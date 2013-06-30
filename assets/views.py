# -*- coding:utf-8 -*-
# coding=<utf8>

import datetime
from itertools import chain

from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render_to_response
from assets.models import Asset, Payment, Cash, Cashless, Contractor, Garanty, Asset_type, Status, Budget, Repair, Place_Asset, Place, Cartridge, Cartridge_Model_General_Model, Cartridge_General_Model_Printer_Model, Cartridge_Printer, ROM, Cooler, Storage, Acoustics, Telephone, Battery, Optical_Drive, Printer, Power_suply, Motherboard, CPU, Case
from todoes.models import  Person #, Task, ProblemByWorker, ProblemByUser, Categories, RegularTask, Activity, Note, Resource, File,
# from assets.forms_rus import NewAssetForm_RUS, NewCashBillForm_RUS
# from assets.forms_eng import NewAssetForm_ENG, NewCashBillForm_ENG
from django.contrib.auth.decorators import login_required
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.template import RequestContext


from djlib.cron_utils import decronize, crontab_to_russian, generate_next_reminder
from djlib.text_utils import htmlize
from djlib.acl_utils import acl
from djlib.user_tracking import set_last_activity_model, get_last_activities
from djlib.mail_utils import send_email_alternative
from djlib.auxiliary import get_info

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

import assets.api

# Делаем переводы
from djlib.multilanguage_utils import select_language,multilanguage,register_lang#,register_app

register_lang('ru','RUS')
register_lang('eng','ENG')
app='assets'
# languages={'ru':'RUS/',
            # 'eng':'ENG/'}
# forms_RUS = {'NewAssetForm':NewAssetForm_RUS,'NewCashBillForm':NewCashBillForm_RUS}
# forms_ENG = {'NewAssetForm':NewAssetForm_ENG,'NewCashBillForm':NewCashBillForm_ENG}
# l_forms = {'ru':forms_RUS,
           # 'eng':forms_ENG,
    # }
    
    #lang=select_language(request)
    #..........
    #if request.method == 'POST':
        #form = NewClientForm(request.POST)
    #.....................
    #else:
        #form = l_forms[lang]['NewClientForm']()
    #return render_to_response(languages[lang]+'new_ticket.html', {'form':form, 'met......

@login_required
@multilanguage
def bill_add(request):
    # lang=select_language(request)
    # user = request.user.username
    # try:
        # fio = Person.objects.get(login=user)
    # except Person.DoesNotExist:
        # fio = FioError()
    # method = request.method
    lang,user,fio,method = get_info(request)
    if request.method == 'POST':
        # Порядок действия таков:
        # 1) Создаём Cash
        # 2) Создаём Payment с этим Cash
        # 3) Создаём Garanty
        # 4) Итерируем по элементам в форме от 1 до макс добавляя активы в список активов
        # 5) Если всё прошло хорошо - активы из списка сохраняем
        bill_date = request.POST.get('date')
        # raise TypeError
        if not bill_date:
            bill_date = datetime.datetime.now()
        cash = Cash(date = bill_date,
               contractor = Contractor.objects.get(id=request.POST.get('contractor_id'))
               )
        cash.save()
        payment = Payment(cash = cash,
                )
        payment.save()
        garanty = Garanty(number = request.POST.get('garanty'))
        garanty.save()
        # assets_list=[]
        # print list(range(1,int(request.POST.get('max_asset_form_number'))+1))
        for item_number in range(1,int(request.POST.get('max_asset_form_number'))+1):
            sitem_number = str(item_number)
            # print sitem_number+'_model',(sitem_number+'_model' in request.POST)
            if sitem_number+'_model' in request.POST:
                # guarantee_period = request.POST.get(sitem_number+'_guarantee_period')
                # if not request.POST.get(sitem_number+'_guarantee_period'):
                    # guarantee_period=0
                for count in range(0,int(request.POST.get('count_of_asset'+sitem_number))):
                    a=Asset(asset_type = Asset_type.objects.get(id=request.POST.get(sitem_number+'_asset_type')),
                        payment = payment,
                        garanty = garanty,
                        # current_place = request.POST.get(sitem_number+'_current_place'],
                        model = request.POST.get(sitem_number+'_model'),
                        status = Status.objects.get(id=request.POST.get(sitem_number+'_status')),
                        # claim = request.POST.get('claim'], - Не тут
                        guarantee_period = request.POST.get(sitem_number+'_guarantee_period'),
                        note = request.POST.get(sitem_number+'_note'),
                        price = request.POST.get(sitem_number+'_price'),
                        )
                    a.save()
                    cur_place=Place_Asset(installation_date = bill_date,
                        # drawdown_date = models.DateTimeField()
                        asset = a,
                        place = Place.objects.get(id=request.POST.get(sitem_number+'_current_place')),
                        # reason_of_drawdown = models.TextField()
                        )
                    cur_place.save()
                    # assets_list.append(a)
                    # assets_list.append(cur_place)
        # for a in assets_list:
            # a.save()
        # raise TypeError
        return (False,HttpResponseRedirect('/tasks/'))
    # form = l_forms[lang]['NewCashBillForm']({})
    contractors_list = assets.api.get_contractors_list(request,internal=True)
    asset_types_list = assets.api.get_asset_type_list(request,internal=True)
    # return render_to_response(languages[lang]+'new_bill.html', {'form':form,'contractors_list':contractors_list,'asset_types_list':asset_types_list, 'method':method},RequestContext(request))
    return (True,('new_bill.html', {'NewCashBillForm':{}},{'contractors_list':contractors_list,'asset_types_list':asset_types_list, 'method':method},request,app))
    
@login_required
@multilanguage
def all_bills(request):
    lang,user,fio,method = get_info(request)
    
    
    cashs = Cash.objects.all()
    cashlesss = Cashless.objects.all()
    return (True,('all_bills.html',{},{'cashs':cashs, 'cashlesss':cashlesss},request,app))
    # return (decorate_or_not,('all_bills.html',{'form_name':(form_param1,form_param2),},{'cashs':cashs, 'cashlesss':cashlesss},request,app))
    # return ('all_bills.html',{'cashs':cashs, 'cashlesss':cashlesss},request)
@login_required
@multilanguage
def show_bill(request,type,id):
    bill_types={'cash':Cash,'cashless':Cashless}
    bill=bill_types[type].objects.get(id=id)
    payment=bill.payment_set.get()
    assets=payment.asset_set.all()
    for asset in assets:
        asset.place=asset.place_asset_set.latest('installation_date').place.place
    return (True,('show_bill.html',{},{'bill':bill,'assets':assets},request,app))