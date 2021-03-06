# -*- coding:utf-8 -*-
# coding=<utf8>

from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.admin import widgets

##from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext as _

from assets.models import Asset, Payment, Cash, Cashless, Contractor, Garanty, Asset_type, Status, Budget, Repair, Place_Asset, Place, Cartridge, Cartridge_Model_General_Model, Cartridge_General_Model_Printer_Model, Cartridge_Printer, ROM, Cooler, Storage, Acoustics, Telephone, Battery, Optical_Drive, Printer, Power_suply, Motherboard, CPU, Case, Claim, CKC, Telephone_Works, UPS
from todoes.models import  Person #, Task, ProblemByWorker, ProblemByUser, Categories, RegularTask, Activity, Note, Resource, File,
import datetime

PRIORITY_CHOICES = (
        ('1','Лазар/Борода/Мотя'),
        ('2','Если не сделать сейчас - огребём проблем потом'),
        ('3','Всё остальное'),
        ('4','В ближайшем будущем'),
        ('5','Когда время будет')
    )
ASSET_TYPES_CATALOGUE_NAME = (
        ('ROM','ROM'),
        ('Cooler','Cooler'),
        ('Storage','Storage'),
        ('Acoustics','Acoustics'),
        ('Telephone','Telephone'),
        ('Battery','Battery'),
        ('Optical_Drive','Optical_Drive'),
        ('Printer','Printer'),
        ('Power_suply','Power_suply'),
        ('Motherboard','Motherboard'),
        ('CPU','CPU'),
        ('Case','Case'),
        ('CKC','CKC'),
        ('Telephone_Works','Telephone_Works'),
        ('UPS','UPS'),
        ('Delivery','Delivery'),

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
    # model = forms.CharField(max_length=140, label='Модель')
    price = forms.DecimalField(min_value=0, decimal_places=2, max_digits=8, initial=0, label='Цена')
    current_place = forms.ModelChoiceField(queryset  = Place.objects.all(), label='Место расположения')
    status = forms.ModelChoiceField(queryset  = Status.objects.all(), label='Статус')
    guarantee_period = forms.DecimalField(min_value=0, max_value=9999, initial=0,label='Срок гарантии, месяцев')
    note = forms.CharField(widget=forms.Textarea(attrs={'cols': 20}), label='Примечания',required=False)

    def __init__(self,arg_dict):
        # print str(kwargs)
        self.number = arg_dict.pop('number','')
        # print self.number
        super(NewAssetForm, self).__init__(arg_dict)
    def add_prefix(self, field_name):
        # print "doing prefix"
        field_name = str(self.number)+"_"+field_name
        return super(NewAssetForm, self).add_prefix(field_name)

class NewCashBillForm(forms.Form):
    date = forms.DateField(initial=datetime.date.today,help_text='Пустое значение означает текущую дату',required=False,input_formats=inp_f)
    garanty = forms.IntegerField(min_value=0)
    bill_number = forms.CharField(max_length=40)
    def __init__(self, *args, **kwargs):
        super(NewCashBillForm, self).__init__(*args, **kwargs)
        self.fields['date'].label = _("Check/Buy/Input date")
        self.fields['garanty'].label = _("Garanty number")
        self.fields['bill_number'].label = _("Check number")

class NewContractorForm(forms.Form):
    name = forms.CharField(max_length=140, label='Название фирмы')
    email = forms.EmailField(label = 'Мыло',required=False)
    tel = forms.CharField(label='Телефон', max_length=10, min_length=10,required=False)
    tel_of_support = forms.CharField(label='Телефон службы поддержки', max_length=10, min_length=10,required=False)
    contact_name = forms.CharField(max_length=140, label='ФИО контактного лица')
class NewAssetTypeForm(forms.Form):
    asset_type = forms.CharField(max_length=200,label="Тип актива")
    catalogue_name = forms.ChoiceField(choices = ASSET_TYPES_CATALOGUE_NAME, label='Таблица в справочнике')

# Формы для добавления новых моделей
class NewModel_Printer(ModelForm):
    class Meta:
        model = Printer
        fields = '__all__' # for 1.8
        localized_fields = '__all__'
class NewModel_Cartridge_Model_General_Model(ModelForm):
    class Meta:
        model = Cartridge_Model_General_Model
        fields = '__all__'
        localized_fields = '__all__'
class NewModel_CKC(ModelForm):
    class Meta:
        model = CKC
        fields = '__all__'
        localized_fields = '__all__'
class NewModel_Telephone_Works(ModelForm):
    class Meta:
        model = Telephone_Works
        fields = '__all__'
        localized_fields = '__all__'
class NewModel_UPS(ModelForm):
    class Meta:
        model = UPS
        fields = '__all__'
        localized_fields = '__all__'
class NewModel_Storage(ModelForm):
    class Meta:
        model = Storage
        fields = '__all__'
        localized_fields = '__all__'
class NewModel_Cooler(ModelForm):
    class Meta:
        model = Cooler
        fields = '__all__'
        localized_fields = '__all__'
class NewModel_ROM(ModelForm):
    class Meta:
        model = ROM
        fields = '__all__'
        localized_fields = '__all__'
class NewModel_Power_suply(ModelForm):
    class Meta:
        model = Power_suply
        fields = '__all__'
        localized_fields = '__all__'
class NewModel_Motherboard(ModelForm):
    class Meta:
        model = Motherboard
        fields = '__all__'
        localized_fields = '__all__'
class NewModel_CPU(ModelForm):
    class Meta:
        model = CPU
        fields = '__all__'
        localized_fields = '__all__'
class NewModel_Case(ModelForm):
    class Meta:
        model = Case
        fields = '__all__'
        localized_fields = '__all__'