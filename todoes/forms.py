# -*- coding:utf-8 -*-
# coding=<utf8>

#TODO: сделать английские формы

from django import forms
from todoes.models import Note, Resource, File, Person, Task, ProblemByWorker, ProblemByUser, Categories
# from tasks.todoes.models import Worker, Client
from django.contrib.auth.forms import UserCreationForm
from django.contrib.admin import widgets

RUS_PRIORITY_CHOICES = (
        ('1','Лазар/Борода/Мотя'),
        ('2','Если не сделать сейчас - огребём проблем потом'),
        ('3','Всё остальное'),
        ('4','В ближайшем будущем'),
        ('5','Когда время будет')
    )
ENG_PRIORITY_CHOICES = (
        ('1','Lazar/Boroda/Motya'),
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
class NewTicketForm(forms.Form):
    name = forms.CharField(max_length=140, label='Название заявки')
    pbus = forms.ModelChoiceField(queryset  = ProblemByUser.objects.all(), label='Проблема со слов пользователя')
    description = forms.CharField(widget=forms.Textarea, label='Описание')
    clients = forms.ModelChoiceField(queryset  = Person.objects.all(), label='Заявитель')
    priority = forms.ChoiceField(widget=forms.RadioSelect,choices = PRIORITY_CHOICES, label='Приоритет')
    category = forms.ModelChoiceField(queryset  = Categories.objects.all(), label='Категория')
    start_date = forms.DateTimeField(label='Дата создания заявки')
    due_date = forms.DateTimeField(label='Предполагаемая дата завершения',input_formats=inp_f)
    workers = forms.ModelChoiceField(queryset  = Person.objects.all(), label='Исполнитель')
    percentage = forms.DecimalField(min_value=0, max_value=100, label='Процент выполнения')
    
class TicketEditForm(forms.Form):
    name = forms.CharField(max_length=140, label='Название заявки')
    pbus = forms.ModelChoiceField(queryset  = ProblemByUser.objects.all(), label='Проблема со слов пользователя')
    description = forms.CharField(widget=forms.Textarea, label='Описание')
    clients = forms.ModelChoiceField(queryset  = Person.objects.all(), label='Заявитель')
    priority = forms.ChoiceField(choices = PRIORITY_CHOICES, label='Приоритет')
    category = forms.ModelChoiceField(queryset  = Categories.objects.all(), label='Категория')
    start_date = forms.DateTimeField(label='Дата создания заявки',input_formats=inp_f)
    when_to_reminder = forms.DateTimeField(label='Установить напоминание',input_formats=inp_f,required=False)
    due_date = forms.DateTimeField(label='Предполагаемая дата завершения',input_formats=inp_f)
    workers = forms.ModelChoiceField(queryset  = Person.objects.all(), label='Исполнитель')
    percentage = forms.DecimalField(min_value=0, max_value=100, label='Процент выполнения')
class NewRegularTicketForm(forms.Form):
    name = forms.CharField(max_length=140, label='Название заявки')
    description = forms.CharField(widget=forms.Textarea, label='Описание',required=False)
    clients = forms.ModelChoiceField(queryset  = Person.objects.all(), label='Заявитель')
    priority = forms.ChoiceField(widget=forms.RadioSelect,choices = PRIORITY_CHOICES, label='Приоритет')
    category = forms.ModelChoiceField(queryset  = Categories.objects.all(), label='Категория')
    start_date = forms.DateTimeField(label='Дата создания заявки',input_formats=inp_f)
    stop_date = forms.DateTimeField(label='Дата завершения',input_formats=inp_f,required=False)
    workers = forms.ModelChoiceField(queryset  = Person.objects.all(), label='Исполнитель')
class EditRegularTicketForm(forms.Form):
    name = forms.CharField(max_length=140, label='Название заявки')
    description = forms.CharField(widget=forms.Textarea, label='Описание',required=False)
    clients = forms.ModelChoiceField(queryset  = Person.objects.all(), label='Заявитель')
    priority = forms.ChoiceField(widget=forms.RadioSelect,choices = PRIORITY_CHOICES, label='Приоритет')
    category = forms.ModelChoiceField(queryset  = Categories.objects.all(), label='Категория')
    start_date = forms.DateTimeField(label='Дата создания заявки',input_formats=inp_f)
    when_to_reminder = forms.DateTimeField(label='Установить напоминание',input_formats=inp_f,required=False)
    stop_date = forms.DateTimeField(label='Дата завершения',input_formats=inp_f,required=False)
    workers = forms.ModelChoiceField(queryset  = Person.objects.all(), label='Исполнитель')

class TicketClosingForm(forms.Form):
    done_date = forms.DateTimeField(label='Дата закрытия заявки',input_formats=inp_f)
    pbw = forms.ModelChoiceField(queryset  = ProblemByWorker.objects.all(), label='Выявленная проблема')
class TicketConfirmingForm(forms.Form):
    confirmed = forms.BooleanField(required=False)
    confirmed_date = forms.DateTimeField(label='Дата подтверждения закрытия заявки',input_formats=inp_f)
    
# class NoteToTicketAddForm(forms.Form):
    # note = forms.CharField(widget=forms.Textarea, label='Комментарий',required=False )
    # workers = forms.ModelMultipleChoiceField(queryset  = Person.objects.all(), label='Кого ещё уведомить о комментарии?',required=False)

    
class UserCreationFormMY(UserCreationForm):
    fio = forms.CharField(label='ФИО')
    mail = forms.EmailField(label = 'Мыло')
    tel = forms.CharField(label='Телефон', max_length=10, min_length=10)
    
class TicketSearchForm(forms.Form):
    name = forms.CharField(max_length=140, label='Текст для поиска')

class NoteToTicketAddForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.defaults = kwargs.pop('defaults','')
        self.exclude = kwargs.pop('exclude','')
        super(NoteToTicketAddForm, self).__init__(*args, **kwargs)
        self.fields['workers'].queryset = Person.objects.exclude(fio__in = [person.fio for person in self.exclude ])
        self.fields['workers'].initial = Person.objects.filter(fio__in = self.defaults)

    note = forms.CharField(widget=forms.Textarea, label='Комментарий',required=False )
    workers = forms.ModelMultipleChoiceField(queryset  = Person.objects.all(), label='Кого ещё уведомить о комментарии?',required=False,)
class File_and_NoteToTicketAddForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.defaults = kwargs.pop('defaults','')
        self.exclude = kwargs.pop('exclude','')
        super(File_and_NoteToTicketAddForm, self).__init__(*args, **kwargs)
        self.fields['workers'].queryset = Person.objects.exclude(fio__in = [person.fio for person in self.exclude ])
        self.fields['workers'].initial = Person.objects.filter(fio__in = self.defaults)

    note = forms.CharField(widget=forms.Textarea, label='Комментарий',required=False )
    file  = forms.FileField()
    workers = forms.ModelMultipleChoiceField(queryset  = Person.objects.all(), label='Кого ещё уведомить о комментарии?',required=False,)
