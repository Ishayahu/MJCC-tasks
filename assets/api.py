# -*- coding:utf-8 -*-
# coding=<utf8>

import datetime
from itertools import chain

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
def get_asset_add_form(request,asset_category,form_number=''):
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
    # form = l_forms[lang]['NewAssetForm'](number=form_number)
    # return render_to_response(languages[lang]+'get_asset_add_form.html', {'number':form_number,'asset_type':asset_type,'form':form, 'method':method},RequestContext(request))
    return (True,('get_asset_add_form.html', {'NewAssetForm':{'number':form_number}},{'number':form_number,'asset_type':asset_type, 'method':method},request,app))
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
        return t.render(c)
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
    # form = l_forms[lang]['NewContractorForm']({'name':contractor_name})
    return (True,('get_new_contractor_add_form.html', {'NewContractorForm':{'name':contractor_name}},{'method':method},request,app))
    # return render_to_response(languages[lang]+'get_new_contractor_add_form.html', {'form':form, 'method':method},RequestContext(request)) 
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
            html='<input type="hidden" id="c_id" value="%s" /><input type="hidden" id="c_name" value="%s" />' % (c.id, c.name)
            return (True,('OK.html', {'NewContractorForm':{'name':contractor_name}},{'method':method},request,app))
            # return render_to_response(languages[lang]+'OK.html', {'c':c,'html':html},RequestContext(request))
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
            return t.render(c)
        c = Context({'items':type_names,'input_id_name':'asset_type_id'})
        return t.render(c)
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
    try:
        a = Asset.objects.get(id=id)
    except Asset.DoesNotExist:
        add_error(u"Актив с номером %s не найден!" % id,request)
        return (False,(HttpResponseRedirect("/assets_by_type/"+type_id+"/")))
    a.delete()
    html='Актив %s удалён' % id
    return (True,('OK.html', {},{},request,app))