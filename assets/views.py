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


from djlib.error_utils import FioError, ErrorMessage, add_error, shows_errors

import assets.api

# Делаем переводы
from djlib.multilanguage_utils import select_language,multilanguage,register_lang#,register_app

register_lang('ru','RUS')
register_lang('eng','ENG')
app='assets'

@login_required
@multilanguage
def bill_cash_add(request):
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
        return (False,HttpResponseRedirect('/all_bills/'))
    # Создаём новый счёт, значит теперь надо номер новой гарантии
    garanty_number = int(Garanty.objects.all().order_by('-number')[0].number)+1
    contractors_list = assets.api.get_contractors_list(request,internal=True)
    asset_types_list = assets.api.get_asset_type_list(request,internal=True)
    return (True,('new_bill.html', {'NewCashBillForm':{'garanty':garanty_number}},{'contractors_list':contractors_list,'asset_types_list':asset_types_list, 'method':method},request,app))
@login_required
@multilanguage
def bill_cashless_add(request):
    def what_to_people_friendly(a):
        b=list(set(a.split(';')))
        c = ''
        for word in b:
            count=a.split(';').count(b[0])
            c = c + b[0] + ' -' + str(count) + 'шт'
        return c
    lang,user,fio,method = get_info(request)
    # Получаем настройки из файла:
    import ConfigParser
    config=ConfigParser.RawConfigParser()
    config.read(config_file)
    # stages = ";".join([a[1] for a in config.items("cashless_stages")])
    from user_settings.functions import get_stages
    stages = get_stages(";")

    if request.method == 'POST':
        # Порядок действия таков:
        # 1) Создаём Cashless c этапами из файла настройки
        # 2) Создаём Payment с этим Cash
        # 3) Создаём Garanty - если её ещё нет. Если есть - добавляем к имеющейся
        # 4) Итерируем по элементам в форме от 1 до макс добавляя активы в список активов
        # 5) Если всё прошло хорошо - активы из списка сохраняем
        bill_date = request.POST.get('date','')
        if bill_date:
            a=[int(a) for a in bill_date.split(bill_date[2])]
            a.reverse()
            bill_date=datetime.datetime(*a)
        else:
            bill_date = datetime.datetime.now()
        cashless = Cashless(date_of_invoice = bill_date,
                stages=stages,
                # нужно для более простой обработки в дальнейшем
                dates = ';'.join(map(lambda x: '',range(len(stages.split(';'))))),
                contractor = Contractor.objects.get(id=request.POST.get('contractor_id')),
                bill_number = request.POST.get('bill_number'),
                )
        cashless.save()
        payment = Payment(cashless = cashless,
                )
        payment.save()
        try:
            garanty = Garanty.objects.get(number = request.POST.get('garanty'))
        except Garanty.DoesNotExist:
            garanty = Garanty(number = request.POST.get('garanty'))
            garanty.save()
        # Для записки сопровождения счёта
        places = ''
        what = ''
        price = 0
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
                    # a_TMP = cur_place.place.place
                    if cur_place.place.place + u';' not in places:
                        places = places+ cur_place.place.place + u';'
                    # if a.model + u';' not in what:    
                        # what = what + a.model + u';'
                    what = what + a.model + u';'
                    price += float(a.price)
        places = places[:-1]
        # Приводим к человеческому виду "кот - 5шт"
        what = what_to_people_friendly(what[:-1])
        # Теперь надо выдать штуку для распечатки сопровождения счёта
        text = config.get('cashless','text')
        text=text.decode('utf8').format({'number':cashless.bill_number,'where':places,'date':str(cashless.date_of_invoice),'price':price,'what':what,'who':fio.fio,'phones':fio.tel,'date2':str(datetime.datetime.now()).split('.')[0]}).replace('\n','<p>')
        # window.open("http://mylink.net", "windowName");
        # window.localStorage.setItem('text',text)
        # document.body.innerHTML=window.localStorage.getItem('text')        
        # return (False,HttpResponseRedirect('/all_bills/'))
        # Открывается окно с сопровождающей запиской, из него уже открывается окно списка счетов
        show_cashless_maintain = config.get('cashless','show_text')
        if show_cashless_maintain=='True':
            return (True,('cashless_redirect.html', {},{'text':text,'cashless':cashless},request,app))
        return (False,HttpResponseRedirect('/all_bills/'))
    # Создаём новый счёт, значит теперь надо номер новой гарантии
    garanty_number = int(Garanty.objects.all().order_by('-number')[0].number)+1
    contractors_list = assets.api.get_contractors_list(request,internal=True)
    asset_types_list = assets.api.get_asset_type_list(request,internal=True)
    return (True,('new_bill.html', {'NewCashBillForm':{'garanty':garanty_number}},{'stages':stages,'contractors_list':contractors_list,'asset_types_list':asset_types_list, 'method':method},request,app))
@login_required
@multilanguage
@shows_errors
def cashless_maintenance(request):
    return (True,('cashless_maintenance.html', {},{},request,app))
@login_required
@multilanguage
@shows_errors
@for_admins
def all_bills(request):
    # вспомогательный класс для вывода счётов по этапам
    class Bill_Set(object):
        def __init__(self):
            self.name=""
            self.set=[]
            self.id_name = ""
        def __unicode__(self):
            return  self.name+str( self.set)
        def __str__(self):
            return self.name+str(self.set)
        def __repr__(self):
            return self.name+" "+str(self.set)
        def __getattribute__(self,name):
            if name=='id_name':
                name = object.__getattribute__(self,'name')
                if name == 'Получить товар':
                    return 'Товар_получен'
                if name == 'Сдать документы':
                    return 'Документы_сданы'
                return object.__getattribute__(self,'name').replace(" ","_")
            return object.__getattribute__(self,name)
    class Bill_with_title():
        def __init__(self,c,title):
            self.bill=c
            self.title=title
        def __repr__(self):
            return self.title+"; "+str(self.bill.id)
    lang,user,fio,method = get_info(request)
    # выбираем только ещё не закрытые чеки
    cashs_tmp =  Cash.objects.filter(payment__in=Payment.objects.filter(deleted=False)).filter(closed_for=False)
    cashs=[]
    for c in cashs_tmp:
        # Для каждого чека делаем подсказку - что в нём
        title=""
        payment=c.payment_set.get()
        assets=payment.asset_set.all()
        for asset in assets:
            title+=asset.model
            title+="; "
        title=title[:-2]
        cashs.append(Bill_with_title(c,title))
    # выбираем только счета, по которым ещё не сдали документы
    cashlesss = Cashless.objects.filter(payment__in=Payment.objects.filter(deleted=False))
    # сортируем счета по безналу по этапам
    # импортируем функцию для получения количества этапов на счёт
    from user_settings.functions import get_stages
    stages = get_stages(";").split(";")
    stages_number = len(stages)
    cashlesss_sorted=[Bill_Set() for x in range(stages_number+2)]
    for x in range(stages_number):
        cashlesss_sorted[x].name=stages[x]
    cashlesss_sorted[x+1].name = "Получить товар"
    cashlesss_sorted[x+2].name = "Сдать документы"
    # Делаем класс a.name and a.list, делаем из него список по очереди
    # каждый класс - один из этапов
    for cl in cashlesss:
        # Для каждого чека делаем подсказку - что в нём
        title=""
        payment=cl.payment_set.get()
        assets=payment.asset_set.all()
        for asset in assets:
            title+=asset.model
            title+="; "
        title=title[:-2]
        # Старый варинат, проверял cl.dates, но делает логическую ошибку. Заменён
        # if cl.dates:
            # d=cl.dates.split(";")
            # for x in range(stages_number):
                # if not d[x]:
                    # cashlesss_sorted[x].set.append(Bill_with_title(cl,title))
                    # break
        # else:
            # cashlesss_sorted[0].set.append(Bill_with_title(cl,title))
        # if not cl.date_of_assets:
            # cashlesss_sorted[x+1].set.append(Bill_with_title(cl,title))   
            # continue
        # if not cl.date_of_documents:
            # cashlesss_sorted[x+2].set.append(Bill_with_title(cl,title))
            # continue
            
        # Новый вариант:
        d=cl.dates.split(";")
        for x in range(stages_number):
            if not d[x]:
                cashlesss_sorted[x].set.append(Bill_with_title(cl,title))
                break
        else:
            if not cl.date_of_assets:
                cashlesss_sorted[x+1].set.append(Bill_with_title(cl,title))   
                continue
            if not cl.date_of_documents:
                cashlesss_sorted[x+2].set.append(Bill_with_title(cl,title))
                continue
    # raise ImportError
    return (True,('all_bills.html',{},{'title':'Список всех счетов и чеков','cashs':cashs, 'cashlesss':cashlesss_sorted,'stages':stages,'stages_range':range(stages_number)},request,app))
@login_required
@multilanguage
def show_bill(request,type,id):
    bill_types={'cash':Cash,'cashless':Cashless}
    bill=bill_types[type].objects.get(id=id)
    payment=bill.payment_set.get()
    assets=payment.asset_set.all()
    for asset in assets:
        asset.place=asset.place_asset_set.latest('installation_date').place.place
    if type=='cashless':
        # если безнал - надо получить пройденные этапы и не пройденные и предоставить возможность их пройти в "пакетном режиме"
        from user_settings.functions import get_stages
        stages = get_stages(";").split(";")
        # Класс для отображения в шаблоне этапов с датами по порядку
        class Stages_info():
            class Stage():
                def __init__(self,n,d):
                    self.name = n
                    self.date = d
                    self.id_name = n.replace(" ","_")
            def __init__(self):
                self.items=[]
                for x in stages:
                    self.items.append(self.Stage(x,""))
                self.items.append(self.Stage("Товар получен",""))
                self.items.append(self.Stage("Документы сданы",""))
            def edit(self,n,d):
                self.items[n].date=d
            def date_of_assets(self,d):
                self.items[-2].date=d
            def date_of_documents(self,d):
                self.items[-1].date=d
        si = Stages_info()
        if bill.dates:
            d=bill.dates.split(";")
            for x in range(len(stages)):
                if not d[x]:
                    pass
                else:
                    si.edit(x,d[x])
        if bill.date_of_assets:
            si.date_of_assets(bill.date_of_assets)
        if bill.date_of_documents:
            si.date_of_documents(bill.date_of_documents)
        return (True,('show_bill.html',{},{'bill':bill,'assets':assets,'cashles':True,'stages_info':si},request,app))



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