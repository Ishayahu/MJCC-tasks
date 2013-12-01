# -*- coding:utf-8 -*-
# coding=<utf8>

import datetime
from itertools import chain
import json

from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render_to_response
from assets.models import Asset, Payment, Cash, Cashless, Contractor, Garanty, Asset_type, Status, Budget, Repair, Place_Asset, Place, Cartridge, Cartridge_Model_General_Model, Cartridge_General_Model_Printer_Model, Cartridge_Printer, ROM, Cooler, Storage, Acoustics, Telephone, Battery, Optical_Drive, Printer, Power_suply, Motherboard, CPU, Case
from todoes.models import  Person #, Task, ProblemByWorker, ProblemByUser, Categories, RegularTask, Activity, Note, Resource, File,
# from assets.forms_rus import NewAssetForm_RUS, NewContractorForm_RUS
# from assets.forms_eng import NewAssetForm_ENG, NewContractorForm_ENG
from django.contrib.auth.decorators import login_required
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.template import RequestContext, loader, Context

from djlib.cron_utils import decronize, crontab_to_russian, generate_next_reminder
from djlib.text_utils import htmlize
from djlib.acl_utils import acl, for_admins, admins_only
from djlib.user_tracking import set_last_activity_model, get_last_activities
from djlib.mail_utils import send_email_alternative
from djlib.error_utils import FioError, ErrorMessage, add_error, shows_errors
from djlib.auxiliary import get_info
from djlib.logging_utils import log, confirm_log, make_request_with_logging

from user_settings.settings import server_ip, admins, admins_mail
from user_settings.functions import get_option_with_description,get_bd_option_with_description

try:
    from user_settings.settings import assets_url_not_to_track as url_not_to_track
except ImportError:
    url_not_to_track=('',)
try:
    from user_settings.settings import assets_url_one_record as url_one_record
except ImportError:
    url_one_record=('',)

# Делаем переводы
from djlib.multilanguage_utils import select_language,multilanguage,register_lang, get_localized_name, get_localized_form#,register_app

register_lang('ru','RUS')
register_lang('eng','ENG')
app='assets'
# languages={'ru':'RUS/',
            # 'eng':'ENG/'}
# forms_RUS = {'NewAssetForm':NewAssetForm_RUS, 'NewContractorForm':NewContractorForm_RUS}
# forms_ENG = {'NewAssetForm':NewAssetForm_ENG, 'NewContractorForm':NewContractorForm_ENG}
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
def get_asset_add_form(request,asset_category,form_number):
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
    # print form_number
    # функция для загрузки последней цены, срока гарантии + установка статуса в {{статус по умолчанию}} и места в {{место по умолчанию}} из настроек раздела [cashless] (из get_asset_add_form.html)
    # get_bd_option_with_description returns name,opt_id,opt_val,desc
    a,b,default_place,c = get_bd_option_with_description('cashless','default_place')
    a,b,default_status,c = get_bd_option_with_description('cashless','default_status')
    return (True,('get_asset_add_form.html', {'NewAssetForm':{'number':form_number}},{'default_place':default_place,'default_status':default_status,'number':form_number,'asset_type':asset_type, 'method':method},request,app))
@login_required
@multilanguage
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
        t = loader.get_template(get_localized_name('get_contractors_list.html',request))
        c = Context({'contractors':contractors})
        return (False,(t.render(c)))
    return (True,('get_contractors_list.html', {},{'contractors':contractors,'contractor':contractor,'name_to_select':name_to_select},request,app))
    # return render_to_response(languages[lang]+'get_contractors_list.html', {'contractors':contractors,'contractor':contractor,'name_to_select':name_to_select},RequestContext(request))
@login_required
@multilanguage
def get_new_contractor_add_form(request, contractor_name):
    lang=select_language(request)
    user = request.user.username
    try:
        fio = Person.objects.get(login=user)
    except Person.DoesNotExist:
        fio = FioError()
    method = request.method
    return (True,('get_new_contractor_add_form.html', {'NewContractorForm':{'name':contractor_name}},{'method':method},request,app))
@login_required
@multilanguage
def save_new_contractor(request):
    lang=select_language(request)
    user = request.user.username
    try:
        fio = Person.objects.get(login=user)
    except Person.DoesNotExist:
        fio = FioError()
    method = request.method
    if request.method == 'POST':
        form = get_localized_form('NewContractorForm',app,request)(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            c=Contractor(name = data['name'],
                        tel = data['tel'],
                        email = data['email'],
                        tel_of_support = data['tel_of_support'],
                        contact_name = data['contact_name'],)
            c.save()
            html=u'<input type="hidden" id="c_id" value="%s" /><input type="hidden" id="c_name" value="%s" />' % (c.id, c.name)
            return (True,('OK.html', {},{'html':html},request,app))
            # return render_to_response(languages[lang]+'OK.html', {'c':c,'html':html},RequestContext(request))
    raise IOError
    return "Произошла какая-то ошибка, но не могу представить какая. Надо выяснить и записать для диагностики"
@login_required
@multilanguage
@shows_errors
def get_asset_type_list(request,id=-1,internal=False):
    lang=select_language(request)
    user = request.user.username
    try:
        fio = Person.objects.get(login=user)
    except Person.DoesNotExist:
        fio = FioError()
    type_names = Asset_type.objects.all()
    for item in type_names:
        item.name=item.asset_type
    method = request.method
    # если для встраивания
    if internal:
        t = loader.get_template(get_localized_name('get_list.html',request))
        if id!=-1:
            c = Context({'items':type_names,'input_id_name':'asset_type_id','selected_item_id':id})
            return (False,(t.render(c)))
        c = Context({'items':type_names,'input_id_name':'asset_type_id'})
        return (False,(t.render(c)))
    if id!=-1:
        return render_to_response(languages[lang]+'get_list.html', {'items':type_names,'input_id_name':'asset_type_id','selected_item_id':id},RequestContext(request))
    return (True,('get_list.html', {},{'items':type_names,'input_id_name':'asset_type_id'},request,app))
    # return render_to_response(languages[lang]+'get_list.html', {'items':type_names,'input_id_name':'asset_type_id'},RequestContext(request))
@login_required
@multilanguage
def mark_as_deleted_bill(request,b_type,id):
    bill_types={'cash':Cash,'cashless':Cashless}
    bill=bill_types[b_type].objects.get(id=id)
    payment=bill.payment_set.get()
    payment.deleted=True
    payment.save()
    return (False,(HttpResponseRedirect('/all_bills/')))
@login_required
@multilanguage
@shows_errors
def full_delete_bill(request,b_type,id):
    # print "in full_delete_bill"
    bill_types={'cash':Cash,'cashless':Cashless}
    bill=bill_types[b_type].objects.get(id=id)
    payment=bill.payment_set.get()
    if not payment.deleted:
        add_error(u"Этот чек/счёт ещё не удалён! id=%s тип %s" % (id,b_type),request)
        # print "added error: "+str(request.session['my_error'])
        request.session.modified = True
        return (False,(HttpResponseRedirect('/all_bills/')))
    assets=payment.asset_set.all()
    for asset in assets:
        asset.delete()
    payment.delete()
    bill.delete()
    return (False,(HttpResponseRedirect('/all_bills/')))
@login_required
@multilanguage
@shows_errors
@for_admins
def assets_by_type(request,type_id):
    lang,user,fio,method = get_info(request)
    assets = Asset.objects.filter(asset_type=type_id)
    asset_types = Asset_type.objects.all()
    for asset in assets:
        asset.place=asset.place_asset_set.latest('installation_date').place.place
    return (True,('assets_by_type_table.html',{},{'assets':assets},request,app))
@login_required
@multilanguage
@admins_only
# @for_admins
def asset_delete(request,id,type_id):
    lang,user,fio,method = get_info(request)
    try:
        a = Asset.objects.get(id=id)
    except Asset.DoesNotExist:
        add_error(u"Актив с номером %s не найден!" % id,request)
        # return (False,(HttpResponseRedirect("/assets_by_type/"+type_id+"/")))
        return (False,(HttpResponseRedirect("/")))
    a=make_request_with_logging(user,"Удаляем актив №%s" % str(id),a.delete,{})
    html=u'Актив %s удалён' % str(id)
    return (True,('OK.html', {},{'html':html},request,app))
@login_required
@multilanguage
@admins_only
def asset_edit(request,id):
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
@login_required
@multilanguage
@admins_only
def get_models_list_json(request,asset_type_id):
    at = Asset_type.objects.get(id=catalogue_name)
    at_name = at.catalogue_name
    response_data['result'] = 'failed'
    response_data['message'] = 'You messed up'
    return HttpResponse(json.dumps(response_data), mimetype="application/json")
@login_required
@multilanguage
@shows_errors
def get_new_asset_type_add_form(request):
    lang=select_language(request)
    user = request.user.username
    try:
        fio = Person.objects.get(login=user)
    except Person.DoesNotExist:
        fio = FioError()
    method = request.method
    return (True,('get_new_asset_type_add_form.html', {'NewAssetTypeForm':{}},{'method':method},request,app))
@login_required
@multilanguage
@shows_errors
def get_new_asset_type_save(request):
    lang=select_language(request)
    user = request.user.username
    try:
        fio = Person.objects.get(login=user)
    except Person.DoesNotExist:
        fio = FioError()
    method = request.method
    if request.method == 'POST':
        form = get_localized_form('NewAssetTypeForm',app,request)(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            at=Asset_type(asset_type = data['asset_type'],
                        catalogue_name = data['catalogue_name'],
                        )
            at.save()
            # html='<input type="hidden" id="c_id" value="%s" /><input type="hidden" id="c_name" value="%s" />' % (c.id, c.name)
            # return (True,('OK.html', {},{},request,app))
            # return render_to_response(languages[lang]+'OK.html', {'c':c,'html':html},RequestContext(request))
            return (False,(HttpResponseRedirect("/assets_by_type/"+str(at.id)+"/")))
    raise IOError("Произошла какая-то ошибка, но не могу представить какая. Надо выяснить и записать для диагностики")
@login_required
@multilanguage
@shows_errors
def asset_save_edited(request,asset_id):
    asset = Asset.objects.get(id=asset_id)
    asset.model = request.POST.get('model_'+asset_id)
    asset.price = request.POST.get('price_'+asset_id)
    asset.status = Status.objects.get(id=request.POST.get('status_'+asset_id))
    asset.garanty = Garanty.objects.get(id=request.POST.get('garanty_'+asset_id))
    asset.place = Place.objects.get(id=request.POST.get('place_'+asset_id))
    asset.save()
    return (True,('edited_asset.html',{},{'item':asset,},request,app))
@login_required
@multilanguage
@shows_errors
def json_models(request,asset_type_id):
    asset_type = Asset_type.objects.get(id=asset_type_id)
    models_module_name = 'assets.models'
    asset_type_model_name = asset_type.catalogue_name
    app_module = __import__(models_module_name)
    models_model = getattr(app_module,'models')
    asset_type_model = getattr(models_model,asset_type_model_name)
    models = asset_type_model.objects.all().values('model_name')
    mj = list(set([i['model_name']for i in models]))
    return (False,HttpResponse(json.dumps(mj), mimetype="application/json"))
@login_required
@multilanguage
@shows_errors
def json_price_and_warranty(request):
    lang,user,fio,method = get_info(request)
    if request.method == 'POST':
        model = request.POST.get('model')
        contractor = request.POST.get('contractor')
        ass = Asset.objects.filter(model=model)
        assets = []
        for asset in ass:
            try:
                ass_contractor = asset.payment.cash.contractor.name
                asset.data = asset.payment.cash.date
            except AttributeError:
                ass_contractor = asset.payment.cashless.contractor.name
                asset.data = asset.payment.cashless.date_of_invoice
            if ass_contractor == contractor:
                assets.append(asset)
        def sort_key(a):
            return a.data
        assets.sort(key=sort_key,reverse=True)
        # То что нужно - assets[0]
        # Возвращаем JSON
        try:
            a={'price':float(assets[0].price),'warranty':assets[0].guarantee_period}
        except IndexError:
            a={'price':0,'warranty':0}
        a=json.dumps(a)
        return (False,HttpResponse(a, mimetype="application/json"))
        
@login_required
@multilanguage
@shows_errors
def get_new_asset_model_add_form(request,asset_type_id,asset_model_name):
    lang=select_language(request)
    user = request.user.username
    try:
        fio = Person.objects.get(login=user)
    except Person.DoesNotExist:
        fio = FioError()
    method = request.method
    asset_type = Asset_type.objects.get(id=asset_type_id)
    form_name = 'NewModel_'+asset_type.catalogue_name
    return (True,('get_new_asset_model_add_form.html', {form_name:{'model_name':asset_model_name}},{'method':method,'form_template_name':'NewModelForm','asset_type_id':asset_type_id},request,app))
@login_required
@multilanguage
@shows_errors
def save_new_model(request,asset_type_id):
    lang=select_language(request)
    user = request.user.username
    try:
        fio = Person.objects.get(login=user)
    except Person.DoesNotExist:
        fio = FioError()
    method = request.method
    asset_type = Asset_type.objects.get(id=asset_type_id)
    form_name = 'NewModel_'+asset_type.catalogue_name
##    print form_name
    if request.method == 'POST':
        # f = ArticleForm(request.POST)
        f = get_localized_form(form_name,app,request)(request.POST)
        if f.is_valid():
            # Save a new object from the form's data.
##            print form_name
##            print f
            new_model=f.save()
            return (True,('OK.html', {},{'html':u'Модель '+new_model.model_name+u' успешно добавлена в базу'},request,app))
        else:
##            print "Not valid"
            pass
    return (True,('OK.html', {},{'html':u'Случилась неведомая фигня в функции api.save_new_model'},request,app))
@login_required
@multilanguage
def cashless_edit_stages(request,bill_number,stage_name,new_stage,not_redirect):
    print stage_name
    cl=Cashless.objects.get(id=bill_number)
    today=str(datetime.datetime.today()).split(' ')[0].replace('-','.') # '2013.10.21'
    today_dash=str(datetime.datetime.today()) # '2013-10-21'
    if stage_name in cl.stages.split(';'):
    # Если меняется дата этапа из настроек
        stage_number=cl.stages.split(';').index(stage_name)
        if new_stage=='1':
            dates=cl.dates.split(';')
            dates[stage_number] = today
            cl.dates = ';'.join(dates)
            cl.save()
        else:
            dates=cl.dates.split(';')
            dates[stage_number] = ''
            cl.dates = ';'.join(dates)
            cl.save()
    # Если меняется дата получения товара и сдачи документов в бухгалтерию
    if stage_name==u'Товар_получен':
        assets = cl.payment_set.get().asset_set.filter()
        status_reserved = Status.objects.get(status="Заказан")
        status_new =  Status.objects.get(status="Новый")
        if new_stage=='1':
            cl.date_of_assets = today_dash
            cl.save()
            # Теперь надо активировать полученный товар в базе
            for asset in assets:
                asset.status = status_new
                asset.save()
        else:
            cl.date_of_assets = None
            cl.save()
            # Теперь надо перенести полученный товар обратно в зарезервированный
            for asset in assets:
                asset.status = status_reserved
                asset.save()
    if stage_name==u'Документы_сданы':
        if new_stage=='1':
            cl.date_of_documents = today_dash
            cl.save()
        else:
            cl.date_of_documents = None
            cl.save()
    # из views.show_bill для построения новой таблицы
    # если безнал - надо получить пройденные этапы и не пройденные и предоставить возможность их пройти в "пакетном режиме"
    # from user_settings.functions import get_stages
    
    # Мы должны пользоваться теми этапами, которые предусмотрены для счёта
    stages = cl.stages.split(';')
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
    if cl.dates:
        d=cl.dates.split(";")
        for x in range(len(stages)):
            if not d[x]:
                #break
                pass
            else:
                si.edit(x,d[x])
    if cl.date_of_assets:
        si.date_of_assets(cl.date_of_assets)
    if cl.date_of_documents:
        si.date_of_documents(cl.date_of_documents)
    if not_redirect=='1':
        return (True,('stages_table.html', {},{'stages_info':si},request,app))
    return (False,(HttpResponseRedirect('/all_bills/')))
