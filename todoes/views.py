# -*- coding:utf-8 -*-
# coding=<utf8>


#TODO: сделать возможность изменения языков
__version__ = '0.2.3d'


from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render_to_response
import datetime
from todoes.models import Note, Resource, File, Person, Task, ProblemByWorker, ProblemByUser, Categories, RegularTask, Activity
from todoes.forms_rus import NewTicketForm_RUS, NoteToTicketAddForm_RUS, UserCreationFormMY_RUS, TicketClosingForm_RUS, TicketConfirmingForm_RUS, TicketEditForm_RUS,TicketSearchForm_RUS, NewRegularTicketForm_RUS, EditRegularTicketForm_RUS, File_and_NoteToTicketAddForm_RUS
from todoes.forms_eng import NewTicketForm_ENG, NoteToTicketAddForm_ENG, UserCreationFormMY_ENG, TicketClosingForm_ENG, TicketConfirmingForm_ENG, TicketEditForm_ENG,TicketSearchForm_ENG, NewRegularTicketForm_ENG, EditRegularTicketForm_ENG, File_and_NoteToTicketAddForm_ENG
from django.contrib.auth.decorators import login_required
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.template import RequestContext
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from itertools import chain

from djlib.cron_utils import decronize, crontab_to_russian, generate_next_reminder
from djlib.text_utils import htmlize
from djlib.acl_utils import acl, for_admins, admins_only
from djlib.user_tracking import set_last_activity_model, get_last_activities
from djlib.mail_utils import send_email_alternative
from djlib.error_utils import FioError, ErrorMessage, add_error, shows_errors

from user_settings.settings import server_ip, admins, admins_mail
try:
    from user_settings.settings import todoes_url_not_to_track as url_not_to_track
except ImportError:
    url_not_to_track=('',)
try:
    from user_settings.settings import todoes_url_one_record as url_one_record
except ImportError:
    url_one_record=('',)



from todoes.utils import build_note_tree, note_with_indent

task_types = {'one_time':Task,'regular':RegularTask}
task_addr = {'one_time':'one_time','regular':'regular'}

# Делаем переводы
from djlib.multilanguage_utils import select_language
languages={'ru':'RUS/',
            'eng':'ENG/'}
forms_RUS = {'NewTicketForm':NewTicketForm_RUS, 'NoteToTicketAddForm':NoteToTicketAddForm_RUS, 'UserCreationFormMY':UserCreationFormMY_RUS, 'TicketClosingForm':TicketClosingForm_RUS, 'TicketConfirmingForm':TicketConfirmingForm_RUS, 'TicketEditForm':TicketEditForm_RUS,'TicketSearchForm':TicketSearchForm_RUS, 'NewRegularTicketForm':NewRegularTicketForm_RUS, 'EditRegularTicketForm':EditRegularTicketForm_RUS, 'File_and_NoteToTicketAddForm':File_and_NoteToTicketAddForm_RUS}
forms_ENG = {'NewTicketForm':NewTicketForm_ENG, 'NoteToTicketAddForm':NoteToTicketAddForm_ENG, 'UserCreationFormMY':UserCreationFormMY_ENG, 'TicketClosingForm':TicketClosingForm_ENG, 'TicketConfirmingForm':TicketConfirmingForm_ENG, 'TicketEditForm':TicketEditForm_ENG,'TicketSearchForm':TicketSearchForm_ENG, 'NewRegularTicketForm':NewRegularTicketForm_ENG, 'EditRegularTicketForm':EditRegularTicketForm_ENG, 'File_and_NoteToTicketAddForm':File_and_NoteToTicketAddForm_ENG}
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
    #return render_to_response(languages[lang]+languages[lang]+'new_ticket.html', {'form':form, 'met......
    
    
def set_last_activity(login,url):
    set_last_activity_model(login,url,url_not_to_track,url_one_record)

@login_required
def new_ticket(request):
    lang=select_language(request)
    user = request.user.username
    try:
        fio = Person.objects.get(login=user)
    except Person.DoesNotExist:
        fio = FioError
    method = request.method
    if request.method == 'POST':
        form = l_forms[lang]['NewTicketForm'](request.POST)
        if form.is_valid():
            data = form.cleaned_data
            t=Task(name=data['name'], 
                pbu=data['pbus'], 
                description=data['description'], 
                client=data['clients'], 
                priority=data['priority'], 
                category=data['category'], 
                start_date=data['start_date'], 
                when_to_reminder = data['start_date'],
                due_date=data['due_date'], 
                worker=data['workers'],
                percentage=data['percentage'],
                acl = data['clients'].login+';'+data['workers'].login)
            t.save()
            send_email_alternative(u"Новая задача: "+t.name,u"*Описание*:\n\<table cellpadding='5' border='1'\>\<tr\>\<td\>"+t.description+u"\</tr\>\</td\>\</table\>\n\n*Посмотреть задачу можно тут*:\nhttp://"+server_ip+"/task/one_time/"+str(t.id),[data['workers'].mail,data['clients'].mail],fio)
            set_last_activity(user,request.path)
            return HttpResponseRedirect('/tasks/')
    else:
        form =l_forms[lang]['NewTicketForm']({'percentage':0,'start_date':datetime.datetime.now(),'due_date':datetime.datetime.now(),'priority':3})
    set_last_activity(user,request.path)
    return render_to_response(languages[lang]+'new_ticket.html', {'form':form, 'method':method},RequestContext(request))

@login_required
def new_regular_ticket(request):
    lang=select_language(request)
    user = request.user.username
    try:
        fio = Person.objects.get(login=user)
    except Person.DoesNotExist:
        fio = FioError()
    method = request.method
    if request.method == 'POST':
        form = NewRegularTicketForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            t=RegularTask(name=data['name'], 
                description=data['description'], 
                client=data['clients'], 
                priority=data['priority'], 
                category=data['category'], 
                start_date=data['start_date'], 
                next_date=data['start_date'],
                when_to_reminder = data['start_date'],
                stop_date=data['stop_date'], 
                worker=data['workers'],
                acl = data['clients'].login+';'+data['workers'].login,
                period = request.POST.get('cronized'))                
            t.save()
            # отправляем уведомление исполнителю по мылу
            send_email_alternative(u"Новая повторяющаяся задача: "+t.name,u"*Описание*:\n\<table cellpadding='5' border='1'\>\<tr\>\<td\>"+t.description+u"\</tr\>\</td\>\</table\>\n\n*Посмотреть задачу можно тут*:\nhttp://"+server_ip+"/task/regular/"+str(t.id),[data['workers'].mail,data['clients'].mail],fio)
            set_last_activity(user,request.path)
            return HttpResponseRedirect('/tasks/')
    else:
        form =l_forms[lang]['NewRegularTicketForm'] ({'start_date':datetime.datetime.now(),'due_date':datetime.datetime.now(),'priority':3})
    set_last_activity(user,request.path)
    return render_to_response(languages[lang]+'new_regular_task.html', {'page_title':u'Новая повторяющаяся задача','form':form, 'method':method},RequestContext(request))
@login_required
def edit_regular_task(request,task_to_edit_id):
    lang=select_language(request)
    if not acl(request,'regular',task_to_edit_id):
        request.session['my_error'] = u'Нет права доступа к этой задаче!'
        return HttpResponseRedirect("/tasks/")
    user = request.user.username
    try:
        fio = Person.objects.get(login=user)
    except Person.DoesNotExist:
        fio = FioError()
    task_to_edit = RegularTask.objects.get(id=task_to_edit_id)
    method = request.method
    if request.method == 'POST':
        form = EditRegularTicketForm(request.POST)
        # если меняется исполнитель - чтобы оповестить
        old_worker = task_to_edit.worker
        old_period = task_to_edit.period
        old_client = task_to_edit.client
        old_category = task_to_edit.category
        old_stop_date = task_to_edit.stop_date
        old_start_date = task_to_edit.start_date
        old_name = task_to_edit.name
        if form.is_valid() and request.POST.get('cronized'):
            data = form.cleaned_data
            task_to_edit.description=data['description']
            task_to_edit.client=data['clients']
            task_to_edit.priority=data['priority']
            task_to_edit.category=data['category'] 
            task_to_edit.start_date=data['start_date']
            task_to_edit.stop_date=data['stop_date']
            task_to_edit.worker=data['workers']
            task_to_edit.when_to_reminder=data['when_to_reminder']
            task_to_edit.period=request.POST.get('cronized')
            task_to_edit.save()            
            if task_to_edit.start_date != old_start_date:
                send_email_alternative(u"Изменена дата начала задачи: "+task_to_edit.name,
                           u"\<table cellpadding='5' border='1'\>\<tr\>\<td\>Прежняя дата начала\</td\>\<td\>"+str(old_start_date)+u"\</td\>\</tr\>\<tr\>\<td\>Новая дата начала\</td\>\<td\>"+str(task_to_edit.start_date)+u"\</td\>\</tr\>\</table\>\n\n*Описание задачи*\<table cellpadding='5' border='1'\>\<tr\>\<td\>"+task_to_edit.description+u"\</td\>\</tr\>\</table\>\n\n*Посмотреть задачу можно тут*:\nhttp://"+server_ip+"/task/one_time/"+str(task_to_edit.id),
                           [task_to_edit.worker.mail,task_to_edit.client.mail]+admins_mail,
                           fio
                           )
            if task_to_edit.name != old_name:
                send_email_alternative(u"Изменёно название задачи: "+old_name,
                           u"\<table cellpadding='5' border='1'\>\<tr\>\<td\>Прежнее название\</td\>\<td\>"+old_name+u"\</td\>\</tr\>\<tr\>\<td\>Новое название\</td\>\<td\>"+task_to_edit.name+u"\</td\>\</tr\>\<tr\>\<td\>Описание задачи\</td\>\<td\>"+task_to_edit.description+u"\</td\>\</tr\>\</table\>\n*Посмотреть задачу можно тут*:\nhttp://"+server_ip+"/task/regular/"+str(task_to_edit.id),
                           [task_to_edit.worker.mail,task_to_edit.client.mail]+admins_mail,
                           fio
                           )
            if task_to_edit.worker != old_worker:
                # добавление нового исполнителя в acl
                if task_to_edit.worker.login not in task_to_edit.acl:
                    task_to_edit.acl=task_to_edit.acl+";"+task_to_edit.worker.login
                    task_to_edit.save()
                send_email_alternative(u"Изменён исполнитель задачи: "+task_to_edit.name,
                           u"\<table cellpadding='5' border='1'\>\<tr\>\<td\>Прежний исполнитель\</td\>\<td\>"+old_worker.fio+u"\</td\>\</tr\>\<tr\>\<td\>Новый исполнитель\</td\>\<td\>"+task_to_edit.worker.fio+u"\</td\>\</tr\>\<tr\>\<td\>Описание задачи\</td\>\<td\>"+task_to_edit.description+u"\</td\>\</tr\>\</table\>\n*Посмотреть задачу можно тут*:\nhttp://"+server_ip+"/task/regular/"+str(task_to_edit.id),
                           [task_to_edit.worker.mail,task_to_edit.client.mail,old_worker.mail]+admins_mail,
                           fio
                           )
            if task_to_edit.stop_date != old_stop_date:
                send_email_alternative(u"Изменёна дата завершения регулярной задачи: "+task_to_edit.name,
                           u"\<table cellpadding='5' border='1'\>\<tr\>\<td\>Прежная проблема\</td\>\<td\>"+str(old_stop_date)+u"\</td\>\</tr\>\<tr\>\<td\>Новая проблема\</td\>\<td\>"+str(task_to_edit.stop_date)+u"\</td\>\</tr\>\<tr\>\<td\>Описание задачи\</td\>\<td\>"+task_to_edit.description+u"\</td\>\</tr\>\</table\>\n*Посмотреть задачу можно тут*:\nhttp://"+server_ip+"/task/regular/"+str(task_to_edit.id),
                           [task_to_edit.worker.mail,task_to_edit.client.mail]+admins_mail,
                           fio
                           )
            if task_to_edit.client != old_client:
                # добавление нового исполнителя в acl
                if task_to_edit.client.login not in task_to_edit.acl:
                    task_to_edit.acl=task_to_edit.acl+";"+task_to_edit.client.login
                    task_to_edit.save()
                send_email_alternative(u"Изменён заказчик задачи: "+task_to_edit.name,
                           u"\<table cellpadding='5' border='1'\>\<tr\>\<td\>Прежний заказчик\</td\>\<td\>"+old_client.fio+u"\</td\>\</tr\>\<tr\>\<td\>Новый заказчик\</td\>\<td\>"+task_to_edit.client.fio+u"\</td\>\</tr\>\<tr\>\<td\>Описание задачи\</td\>\<td\>"+task_to_edit.description+u"\</td\>\</tr\>\</table\>\n*Посмотреть задачу можно тут*:\nhttp://"+server_ip+"/task/regular/"+str(task_to_edit.id),
                           [task_to_edit.worker.mail,task_to_edit.client.mail,old_client.mail]+admins_mail,
                           fio
                           )
            if task_to_edit.category != old_category:
                send_email_alternative(u"Изменёна категория задачи: "+task_to_edit.name,
                           u"\<table cellpadding='5' border='1'\>\<tr\>\<td\>Прежная категория\</td\>\<td\>"+old_category.name+u"\</td\>\</tr\>\<tr\>\<td\>Новая категория\</td\>\<td\>"+task_to_edit.category.name+u"\</td\>\</tr\>\<tr\>\<td\>Описание задачи\</td\>\<td\>"+task_to_edit.description+u"\</td\>\</tr\>\</table\>\n*Посмотреть задачу можно тут*:\nhttp://"+server_ip+"/task/regular/"+str(task_to_edit.id),
                           [task_to_edit.worker.mail,task_to_edit.client.mail]+admins_mail,
                           fio
                           )
            if task_to_edit.period != old_period:
                send_email_alternative(u"Изменёна периодичность выполонения задачи: "+task_to_edit.name,
                           u"\<table cellpadding='5' border='1'\>\<tr\>\<td\>Старый срок\</td\>\<td\>"+crontab_to_russian(old_period)+u"\</td\>\</tr\>\<tr\>\<td\>Новый срок\</td\>\<td\>"+crontab_to_russian(task_to_edit.period)+u"\</td\>\</tr\>\<tr\>\<td\>Описание задачи\</td\>\<td\>"+task_to_edit.description+u"\</td\>\</tr\>\</table\>\n*Посмотреть задачу можно тут*:\nhttp://"+server_ip+"/task/regular/"+str(task_to_edit.id),
                           [task_to_edit.worker.mail,task_to_edit.client.mail]+admins_mail,
                           fio
                           )
            set_last_activity(user,request.path)
            return HttpResponseRedirect('/tasks/')
    else:
        form = l_forms[lang]['EditRegularTicketForm']({'name' : task_to_edit.name,
            'description' : task_to_edit.description,
            'clients' : task_to_edit.client,
            'priority' : task_to_edit.priority,
            'category' : task_to_edit.category,
            'start_date' : task_to_edit.start_date,
            'when_to_reminder' : task_to_edit.when_to_reminder,
            'stop_date' : task_to_edit.stop_date,
            'workers' : task_to_edit.worker,
        })
    set_last_activity(user,request.path)
    return render_to_response(languages[lang]+'new_regular_task.html', {'page_title':u'Редактировать повторяющуюся задачу','form':form, 'method':method,'period':task_to_edit.period,'russian_period':crontab_to_russian(task_to_edit.period)},RequestContext(request))

    
@login_required
def set_reminder(request,task_type,task_id):
    lang=select_language(request)
    if not acl(request,task_type,task_id):
        request.session['my_error'] = u'Нет права доступа к этой задаче!'
        return HttpResponseRedirect("/tasks/")

    # fix #52
    if request.session.get('my_error'):
        my_error = [request.session.get('my_error'),]
    else:
        my_error=[]
    request.session['my_error'] = ''
    # end fix #52

    user = request.user.username
    admin = False
    if user in admins:
        admin = True
    method = request.method
    data = 0
    time = 0
    try:
        task_full = task_types[task_type].objects.get(id = task_id)
    except:
        request.session['my_error'] = u'Задача почему-то не ' \
                                      u'найдена. Номер ошибки ' \
                                      u'set_reminder_253!'
        return HttpResponseRedirect('/tasks/')
    if request.method == 'POST':
        if 'datepicker' in request.POST:
            data = request.POST['datepicker']
        if 'time' in request.POST:
            time = request.POST['time']
        dtt = datetime.datetime(*map(int,([data.strip().split('/')[2],data.strip().split('/')[1],data.strip().split('/')[0]]+time.strip().split(':'))))

        # fix #52
        # https://github.com/Ishayahu/MJCC-tasks/issues/52
        # Напоминание не может встать позже, чем дата завершения
        # в таком случае надо выдать ошибку
        if dtt>task_full.due_date:
            request.session['my_error'] = u'Невозможно установить ' \
                                          u'напоминане на дату ' \
                                          u'позже, чем срок ' \
                                          u'завершения!'
            # return HttpResponseRedirect('/tasks/')
            return HttpResponseRedirect('/set_reminder/one_time/'+
                                        task_id+
                                        '/')
        # конец 52


        task_full.when_to_reminder = dtt
        task_full.save()
        set_last_activity(user,request.path)
        return HttpResponseRedirect('/tasks/')
    else:

        # fixing bug #38
        # https://github.com/Ishayahu/MJCC-tasks/issues/38
        # минуты должны быть с 0 в начале, иначе <input type="time" value="11:7"> не отображается
        # должно быть <input type="time" value="11:07">
        minutes = str(datetime.datetime.now().minute)
        if len(minutes)==1:
            minutes = "0"+minutes
        # end fixing bug #38

        after_hour = str(datetime.datetime.now().hour+1)+":"+minutes
        today = str(datetime.datetime.now().day)+"/"+str(datetime.datetime.now().month)+"/"+str(datetime.datetime.now().year)
    set_last_activity(user,request.path)
    return render_to_response(languages[lang]+'set_reminder.html',
                              {'my_error':my_error, 'admin':admin,
                                               'method':method,
                               'today':today,'after_hour':after_hour},
                              RequestContext(request))

@login_required
def move_to_call(request,task_type,task_id):
    lang=select_language(request)
    if not acl(request,task_type,task_id):
        request.session['my_error'] = u'Нет права доступа к этой задаче!'
        return HttpResponseRedirect("/tasks/")
    user = request.user.username
    method = request.method
    data = 0
    time = 0
    try:
        task_full = task_types[task_type].objects.get(id = task_id)
    except:
        return HttpResponseRedirect('/tasks/')
    if request.method == 'POST':
        if 'datepicker' in request.POST:
            data = request.POST['datepicker']
        if 'time' in request.POST:
            time = request.POST['time']
        dtt = datetime.datetime(*map(int,([data.strip().split('/')[2],data.strip().split('/')[1],data.strip().split('/')[0]]+time.strip().split(':'))))
        task_full.when_to_reminder = dtt
        cat_call = Categories.objects.get(name = 'Звонки')
        task_full.category = cat_call
        task_full.save()
        set_last_activity(user,request.path)
        return HttpResponseRedirect('/tasks/')
    else:
        after_hour = str(datetime.datetime.now().hour+1)+":"+str(datetime.datetime.now().minute)
        today = str(datetime.datetime.now().day)+"/"+str(datetime.datetime.now().month)+"/"+str(datetime.datetime.now().year)
    set_last_activity(user,request.path)
    return render_to_response(languages[lang]+'set_reminder.html', {'method':method,'today':today,'after_hour':after_hour},RequestContext(request))

@login_required    
def register(request):
    lang=select_language(request)
    if request.method == 'POST':
        form = UserCreationFormMY(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            new_user = form.save()
            new_person = Person(
                fio = data['fio'],
                tel = data['tel'],
                mail = data['mail'],
                login = data['username']
            )
            new_person.save()
            return HttpResponseRedirect("/tasks/")
    else:
        form = l_forms[lang]['UserCreationFormMY']()
    return render_to_response(languages[lang]+"registration/register.html",{'form':form},RequestContext(request))
@login_required    
def profile(request):
    lang=select_language(request)
    user = request.user.username
    set_last_activity(user,request.path)
    return HttpResponseRedirect("/tasks/")
@login_required
def tasks(request):
    lang=select_language(request)
    def tasks_separation(tasks):
        """
        Деление задач на исполнителей для отображения исходящих задач
        """
        class group():
            def __init__(self,person,tasks):
                self.person = person
                self.tasks = tasks
        class state_task():
            def __init__(self,state,task):
                self.state = state
                self.task = task
        my_tasks=[]
        tmp_group=[]
        worker=tasks[0].worker
        now = datetime.datetime.now()
        for task in tasks:
            if task.worker != worker:
                my_tasks.append(group(worker,tmp_group))
                tmp_group=[]
                worker = task.worker
                state=-9
                if task.due_date < now:
                    state = -1
                elif task.due_date.date() == now.date():
                    state = 0
                else:
                    state = 1
                tmp_group.append(state_task(state,task))
            else:
                state=-9
                if task.due_date < now:
                    state = -1
                elif task.due_date.date() == now.date():
                    state = 0
                else:
                    state = 1
                tmp_group.append(state_task(state,task))
        my_tasks.append(group(worker,tmp_group))
        return my_tasks
    # получаем ошибку, если она установлена и сбрасываем её в запросах
    if request.session.get('my_error'):
        my_error = [request.session.get('my_error'),]
    else:
        my_error=[]
    # print my_error.encode('utf8')
    request.session['my_error'] = ''
    user = request.user.username
    # method = request.method
    # Если подтверждаются задачи с главной страницы
    if request.method == 'POST':
        for task_to_confirm_id in request.POST.getlist('task_to_confirm_id'):
            task_to_confirm = Task.objects.get(id=int(task_to_confirm_id))
            task_to_confirm.confirmed = True
            task_to_confirm.confirmed_date = datetime.datetime.now()
            task_to_confirm.save()
            send_email_alternative(u"Завершение задачи подтверждено: "+task_to_confirm.name,u"Описание задачи\<table cellpadding='5' border='1'\>\<tr\>\<td\>"+task_to_confirm.description+u"\</td\>\</tr\>\</table\>\n*Посмотреть задачу можно тут*:\nhttp://"+server_ip+"/task/one_time/"+str(task_to_confirm.id),[task_to_confirm.worker.mail,task_to_confirm.client.mail])
            request.session['my_error'] = u'Выполнение задач успешно подтверждено!'
        set_last_activity(user,request.path)
        return HttpResponseRedirect('/tasks/')
    # Если просто просматриваем список задач
    else:
        try:
            # Получаем объект пользователя, который открыл страницу
            worker = Person.objects.get(login=user)#.order_by("priority")
        # Если такого человека нет в базе, хз как это может быть:
        # Но если вдруг есть, то надо внести это в my_error и открыть страницу для этой ошибки
        # Эту же страницу не открывать, так как попадём в замкнутый круг. Вот этого-то ещё и нет
        except Person.DoesNotExist:
            # worker = 'Нет такого пользователя'
            my_error.append('Нет такого пользователя')
        #
        # получаем заявки ДЛЯ человека
        #
        # просроченные
        try:
            # отображаем только НЕ закрытые заявки, т.е. процент выполнения которых меньше 100
            # фильтр filter(start_date__lt=datetime.datetime.now()) удялет заявки, которые ещё не наступили
            # фильтр filter(when_to_reminder__lt=datetime.datetime.now()) удялет заявки, которые ещё не наступили
            tasks_overdue = Task.objects.filter(deleted = False).filter(worker=worker,percentage__lt=100).filter(due_date__lt=datetime.datetime.now()).filter(start_date__lt=datetime.datetime.now()).filter(when_to_reminder__lt=datetime.datetime.now())
        except:
            tasks_overdue = ''# если задач нет - вывести это в шаблон
        # на сегодня
        try:
            # отображаем только НЕ закрытые заявки, т.е. процент выполнения которых меньше 100
            # фильтр filter(start_date__lt=datetime.datetime.now()) удялет заявки, которые ещё не наступили
            # фильтр filter(when_to_reminder__lt=datetime.datetime.now()) удялет заявки, которые ещё не наступили
            tasks_for_today = Task.objects.filter(deleted = False).filter(worker=worker,percentage__lt=100).filter(due_date__year=datetime.datetime.now().year,due_date__month=datetime.datetime.now().month,due_date__day=datetime.datetime.now().day).filter(start_date__lt=datetime.datetime.now()).filter(when_to_reminder__lt=datetime.datetime.now())
        except:
            tasks_for_today = ''# если задач нет - вывести это в шаблон
        # на будущее
        try:
            # отображаем только НЕ закрытые заявки, т.е. процент выполнения которых меньше 100
            # фильтр filter(start_date__lt=datetime.datetime.now()) удялет заявки, которые ещё не наступили
            # фильтр filter(when_to_reminder__lt=datetime.datetime.now()) удялет заявки, которые ещё не наступили
            tasks_future = Task.objects.filter(deleted = False).filter(worker=worker,percentage__lt=100).filter(due_date__gt=datetime.datetime.now()).filter(start_date__lt=datetime.datetime.now()).filter(when_to_reminder__lt=datetime.datetime.now())
        except:
            tasks_future = ''# если задач нет - вывести это в шаблон

        # https://github.com/Ishayahu/MJCC-tasks/issues/63
        # срок исполнения которых меньше 3-х дней, для выделения
        # оповещение должно выдаваться только раз за сессию!
        # и раз за день
        was_nearest_remining = request.session.get('nearest_remining',False)
        today = str(datetime.datetime.now().date())
        last_nearest_remining_date = request.session.get(
            'nearest_remining_date','1900-01-01')
        if last_nearest_remining_date!=today:
            was_nearest_remining = False
        # print request.session.get('nearest_remining_date',False)
        nearest_count = 0
        for task in tasks_future:
            if task.due_date <= datetime.datetime.now() \
                    + datetime.timedelta(days=3):
                task.nearest = True
                if not was_nearest_remining:
                    request.session['nearest_remining'] = True
                    request.session['nearest_remining_date'] = today
                    nearest_count+=1
        #

        # получаем заявки ОТ человека
        #
        try:
            my_tasks = Task.objects.filter(deleted = False).filter(client=worker,percentage__lt=100).order_by('worker','due_date')
            # Теперь их надо разбить по тому, кому они адресованы и выделять цветом их просроченность/нет
            my_tasks = tasks_separation(my_tasks)
        except:
            # если задач нет - вывести это в шаблон
            my_tasks = ''# если задач нет - вывести это в шаблон
            my_error.append('От Вас нет задач')
        try:
            # получаем активные регулярные задачи
            # фильтр filter(start_date__lt=datetime.datetime.now()) удялет заявки, которые ещё не наступили
            # фильтр filter(when_to_reminder__lt=datetime.datetime.now()) удялет заявки, которые ещё не наступили
            regular_tasks = RegularTask.objects.filter(deleted = False).filter(worker=worker).filter(next_date__lt=datetime.datetime.now()).filter(when_to_reminder__lt=datetime.datetime.now())
        except:
            regular_tasks = ''# если задач нет - вывести это в шаблон
        
        # получаем кол-во заявок в этот раз и сравниваем с тем, что было для уведомления всплывающим окном или ещё какой фигней
        alert = False
        if request.session.get('tasks_number'):
            tasks_number_was = int(request.session.get('tasks_number'))
        else:
            tasks_number_was = 999
        tasks_number = sum(map(len,(tasks_overdue,tasks_for_today,tasks_future,regular_tasks)))
        if tasks_number_was < tasks_number:
            alert = True
        request.session['tasks_number'] = tasks_number
        # только для админов
        admin = False
        if user in admins:
            admin = True
            # получаем Список всех заявок для админов
            try:
                # отображаем только НЕ закрытые заявки, т.е. процент выполнения которых меньше 100
                all_tasks = Task.objects.filter(deleted = False).filter(percentage__lt=100).exclude(client=worker).exclude(worker=worker)#.order_by("priority")
            except:
                all_tasks = ''# если задач нет - вывести это в шаблон
            # получаем заявки ДЛЯ ПОДТВЕРЖДЕНИЯ ЗАКРЫТИЯ если человек - админ
            try:
                # отображаем только НЕ закрытые заявки, т.е. процент выполнения которых меньше 100
                tasks_to_confirm = Task.objects.filter(deleted = False).filter(percentage__exact=100).filter(confirmed__exact=False)
            except:
                tasks_to_confirm = ''# если задач нет - вывести это в шаблон
                my_error.append('Нет неподтверждённых заявок')
    set_last_activity(user,request.path)
    return render_to_response(languages[lang]+'tasks.html',
        {'my_error':my_error,'user':user,'worker':worker,
        'tasks_overdue':tasks_overdue,
        'tasks_for_today':tasks_for_today,
        'tasks_future':tasks_future,'my_tasks':my_tasks,
        'tasks_to_confirm':tasks_to_confirm,'all_tasks':all_tasks,
        'alert':alert,'admin':admin,'regular_tasks':regular_tasks,
         'nearest_count':nearest_count,
        },RequestContext(request))
    # set_last_activity(user,request.path)
    # return render_to_response(languages[lang]+'tasks.html',{'my_error':my_error,'user':user,'worker':worker,'tasks_overdue':tasks_overdue,'tasks_for_today':tasks_for_today,'tasks_future':tasks_future,'my_tasks':my_tasks,'alert':alert,'regular_tasks':regular_tasks},RequestContext(request))
@login_required
def task(request,task_type,task_id):
    lang=select_language(request)
    if not acl(request,task_type,task_id):
        request.session['my_error'] = u'Нет права доступа к этой задаче!'
        return HttpResponseRedirect("/tasks/")
    user = request.user.username
    admin = False
    if user in admins:
	admin = True
    try:
        fio = Person.objects.get(login=user)
    except Person.DoesNotExist:
        fio = FioError()
    try:
        # есть ли здача или она уже удалена?
        task_full = task_types[task_type].objects.get(id=task_id)
        try:
            if task_type == 'one_time':
                tmp_notes = Note.objects.filter(for_task=task_full).order_by('-timestamp')
            if task_type == 'regular':
                tmp_notes = Note.objects.filter(for_regular_task=task_full).order_by('-timestamp')
        except Note.DoesNotExist:
            tmp_notes = ('Нет подходящих заметок',)
        notes=[]
        for note in tmp_notes:
            notes.append(note_with_indent(note,0))
            build_note_tree(note,notes,1)
        # подготовка к выводу
        task_full.html_description = htmlize(task_full.description)
        if task_type=='regular':
            task_full.russian_period = crontab_to_russian(task_full.period)
        method = request.method
        if request.method == 'POST':
            form = NoteToTicketAddForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                if request.POST.get('add_comment'):
                    note = Note(
                        timestamp = datetime.datetime.now(),
                        note = data['note'],
                        author = fio
                    )
                    note.save()
                    if task_type == 'one_time':
                        note.for_task.add(task_full)
                    if task_type == 'regular':
                        note.for_regular_task.add(task_full)
                    note.save()
                    mails = [person.mail for person in data['workers']]
                    acl_list = task_full.acl.split(';')
                    for person in data['workers']:
                        if person.login not in acl_list:
                            acl_list.append(person.login)
                    task_full.acl = ';'.join(acl_list)
                    task_full.save()
                    send_email_alternative(u"Новый комментарий к задаче: "+task_full.name,u"*Комментарий*\<table cellpadding='5' border='1'\>\<tr\>\<td\>"+note.note+u"\</td\>\</tr\>\</table\>\n\n*Описание задачи*\<table cellpadding='5' border='1'\>\<tr\>\<td\>"+task_full.description+u"\</td\>\</tr\>\</table\>\n*Посмотреть задачу можно тут*:\nhttp://"+server_ip+"/task/"+task_addr[task_type]+"/"+str(task_full.id),mails,fio)
                    set_last_activity(user,request.path)
                    return HttpResponseRedirect(request.get_full_path())
                elif request.POST.get('answer_to_comment'):
                    parent_note = Note.objects.get(id=int(request.POST.get('to_note')))
                    note = Note(
                        timestamp = datetime.datetime.now(),
                        note = request.POST.get('answer'),
                        author = fio,
                    )
                    note.save()
                    note.parent_note.add(parent_note)
                    note.save()
                    mails = (parent_note.author.mail if parent_note.author.mail else '' ,)
                    send_email_alternative(u"Ответ на ваш комментарий к задаче: "+task_full.name,u"\<table cellpadding='5' border='1'\>\<tr\>\<td\>Ваш комментарий\</td\>\<td\>"+parent_note.note+u"\</td\>\</tr\>\<tr\>\<td\>Ответ\</td\>\<td\>\<table cellpadding='20'\>\<tr\>\<td\> "+note.note+u"\</td\>\</tr\>\</table\>\</td\>\</tr\>\</table\>\n\n*Описание задачи*:\<table border='1'\>\<tr\>\<td\>"+task_full.description+u"\</td\>\</tr\>\</table\>\n*Посмотреть задачу можно тут*:\nhttp://"+server_ip+"/task/"+task_addr[task_type]+"/"+str(task_full.id),mails,fio)
                    set_last_activity(user,request.path)
                    return HttpResponseRedirect(request.get_full_path())
                elif request.POST.get('del_comment'):
                    note_to_del_id=request.POST.get('num')
                    note_to_del = Note.objects.get(id=note_to_del_id)
                    # Если есть дочерние комментарии - прикрепить к родительской заметке или к задаче
                    children_note=''
                    parent_note=''
                    try:
                        children_note = note_to_del.children_note.get()
                    except Note.DoesNotExist:
                        pass
                    try:
                        parent_note= note_to_del.parent_note.get()
                    except Note.DoesNotExist:
                        pass
                    # Если есть дочерний комментарий - работаем
                    if children_note:
                        # Если есть родительский комментарий - прикрепляем к нему
                        if parent_note:
                            parent_note.children_note.add(children_note)
                            parent_note.save()
                        # Если родительского комментария нет - прикрепляем к задаче
                        else:
                            if task_type == 'one_time':
                                children_note.for_task.add(task_full)
                            if task_type == 'regular':
                                children_note.for_regular_task.add(task_full)
                            children_note.save()                    
                    note_to_del.delete()
                    set_last_activity(user,request.path)
                    return HttpResponseRedirect(request.get_full_path())
                elif request.POST.get('edit_comment'):
                    note_to_edit_id = request.POST.get('num')
                    for note in notes:
                        if note.id != int(note_to_edit_id):
                            note.note = htmlize(note.note)
                    set_last_activity(user,request.path)
                    return render_to_response(languages[lang]+'task.html',{'user':user,'fio':fio,'task':task_full,'notes':notes, 'form':form,'note_to_edit_id':int(note_to_edit_id),'task_type':task_type},RequestContext(request))
                elif request.POST.get('save_edited_comment'):
                    note_to_edit_id = request.POST.get('num')
                    note_to_edit = Note.objects.get(id=note_to_edit_id)
                    old_comment = note_to_edit.note
                    note_to_edit.note = request.POST.get('text_note_to_edit')
                    note_to_edit.save()
                    send_email_alternative(u"Отредактирован комментарий к задаче: "+task_full.name,u"\<table cellpadding='5' border='1'\>\<tr\>\<td\>Старый комментарий\</td\>\<td\>"+old_comment+u"\</td\>\</tr\>\<tr\>\<td\>Новый комментарий\</td\>\<td\>"+note_to_edit.note+u"\</td\>\</tr\>\</table\>\n\n*Посмотреть задачу можно тут*:\nhttp://"+server_ip+"/task/"+task_addr[task_type]+"/"+str(task_full.id),[task_full.worker.mail,task_full.client.mail],fio)
                    set_last_activity(user,request.path)
                    return HttpResponseRedirect(request.get_full_path())

        else:
            form = l_forms[lang]['NoteToTicketAddForm'](defaults = (task_full.worker.fio, task_full.client.fio),exclude = (fio,))
            for note in notes:
                note.note = htmlize(note.note)
            files=task_full.file.all()
            # files[0].file.url
            set_last_activity(user,request.path)
            return render_to_response(languages[lang]+'task.html',
                                      {'files':files,'user':user,
                                       'worker':fio,'task':task_full,
                                       'notes':notes, 'form':form,
                                       'task_type':task_type,
                                       'admin':admin},
                                      RequestContext(request))
            # return render_to_response(languages[lang]+'task.html',{'files':files,'user':user,'fio':fio,'task':task_full,'notes':notes, 'form':form,'task_type':task_type,'admin':admin},RequestContext(request))
    # если задачи нет - возвращаем к списку с ошибкой
    except Task.DoesNotExist:
        # print 'here'
        # return tasks(request, my_error=u'Такой задачи нет. Возможно она была уже удалена')
        request.session['my_error'] = u'Такой задачи нет. Возможно она была уже удалена'
        return HttpResponseRedirect('/tasks/')
    # никогда не выполняется. нужно только для проформы
    return HttpResponseRedirect("/tasks/")

@login_required
def close_task(request,task_to_close_id):
    lang=select_language(request)
    if not acl(request,'one_time',task_to_close_id):
        request.session['my_error'] = u'Нет права доступа к этой задаче!'
        return HttpResponseRedirect("/tasks/")

    task_to_close = Task.objects.get(id=task_to_close_id)
    method = request.method
    user = request.user.username
    try:
        fio = Person.objects.get(login=user)
    except Person.DoesNotExist:
        fio = FioError()
    try:
        tmp_notes = Note.objects.filter(for_task=task_to_close).order_by('-timestamp')
    except Note.DoesNotExist:
        tmp_notes = ('Нет подходящих заметок',)
    notes=[]
    for note in tmp_notes:
	notes.append(note_with_indent(note,0))
	build_note_tree(note,notes,1)
    # если закрываем заявку
    if request.method == 'POST':
        form = TicketClosingForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            task_to_close.pbw=data['pbw']
            task_to_close.done_date=data['done_date']
            task_to_close.percentage=100
            task_to_close.save()
            request.session['my_error'] = u'Задача благополучно закрыта! Ещё одну? ;)'
            send_email_alternative(u"Задача закрыта и требует подтверждения: "+task_to_close.name,u"*Описание задачи*\<table cellpadding='5' border='1'\>\<tr\>\<td\>"+task_to_close.description+u"\</td\>\</tr\>\</table\>\n\n*Посмотреть задачу можно тут*:\nhttp://"+server_ip+"/task/one_time/"+str(task_to_close.id),[task_to_close.client.mail,]+admins_mail,fio)
            return HttpResponseRedirect('/tasks/')
    # если хотим закрыть заявку
    else: 
        # проверяем, есть ли незакрытые дочерние заявки. Если есть - выводим их список на новой странице
        try:
            not_closed_children_tasks = Task.objects.filter(deleted = False).filter(parent_task = task_to_close).exclude(percentage__exact=100)
        except:
            not_closed_children_tasks = ''
        if not_closed_children_tasks:
            set_last_activity(user,request.path)
            return render_to_response(languages[lang]+'not_closed_children.html', {'user':user,'fio':fio,'task_to_close':task_to_close,'not_closed_children_tasks':not_closed_children_tasks},RequestContext(request))
        form = l_forms[lang]['TicketClosingForm']({'done_date' : datetime.datetime.now(),})
    task_to_close.description = htmlize(task_to_close.description)
    for note in notes:
        note.note = htmlize(note.note)
    set_last_activity(user,request.path)
    return render_to_response(languages[lang]+'close_ticket.html', {'user':user,'fio':fio,'form':form, 'task':task_to_close,'notes':notes},RequestContext(request))
@login_required
def unclose_task(request,task_to_unclose_id):
    lang=select_language(request)
    if not acl(request,'one_time',task_to_unclose_id):
        request.session['my_error'] = u'Нет права доступа к этой задаче!'
        return HttpResponseRedirect("/tasks/")

    try:
        task_to_unclose = Task.objects.get(id=task_to_unclose_id)
    except:
        task_to_unclose = ''
    method = request.method
    user = request.user.username
    try:
        fio = Person.objects.get(login=user)
    except Person.DoesNotExist:
        fio = FioError()
    task_to_unclose.percentage = 50
    task_to_unclose.save()
    send_email_alternative(u"Задача открыта заново: "+task_to_unclose.name,u"*Описание задачи*\<table cellpadding='5' border='1'\>\<tr\>\<td\>"+task_to_unclose.description+u"\</td\>\</tr\>\</table\>\n\n*Посмотреть задачу можно тут*:\nhttp://"+server_ip+"/task/one_time/"+str(task_to_unclose.id),[task_to_unclose.client.mail,task_to_unclose.worker.mail]+admins_mail,fio)
    set_last_activity(user,request.path)
    return HttpResponseRedirect('/tasks/')
@login_required
def to(request, to_who):
    lang=select_language(request)
    user = request.user.username
    method = request.method
    if user in admins:
        admin = True
    try:
        fio = Person.objects.get(login=user)
    except Person.DoesNotExist:
        fio = FioError()
    if request.session.get('my_error'):
        my_error = [request.session.get('my_error'),]
    else:
        my_error=[]
    request.session['my_error'] = ''
    if user not in admins:
        return HttpResponseRedirect("/tasks/")
    tasks = list()
    for task_type in task_types:
        if task_type != 'regular':
            for task in task_types[task_type].objects.filter(deleted = False).filter(percentage__lt=100).filter(start_date__lt=datetime.datetime.now()).filter(when_to_reminder__lt=datetime.datetime.now()).filter(category=Categories.objects.get(name=to_who).id):
                task.task_type=task_type
                tasks.append(task)
        else:
            for task in task_types[task_type].objects.filter(deleted = False).filter(next_date__lt=datetime.datetime.now()).filter(when_to_reminder__lt=datetime.datetime.now()).filter(category=Categories.objects.get(name=to_who).id):
                task.task_type=task_type
                tasks.append(task)
    tasks_to = list(chain(tasks))
    notes={}
    for task in tasks_to:
        task.description = htmlize(task.description)
        try:
            notes[task.id] = Note.objects.filter(for_task=task).order_by('-timestamp')
        except Note.DoesNotExist:
            notes = ('Нет подходящих заметок',)
    for note_to_id in notes:
        for note in notes[note_to_id]:
            note.note = htmlize(note.note)
    set_last_activity(user,request.path)
    return render_to_response(languages[lang]+'tasks_to.html',
                              {'worker':fio,'tasks':tasks_to,
                               'notes':notes,'to_who':to_who,
                               'method':method, 'admin':admin},
                              RequestContext(request))
@login_required
def confirm_task(request,task_to_confirm_id):
    lang=select_language(request)
    user = request.user.username
    if user not in admins:
        request.session['my_error'] = u'Нет права подтвердить закрытие задачи!'
        return HttpResponseRedirect("/tasks/")

    task_to_confirm = Task.objects.get(id=task_to_confirm_id)
    method = request.method
    try:
        fio = Person.objects.get(login=user)
    except Person.DoesNotExist:
        fio = FioError()
    if request.method == 'POST':
        form = TicketConfirmingForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            if request.POST.get('confirm_task'):
                task_to_confirm.confirmed=data['confirmed']
                task_to_confirm.confirmed_date=data['confirmed_date']
                task_to_confirm.save()
                request.session['my_error'] = u'Выполнение задачи успешно подтверждено!'
                send_email_alternative(u"Завершение задачи подтверждено: "+task_to_confirm.name,u"*Описание задачи*\<table cellpadding='5' border='1'\>\<tr\>\<td\>"+task_to_confirm.description+u"\</td\>\</tr\>\</table\>\n\n*Посмотреть задачу можно тут*:\nhttp://"+server_ip+"/task/one_time/"+str(task_to_confirm.id),[task_to_confirm.worker.mail,task_to_confirm.client.mail],fio)
                set_last_activity(user,request.path)
                return HttpResponseRedirect('/tasks/')
            elif request.POST.get('del_comment'):
                note_to_del_id=request.POST.get('num')
                note_to_del = Note.objects.get(id=note_to_del_id)
                note_to_del.delete()
                set_last_activity(user,request.path)
                return HttpResponseRedirect(request.get_full_path())
    else:
        try:
            notes = Note.objects.filter(for_task=task_to_confirm).order_by('-timestamp')
        except Note.DoesNotExist:
            notes = ('Нет подходящих заметок',)
        form = l_forms[lang]['TicketConfirmingForm']({'confirmed':True, 'confirmed_date':datetime.datetime.now()})
        for note in notes:
            note.note = htmlize(note.note)
    task_to_confirm.description = htmlize(task_to_confirm.description)
    set_last_activity(user,request.path)
    return render_to_response(languages[lang]+'confirm_ticket.html', {'form':form,'task':task_to_confirm,'notes':notes,'method':method,'fio':fio},RequestContext(request))    
@login_required
def edit_task(request,task_to_edit_id):
    lang=select_language(request)
    if not acl(request,'one_time',task_to_edit_id):
        request.session['my_error'] = u'Нет права доступа к этой задаче!'
        return HttpResponseRedirect("/tasks/")

    task_to_edit = Task.objects.get(id=task_to_edit_id)
    method = request.method
    
    user = request.user.username
    if user in admins:
        admin = True
    try:
        fio = Person.objects.get(login=user)
    except Person.DoesNotExist:
        fio = FioError()
    if request.method == 'POST':
        form = l_forms[lang]['TicketEditForm'](request.POST,request.FILES)
        # если меняется исполнитель - чтобы оповестить
        old_worker = task_to_edit.worker
        old_pbu = task_to_edit.pbu
        old_client = task_to_edit.client
        old_start_date = task_to_edit.start_date
        old_category = task_to_edit.category
        old_due_date = task_to_edit.due_date
        old_name = task_to_edit.name

        # # старый варинат
        if form.is_valid():
            # проверка - есть ли файл надо добавить
            def save_file(files):
                instanse = File(file=files['file'],
                                timestamp=datetime.datetime.now(),
                                file_name = 'file_name',
                                description = 'TEST',)
                instanse.save()
                return instanse
            if request.FILES:
                task_to_edit.file.add(save_file(request.FILES))
                task_to_edit.save()
            # raise TabError
            data = form.cleaned_data
            task_to_edit.name=data['name']
            task_to_edit.pbu=data['pbus']
            task_to_edit.description=data['description']
            task_to_edit.client=data['clients']
            task_to_edit.priority=data['priority']
            task_to_edit.category=data['category'] 
            task_to_edit.start_date=data['start_date']
            task_to_edit.due_date=data['due_date']
            task_to_edit.worker=data['workers']
            task_to_edit.percentage=data['percentage']
            task_to_edit.when_to_reminder=data['when_to_reminder']
            # task_to_edit.file_id = file.id
            task_to_edit.save()
            if task_to_edit.name != old_name:
                send_email_alternative(u"Изменёно название задачи: "+old_name,
                           u"\<table cellpadding='5' border='1'\>\<tr\>\<td\>Прежнее название\</td\>\<td\>"+old_name+u"\</td\>\</tr\>\<tr\>\<td\>Новое название\</td\>\<td\>"+task_to_edit.name+u"\</td\>\</tr\>\</table\>\n\n*Описание задачи*\<table cellpadding='5' border='1'\>\<tr\>\<td\>"+task_to_edit.description+u"\</td\>\</tr\>\</table\>\n\n*Посмотреть задачу можно тут*:\nhttp://"+server_ip+"/task/one_time/"+str(task_to_edit.id),
                           [task_to_edit.worker.mail,task_to_edit.client.mail]+admins_mail,
                           fio
                           )
            if task_to_edit.worker != old_worker:
                # добавление нового исполнителя в acl
                if task_to_edit.worker.login not in task_to_edit.acl:
                    task_to_edit.acl=task_to_edit.acl+";"+task_to_edit.worker.login
                    task_to_edit.save()
                send_email_alternative(u"Изменён исполнитель задачи: "+task_to_edit.name,
                           u"\<table cellpadding='5' border='1'\>\<tr\>\<td\>Прежний исполнитель\</td\>\<td\>"+old_worker.fio+u"\</td\>\</tr\>\<tr\>\<td\>Новый исполнитель\</td\>\<td\>"+task_to_edit.worker.fio+u"\</td\>\</tr\>\</table\>\n\n*Описание задачи*\<table cellpadding='5' border='1'\>\<tr\>\<td\>"+task_to_edit.description+u"\</td\>\</tr\>\</table\>\n\n*Посмотреть задачу можно тут*:\nhttp://"+server_ip+"/task/one_time/"+str(task_to_edit.id),
                           [task_to_edit.worker.mail,task_to_edit.client.mail,old_worker.mail]+admins_mail,
                           fio
                           )
            if task_to_edit.pbu != old_pbu:
                send_email_alternative(u"Изменёно описание проблемы со слов пользователя для задачи: "+task_to_edit.name,
                           u"\<table cellpadding='5' border='1'\>\<tr\>\<td\>Прежная проблема\</td\>\<td\>"+old_pbu.name+u"\</td\>\</tr\>\<tr\>\<td\>Новая проблема\</td\>\<td\>"+task_to_edit.pbu.name+u"\</td\>\</tr\>\</table\>\n\n*Описание задачи*\<table cellpadding='5' border='1'\>\<tr\>\<td\>"+task_to_edit.description+u"\</td\>\</tr\>\</table\>\n\n*Посмотреть задачу можно тут*:\nhttp://"+server_ip+"/task/one_time/"+str(task_to_edit.id),
                           [task_to_edit.worker.mail,task_to_edit.client.mail]+admins_mail,
                           fio
                           )
            if task_to_edit.client != old_client:
                # добавление нового заказчика в acl
                if task_to_edit.client.login not in task_to_edit.acl:
                    task_to_edit.acl=task_to_edit.acl+";"+task_to_edit.client.login
                    task_to_edit.save()
                send_email_alternative(u"Изменён заказчик задачи: "+task_to_edit.name,
                           u"\<table cellpadding='5' border='1'\>\<tr\>\<td\>Прежний заказчик\</td\>\<td\>"+old_client.fio+u"\</td\>\</tr\>\<tr\>\<td\>Новый заказчик\</td\>\<td\>"+task_to_edit.client.fio+u"\</td\>\</tr\>\</table\>\n\n*Описание задачи*\<table cellpadding='5' border='1'\>\<tr\>\<td\>"+task_to_edit.description+u"\</td\>\</tr\>\</table\>\n\n*Посмотреть задачу можно тут*:\nhttp://"+server_ip+"/task/one_time/"+str(task_to_edit.id),
                           [task_to_edit.worker.mail,task_to_edit.client.mail,old_client.mail]+admins_mail,
                           fio
                           )
            if task_to_edit.category != old_category:
                send_email_alternative(u"Изменёна категория задачи: "+task_to_edit.name,
                           u"\<table cellpadding='5' border='1'\>\<tr\>\<td\>Прежная категория\</td\>\<td\>"+old_category.name+u"\</td\>\</tr\>\<tr\>\<td\>Новая категория\</td\>\<td\>"+task_to_edit.category.name+u"\</td\>\</tr\>\</table\>\n\n*Описание задачи*\<table cellpadding='5' border='1'\>\<tr\>\<td\>"+task_to_edit.description+u"\</td\>\</tr\>\</table\>\n\n*Посмотреть задачу можно тут*:\nhttp://"+server_ip+"/task/one_time/"+str(task_to_edit.id),
                           [task_to_edit.worker.mail,task_to_edit.client.mail]+admins_mail,
                           fio
                           )
            if task_to_edit.due_date != old_due_date:
                send_email_alternative(u"Изменён срок выполонения задачи: "+task_to_edit.name,
                           u"\<table cellpadding='5' border='1'\>\<tr\>\<td\>Старый срок\</td\>\<td\>"+str(old_due_date)+u"\</td\>\</tr\>\<tr\>\<td\>Новый срок\</td\>\<td\>"+str(task_to_edit.due_date)+u"\</td\>\</tr\>\</table\>\n\n*Описание задачи*\<table cellpadding='5' border='1'\>\<tr\>\<td\>"+task_to_edit.description+u"\</td\>\</tr\>\</table\>\n\n*Посмотреть задачу можно тут*:\nhttp://"+server_ip+"/task/one_time/"+str(task_to_edit.id),
                           [task_to_edit.worker.mail,task_to_edit.client.mail]+admins_mail,
                           fio
                           )
            if task_to_edit.start_date != old_start_date:
                send_email_alternative(u"Изменена дата начала задачи: "+task_to_edit.name,
                           u"\<table cellpadding='5' border='1'\>\<tr\>\<td\>Прежняя дата начала\</td\>\<td\>"+str(old_start_date)+u"\</td\>\</tr\>\<tr\>\<td\>Новая дата начала\</td\>\<td\>"+str(task_to_edit.start_date)+u"\</td\>\</tr\>\</table\>\n\n*Описание задачи*\<table cellpadding='5' border='1'\>\<tr\>\<td\>"+task_to_edit.description+u"\</td\>\</tr\>\</table\>\n\n*Посмотреть задачу можно тут*:\nhttp://"+server_ip+"/task/one_time/"+str(task_to_edit.id),
                           [task_to_edit.worker.mail,task_to_edit.client.mail]+admins_mail,
                           fio
                           )
            set_last_activity(user,request.path)
            return HttpResponseRedirect('/tasks/')
    else:
        form = l_forms[lang]['TicketEditForm']({'name' : task_to_edit.name,
            'pbus' : task_to_edit.pbu,
            'description' : task_to_edit.description,
            'clients' : task_to_edit.client,
            'priority' : task_to_edit.priority,
            'category' : task_to_edit.category,
            'start_date' : task_to_edit.start_date,
            'when_to_reminder' : task_to_edit.when_to_reminder,
            'due_date' : task_to_edit.due_date,
            'workers' : task_to_edit.worker,
            'percentage' : task_to_edit.percentage,
            # 'file':task_to_edit.file,
        })
        # Creating a form to change an existing task.
        # form = TaskEditForm(instance=task_to_edit)
    set_last_activity(user,request.path)
    return render_to_response(languages[lang]+'new_ticket.html',
                              {'worker':fio,'form':form,
                               'admin':admin,
                               'method':method},
    RequestContext(request))
@login_required
def delete_task(request,task_type,task_to_delete_id):
    lang=select_language(request)
    user = request.user.username
    task_to_delete = task_types[task_type].objects.get(id=task_to_delete_id)
    task_to_delete.deleted = True
    task_to_delete.save()
    set_last_activity(user,request.path)
    return HttpResponseRedirect('/tasks/')
@login_required
def undelete_task(request,task_type,task_id):
    lang=select_language(request)
    task = task_types[task_type].objects.get(id=task_id)
    task.deleted = False
    task.save()
    set_last_activity(user,request.path)
    return HttpResponseRedirect('/tasks/')    
@login_required
def completle_delete_task(request,task_type,task_to_delete_id):
    lang=select_language(request)
    user = request.user.username
    if user not in admins:
        return HttpResponseRedirect("/tasks/")      
    try:
        task = task_types[task_type].objects.get(id=task_to_delete_id)
    except Task.DoesNotExist, RegularTask.DoesNotExist:
        return HttpResponseRedirect('/tasks/')
    try:
        tmp_notes = Note.objects.filter(for_task=task).order_by('-timestamp')
        notes=[]
	for note in tmp_notes:
	    notes.append(note)
	    get_all_notes(note,notes)
	for note in notes:
	    note.delete()
    except Note.DoesNotExist:
        pass
    task.delete()
    set_last_activity(user,request.path)
    return HttpResponseRedirect('/deleted_tasks/')
def completle_delete_all(request):
    lang=select_language(request)
    user = request.user.username
    if user not in admins:
        return HttpResponseRedirect("/tasks/")
    try:
        tasks = list()
        for task_type in task_types:
            for task in task_types[task_type].objects.filter(deleted = True):
                task.task_type=task_type
                tasks.append(task)
        tasks = list(chain(tasks))
    except:
        pass
    for task in tasks:
	try:
	    tmp_notes = Note.objects.filter(for_task=task).order_by('-timestamp')
	    notes=[]
	    for note in tmp_notes:
		notes.append(note)
		get_all_notes(note,notes)
	    for note in notes:
		note.delete()
	except Note.DoesNotExist:
	    pass
	task.delete()
    set_last_activity(user,request.path)
    return HttpResponseRedirect('/tasks/')  
@login_required
def deleted_tasks(request):
    lang=select_language(request)
    user = request.user.username
    if user not in admins:
        return HttpResponseRedirect("/tasks/")
    try:
        tasks = list()
        for task_type in task_types:
            for task in task_types[task_type].objects.filter(deleted = True):
                task.task_type=task_type
                tasks.append(task)
        tasks = list(chain(tasks))
    except:
        task = ('Нет таких задач',)
    set_last_activity(user,request.path)
    return render_to_response(languages[lang]+'deleted_tasks.html', {'tasks':tasks,},RequestContext(request))

@login_required
def all_tasks(request,page_number):
    lang=select_language(request)
    def find_parent_task(note,task_type):
        """
        Поиск родительской заявки для примечания
        """
        try:
            if note.parent_note:
                return find_parent_task(note.parent_note.get(),task_type)
        except Note.DoesNotExist:
            if task_type=='one_time':
                return Task.objects.filter(note = note)
            else:
                return RegularTask.objects.filter(note = note)
    user = request.user.username

    # admin = False
    # enhancement #31
    # page_number=-1 показываем все
    try:
        page_number = int(page_number)
    except:
        page_number = -1
    if user in admins:
        admin = True
    else:
        admin = False
        page_number = 0
    # end #31

    try:
        fio = Person.objects.get(login=user)
    except Person.DoesNotExist:
        fio = FioError()
    not_finded = False
    finded_tasks = False
    method = request.method
    if request.method == 'POST':
        form = TicketSearchForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            # какая-то фигня - поиск должен не зависеть от регистра. Если ищем ascii - работает, если кирилицу - нет(

            try:
                finded_tasks_names = Task.objects.filter(name__icontains = data['name'])
                finded_tasks_desc = Task.objects.filter(description__icontains = data['name'])
                finded_rtasks_names = RegularTask.objects.filter(name__icontains = data['name'])
                finded_rtasks_desc = RegularTask.objects.filter(description__icontains = data['name'])
                notes = Note.objects.filter(note__icontains = data['name'])
                finded_tasks_notes=[]
                finded_rtasks_notes=[]
                for note in notes:
                    finded_tasks_notes = find_parent_task(note = note,task_type='one_time')
                    finded_rtasks_notes = find_parent_task(note = note,task_type='regular')
                finded_tasks = list(set(chain(finded_tasks_names, finded_tasks_desc, finded_rtasks_names,finded_rtasks_desc,finded_tasks_notes,finded_rtasks_notes)))
                if not finded_tasks:
                    not_finded = True
            except:
                print 'exception'
                not_finded = True
            set_last_activity(user,request.path)
            return render_to_response(languages[lang]+'all_tasks.html', {'not_finded':not_finded,'finded_tasks':finded_tasks,'form':form, 'method':method},RequestContext(request))
    else:
        form = l_forms[lang]['TicketSearchForm']()
        if request.session.get('my_error'):
            my_error = [request.session.get('my_error'),]
        else:
            my_error=[]
        request.session['my_error'] = ''

        # enhancement #31
        # Для изменения количества выводимых элементов будем
        # хранить их в словаре
        result = dict()
        # end #31

        try:
            # отображаем все НЕ закрытые заявки, т.е. процент выполнения которых меньше 100
            result['tasks'] = Task.objects.filter(deleted =
                                                  False).filter(percentage__lt=100)
        except:
            result['tasks'] = ''# если задач нет - вывести это в
            # шаблон
        try:
            # отображаем все повторяющиеся задачи
            result['regular_tasks'] = RegularTask.objects.filter(
                deleted = False)
        except:
            result['regular_tasks'] = ''# если задач нет - вывести
            # это в шаблон
        try:
            # отображаем все закрытые заявки не подтверждённые
            result['closed_tasks'] = Task.objects.filter(deleted =
                                                         False).filter(percentage__exact=100).filter(confirmed__exact=False)
        except:
            result['closed_tasks'] = ''# если задач нет - вывести
            # это в шаблон
            # my_error.append('Для Вас нет задач')
        try:
            # отображаем все подтверждённые заявки
            result['confirmed_tasks'] = Task.objects.filter(deleted = False).filter(confirmed__exact=True)
        except:
            result['confirmed_tasks'] = ''# если задач нет -
            # вывести это в шаблон

    # enhancement #31
    # https://github.com/Ishayahu/MJCC-tasks/issues/31
    tasks_per_page = 50
    total_tasks_count = 0
    for k,v in result.items():
        total_tasks_count += len(v)
    max_page_number = total_tasks_count / tasks_per_page
    if page_number>=0:
        start = page_number*tasks_per_page
        end = (page_number+1)*tasks_per_page
        # порядок: задачи, регулярные, закрытые, подтверждённые
        for x in ('tasks', 'regular_tasks', 'closed_tasks',
                  'confirmed_tasks'):
            len_x = len(result[x]) # так как меням похожу
            # print x[0],start,end
            result[x] = result[x][start:end]
            start -= len_x
            end -= len_x
            if start<0:
                start = 0
            if end<0:
                end = 0
                # print len(x)
    # end #31

    set_last_activity(user,request.path)
    return render_to_response(languages[lang]+'all_tasks.html',
                              {'my_error':my_error,'tasks':result[
                                  'tasks'],
                               'closed_tasks':result['closed_tasks'],
                               'confirmed_tasks':result[
                                   'confirmed_tasks'],
                               'regular_tasks':result[
                                   'regular_tasks'],
                               'form':form, 'method':method,
                               'admin':admin,'worker':fio,
                               'page_number':page_number,
                               'max_page_number':max_page_number,},
                              RequestContext(request))
@login_required
def add_children_task(request,parent_task_type,parent_task_id):
    lang=select_language(request)
    method = request.method
    user = request.user.username
    try:
        # находим родительскую задачу
        parent_task = task_types[parent_task_type].objects.get(id=parent_task_id)
    except:
        my_error=request.session.get('my_error')# если задач нет - вывести это в шаблон
        my_error.append('Не найдена родительская задача?!')
        return HttpResponseRedirect('/tasks/')
    if request.method == 'POST':
        form = NewTicketForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            t=Task(name=data['name'], 
                pbu=data['pbus'], 
                description=data['description'], 
                client=data['clients'], 
                priority=data['priority'], 
                category=data['category'], 
                start_date=data['start_date'],
                when_to_reminder = data['start_date'],
                due_date=data['due_date'], 
                worker=data['workers'],
                percentage=data['percentage'],
                acl = data['clients'].login+';'+data['workers'].login)
            t.save()
            if parent_task_type =='one_time':
                t.parent_task.add(parent_task)
            if parent_task_type =='regular':
                t.parent_regular_task.add(parent_task)
            t.save()
            # отправляем уведомление исполнителю по мылу
            send_email_alternative(u"Новая подзадача: '"+t.name+u"' для задачи '"+parent_task.name+u"'",
                       u"*Описание*\<table border='1' cellpadding='5'\>\<tr\>\<td\>"+t.description+u"\</td\>\</tr\>\</table\>\n\n*Посмотреть подзадачу можно тут*:\nhttp://"+server_ip+"/task/one_time/"+str(t.id)+u"\n*Посмотреть задачу можно тут*:\nhttp://"+server_ip+"/task/"+parent_task_type+"/"+str(parent_task.id),
                       [data['workers'].mail,])
            set_last_activity(user,request.path)
            return HttpResponseRedirect('/tasks/')
    else:
        form = l_forms[lang]['NewTicketForm'] ({'percentage':0,'start_date':datetime.datetime.now(),'due_date':datetime.datetime.now(),'priority':parent_task.priority,'category':parent_task.category})
    set_last_activity(user,request.path)
    return render_to_response(languages[lang]+'new_ticket.html', {'form':form, 'method':method},RequestContext(request))

@login_required
def regular_task_done(request,task_id):
    lang=select_language(request)
    user = request.user.username
    method = request.method
    try:
        # находим задачу
        task = RegularTask.objects.get(id=task_id)
    except:
        # если задач нет - вывести это в шаблон
        my_error=request.session.get('my_error')
        my_error.append('Не найдена задача?!')
        return HttpResponseRedirect('/tasks/')
    task.next_date = generate_next_reminder(decronize(task.period),
                                            task.stop_date)
    task.when_to_reminder = task.next_date
    task.save()
    set_last_activity(user,request.path)
    return HttpResponseRedirect('/tasks/')

@login_required
def get_all_logged_in_users(request):
    lang=select_language(request)
    user = request.user.username
    if user in admins:
        last_activities=get_last_activities()
        return render_to_response(languages[lang]+'logged_in_user_list.html', {'last_activities':last_activities,},RequestContext(request))
