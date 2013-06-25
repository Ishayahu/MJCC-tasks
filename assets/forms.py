# -*- coding:utf-8 -*-
# coding=<utf8>

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.admin import widgets

from assets.models import Asset, Payment, Cash, Cashless, Contractor, Garanty, Asset_type, Status, Budget, Repair, Place_Asset, Place, Cartridge, Cartridge_Model_General_Model, Cartridge_General_Model_Printer_Model, Cartridge_Printer, ROM, Cooler, Storage, Acoustics, Telephone, Battery, Optical_Drive, Printer, Power_suply, Motherboard, CPU, Case, Claim
from todoes.models import  Person #, Task, ProblemByWorker, ProblemByUser, Categories, RegularTask, Activity, Note, Resource, File,

PRIORITY_CHOICES = (
        ('1','Лазар/Борода/Мотя'),
        ('2','Если не сделать сейчас - огребём проблем потом'),
        ('3','Всё остальное'),
        ('4','В ближайшем будущем'),
        ('5','Когда время будет')
    )

inp_f=( '%d-%m-%Y %H:%M:%S',     # '2006-10-25 14:30:59'
        '%d-%m-%Y %H:%M',        # '2006-10-25 14:30'
        '%Y-%m-%d %H:%M:%S',     # '2006-10-25 14:30'
        '%d-%m-%Y',              # '2006-10-25'
        '%d/%m/%Y %H:%M:%S',     # '10/25/2006 14:30:59'
        '%d/%m/%Y %H:%M',        # '10/25/2006 14:30'
        '%d/%m/%Y',              # '10/25/2006'
        '%d.%m.%Y %H:%M:%S',     # '10/25/2006 14:30:59'
        '%Y.%m.%d %H:%M:%S',     # '2010/01/26 14:30:59'
        '%d/%m/%y %H:%M:%S',     # '10/25/06 14:30:59'
        '%d/%m/%y %H:%M',        # '10/25/06 14:30'
        '%d/%m/%y',       )
        
class NewAssetForm(forms.Form):
    model = forms.CharField(max_length=140, label='Модель')
    asset_type = forms.ModelChoiceField(queryset  = Asset_type.objects.all(), label='Тип актива')
    payment = forms.ModelChoiceField(queryset  = Payment.objects.all(), label='Оплата')    
    garanty = forms.ModelChoiceField(queryset  = Garanty.objects.all(), label='Номер гарантии')
    current_place = forms.ModelChoiceField(queryset  = Place_Asset.objects.all(), label='Место расположения')
    status = forms.ModelChoiceField(queryset  = Status.objects.all(), label='Статус')
    claim = forms.ModelChoiceField(queryset  = Claim.objects.all(), label='Заявка',required=False)
    guarantee_period = forms.DecimalField(min_value=0, max_value=9999, label='Срок гарантии, месяцев')    
    note = forms.CharField(widget=forms.Textarea, label='Примечания')    
    
#    pbus = forms.ModelChoiceField(queryset  = ProblemByUser.objects.all(), label='Проблема со слов пользователя')
#    description = forms.CharField(widget=forms.Textarea, label='Описание')
#    clients = forms.ModelChoiceField(queryset  = Person.objects.all(), label='Заявитель')
#    priority = forms.ChoiceField(widget=forms.RadioSelect,choices = PRIORITY_CHOICES, label='Приоритет')
#    category = forms.ModelChoiceField(queryset  = Categories.objects.all(), label='Категория')
#    start_date = forms.DateTimeField(label='Дата создания заявки')
#    due_date = forms.DateTimeField(label='Предполагаемая дата завершения',input_formats=inp_f)
#    workers = forms.ModelChoiceField(queryset  = Person.objects.all(), label='Исполнитель')
#    percentage = forms.DecimalField(min_value=0, max_value=100, label='Процент выполнения')