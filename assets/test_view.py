# -*- coding:utf-8 -*-
# coding=<utf8>

import datetime
from itertools import chain

from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.utils.translation import ugettext as _
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

import assets.api

# Делаем переводы
from djlib.multilanguage_utils import select_language,multilanguage,register_lang#,register_app

register_lang('ru','RUS')
register_lang('eng','ENG')
app='assets'

@login_required
@multilanguage
def bill_add(request):
    lang,user,fio,method = get_info(request)
    if request.method == 'POST':
        # Порядок действия таков:
        # 1) Создаём Cash
        # 2) Создаём Payment с этим Cash
        # 3) Создаём Garanty - если её ещё нет. Если есть - добавляем к имеющейся
        # 4) Итерируем по элементам в форме от 1 до макс добавляя активы в список активов
        # 5) Если всё прошло хорошо - активы из списка сохраняем

        bill_date = request.POST.get('date','')
        if bill_date:
            a=[int(a) for a in bill_date.split('.')]
            a.reverse()
            bill_date=datetime.datetime(*a)
        else:
            bill_date = datetime.datetime.now()
        # print bill_date
        # raise ImportError
        cash = Cash(date = bill_date,
               contractor = Contractor.objects.get(id=request.POST.get('contractor_id')),
               bill_number = request.POST.get('bill_number'),
               )
        cash.save()
        payment = Payment(cash = cash,
                )
        payment.save()
        try:
            garanty = Garanty.objects.get(number = request.POST.get('garanty'))
        except Garanty.DoesNotExist:
            garanty = Garanty(number = request.POST.get('garanty'))
            garanty.save()
        for item_number in range(1,int(request.POST.get('max_asset_form_number'))+1):
            sitem_number = str(item_number)
            if sitem_number+'_model' in request.POST:
                for count in range(0,int(request.POST.get('count_of_asset'+sitem_number))):
                    a=Asset(asset_type = Asset_type.objects.get(id=request.POST.get(sitem_number+'_asset_type')),
                        payment = payment,
                        garanty = garanty,
                        model = request.POST.get(sitem_number+'_model'),
                        status = Status.objects.get(id=request.POST.get(sitem_number+'_status')),
                        guarantee_period = request.POST.get(sitem_number+'_guarantee_period'),
                        note = request.POST.get(sitem_number+'_note'),
                        price = request.POST.get(sitem_number+'_price'),
                        )
                    a.save()
                    cur_place=Place_Asset(installation_date = bill_date,
                        asset = a,
                        place = Place.objects.get(id=request.POST.get(sitem_number+'_current_place')),
                        )
                    cur_place.save()
        return (False,HttpResponseRedirect('/tasks/'))
        # else:
            # print "FOrm is not valid??"
    contractors_list = assets.api.get_contractors_list(request,internal=True)
    asset_types_list = assets.api.get_asset_type_list(request,internal=True)
    # Translators: This message appears on the home page only
    message=_('Message')
    print message
    print request.LANGUAGE_CODE
    return (True,('new_bill.html', {'NewCashBillForm':{}},{'contractors_list':contractors_list,'asset_types_list':asset_types_list, 'method':method,'message':message},request,app))
    
@login_required
@multilanguage
@shows_errors
@for_admins
def all_bills(request):
    lang,user,fio,method = get_info(request)
    # cashs = make_request_with_logging(user,"Запрашиваем все чеки",Cash.objects.filter,{'payment__in':Payment.objects.filter(deleted=False)})
    cashs =  Cash.objects.filter(payment__in=Payment.objects.filter(deleted=False))
    cashlesss = Cashless.objects.filter(payment__in=Payment.objects.filter(deleted=False))
    return (True,('all_bills.html',{},{'title':'Список всех счетов и чеков','cashs':cashs, 'cashlesss':cashlesss},request,app))
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
@login_required
@multilanguage
@admins_only
def all_deleted_bills(request):
    lang,user,fio,method = get_info(request)
    cashs =  Cash.objects.filter(payment__in=Payment.objects.filter(deleted=True))
    cashlesss = Cashless.objects.filter(payment__in=Payment.objects.filter(deleted=True))
    return (True,('all_deleted_bills.html',{},{'title':'Список всех удалённых счетов и чеков','cashs':cashs, 'cashlesss':cashlesss},request,app))
@login_required
@multilanguage
@shows_errors
def assets_by_type(request,type_id):
    if not type_id:
        type_id=0
    else:
        type_id=int(type_id)
    lang,user,fio,method = get_info(request)
    try:
        type_name = Asset_type.objects.get(id=type_id)
        asset_types = Asset_type.objects.all()
        type_name_asset_type=type_name.asset_type
    except Asset_type.DoesNotExist:
        type_name_asset_type = u"Такого типа акивов нет"
        asset_types=[]
    return (True,('assets_by_type.html',{},{'type_name':type_name_asset_type,'asset_types':asset_types,'type_id':type_id},request,app))
def simple(request):
    output = _("Welcome to my site.")
    return HttpResponse(output)
@login_required
@multilanguage
@shows_errors
def test_cm(request):
    lang,user,fio,method = get_info(request)
    # Получаем настройки из файла:
    cashless={'bill_number':88,'date_of_invoice':'00-11-12'}
    fn=r"user_settings/config.txt"
    import ConfigParser
    config=ConfigParser.RawConfigParser()
    config.read(fn)
    text = config.get('cashless','text')
    text=text.decode('utf8').format({'number':88,'where':"AAAAAAAAAAAAAAA",'date':'10-11-12','price':9854,'what':"DDDDDD",'who':fio.fio,'phones':fio.tel,'date2':str(datetime.datetime.now()).split('.')[0]}).replace('\n','<p>')
    return (True,('cashless_redirect.html', {},{'text':text,'cashless':cashless},request,app))
@login_required
@multilanguage
@shows_errors
def cashless_maintenance(request):
    return (True,('cashless_maintenance.html', {},{},request,app))
@login_required
@multilanguage
@shows_errors
def password(request):
    lang,user,fio,method = get_info(request)
    if request.method == 'POST':
        from django.contrib.auth.models import User
        u = User.objects.get(username__exact='john')
        u.set_password('new password')
        u.save()
        return (True,('password.html', {},{},request,app))
    return (True,('password.html', {},{},request,app))