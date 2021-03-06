# -*- coding:utf-8 -*-
# coding=<utf8>


# TODO: сделать возможность изменения языков

__version__ = '0.2.3f1'


from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
import datetime
from todoes.models import Note, Resource, File, Person, Task, \
    ProblemByWorker, ProblemByUser, Categories, RegularTask, Activity,\
    Message, Message_Visit
from todoes.forms_rus import NewTicketForm_RUS,\
    NoteToTicketAddForm_RUS, UserCreationFormMY,\
    TicketClosingForm_RUS, TicketConfirmingForm_RUS,\
    TicketEditForm_RUS,TicketSearchForm_RUS, NewRegularTicketForm_RUS,\
    EditRegularTicketForm_RUS, File_and_NoteToTicketAddForm_RUS
from todoes.forms_eng import NewTicketForm_ENG,\
    NoteToTicketAddForm_ENG, UserCreationFormMY_ENG,\
    TicketClosingForm_ENG, TicketConfirmingForm_ENG,\
    TicketEditForm_ENG,TicketSearchForm_ENG, NewRegularTicketForm_ENG,\
    EditRegularTicketForm_ENG, File_and_NoteToTicketAddForm_ENG
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from itertools import chain

from djlib.cron_utils import decronize, crontab_to_russian,\
    generate_next_reminder
from djlib.auxiliary import get_info
from djlib.module_utils import add_module_menu
from djlib.text_utils import htmlize
from djlib.acl_utils import acl, for_admins, admins_only
from djlib.user_tracking import set_last_activity_model, \
    get_last_activities, get_user_per_date_activities
from djlib.mail_utils import send_email_alternative, send_email_html
from djlib.error_utils import FioError, ErrorMessage, \
    add_error, shows_errors
from utils import *
from djlib.multilanguage_utils import select_language,multilanguage,\
    register_lang, get_localized_name, get_localized_form #,register_app

from user_settings.settings import server_ip, admins, admins_mail
from user_settings.functions import get_full_option
try:
    from user_settings.settings import todoes_url_not_to_track as \
        url_not_to_track
except ImportError:
    url_not_to_track=('',)
try:
    from user_settings.settings import todoes_url_one_record as \
        url_one_record
except ImportError:
    url_one_record=('',)



from todoes.utils import build_note_tree, note_with_indent

task_types = {'one_time':Task,'regular':RegularTask}
task_addr = {'one_time':'one_time','regular':'regular'}

register_lang('ru','RUS')
register_lang('eng','ENG')
app='todoes'


# Делаем переводы
# from djlib.multilanguage_utils import select_language
languages={'ru':'RUS/',
            'eng':'ENG/'}
forms_RUS = {'NewTicketForm':NewTicketForm_RUS,
             'NoteToTicketAddForm':NoteToTicketAddForm_RUS,
             'UserCreationFormMY':UserCreationFormMY,
             'TicketClosingForm':TicketClosingForm_RUS,
             'TicketConfirmingForm':TicketConfirmingForm_RUS,
             'TicketEditForm':TicketEditForm_RUS,
             'TicketSearchForm':TicketSearchForm_RUS,
             'NewRegularTicketForm':NewRegularTicketForm_RUS,
             'EditRegularTicketForm':EditRegularTicketForm_RUS,
             'File_and_NoteToTicketAddForm':File_and_NoteToTicketAddForm_RUS}
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
    admin = False
    if user in admins:
        admin = True
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
            send_email_html(
                u"Новая задача: " + t.name,
                u"<b>Описание</b>:<table cellpadding='5' border='1'>"
                u"<tr><td>" + htmlize(t.description) +
                u"</tr></td></table>"
                u"<b>Посмотреть задачу можно тут</b>: " +
                htmlize("http://" + server_ip + "/task/one_time/"
                        + str(t.id)),
                [data['workers'].mail,
                 data['clients'].mail])
            set_last_activity(user,request.path)
            return HttpResponseRedirect('/tasks/')
    else:
        form =l_forms[lang]['NewTicketForm'](
            {'percentage':0,
             'start_date':datetime.datetime.now(),
             'due_date':datetime.datetime.now(),
             'priority':3})
    set_last_activity(user,request.path)
    return render_to_response(languages[lang]+'new_ticket.html',
                              {'form':form, 'method':method,
                               'admin':admin, 'worker':fio},
                              RequestContext(request))

@login_required
def new_regular_ticket(request):
    lang=select_language(request)
    user = request.user.username
    admin = False
    if user in admins:
        admin=True
    try:
        fio = Person.objects.get(login=user)
    except Person.DoesNotExist:
        fio = FioError()
    method = request.method
    if request.method == 'POST':
        form = l_forms[lang]['NewRegularTicketForm'](request.POST)
        # form = NewRegularTicketForm(request.POST)
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
            send_email_html(
                u"Новая повторяющаяся задача: " +  t.name,
                u"<b>Описание</b>:<table cellpadding='5' border='1'>"
                u"<tr><td>" + htmlize(t.description) +
                u"</tr></td></table><b>Посмотреть задачу можно тут"
                u"</b>: " + htmlize("http://"+server_ip+
                                   "/task/regular/"+str(t.id)),
                [data['workers'].mail,
                data['clients'].mail])
            set_last_activity(user,request.path)
            return HttpResponseRedirect('/tasks/')
    else:
        form =l_forms[lang]['NewRegularTicketForm'](
            {'start_date':datetime.datetime.now(),
             'due_date':datetime.datetime.now(),'priority':3})
    set_last_activity(user,request.path)
    return render_to_response(languages[lang]+'new_regular_task.html',
                              {'page_title': u'Новая повторяющаяся '
                                             u'задача',
                               'form':form, 'method':method,
                               'admin':admin, 'worker':fio},
                              RequestContext(request))
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
        form = l_forms[lang]['EditRegularTicketForm'](request.POST)
        # form = EditRegularTicketForm(request.POST)
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
    try:
        fio = Person.objects.get(login=user)
    except Person.DoesNotExist:
        fio = FioError()
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
        if task_type == 'one_time' and dtt>task_full.due_date:
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
        hours = str(datetime.datetime.now().hour+1)
        if len(minutes)==1:
            minutes = "0"+minutes
        if len(hours)==1:
            hours = "0"+hours
        # end fixing bug #38

        after_hour = hours+":"+minutes
        today = str(datetime.datetime.now().day)+"/"+str(datetime.datetime.now().month)+"/"+str(datetime.datetime.now().year)
    set_last_activity(user,request.path)
    return render_to_response(languages[lang]+'set_reminder.html',
                              {'my_error':my_error, 'admin':admin,
                                'worker':fio,'method':method,
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
@multilanguage
def register(request):
    lang=select_language(request)
    if request.method == 'POST':
        form = l_forms[lang]['UserCreationFormMY'](request.POST)
        # form = UserCreationFormMY(request.POST)
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
    # return render_to_response(languages[lang]+"register.html",
    #                           {'form':form},
    #                           RequestContext(request))
    return (True,
            ('register.html',
             {'UserCreationFormMY':{}},
              {'title': 'Регистрация нового пользователя',
               'form_template_name':'form'},
              request,
              app))
@login_required    
def profile(request):
    lang=select_language(request)
    user = request.user.username
    set_last_activity(user,request.path)
    return HttpResponseRedirect("/tasks/")

@login_required
@multilanguage
@shows_errors
@for_admins
@add_module_menu
def tasks(request):
    lang=select_language(request)
    def tasks_separation(tasks):
        """
        Деление задач на исполнителей для отображения исходящих задач
        """
        class group():
            def __init__(self,person):
            # def __init__(self,person,tasks):
                self.person = person
                self.tasks = []
                # self.tasks = tasks
                self.count_overdue = 0
                self.count_today = 0
                self.count_future = 0
                self.overdue = []
                self.future = []
                self.today = []

            def add_task(self,task):
                if task.state==-1:
                    self.overdue.append(task)
                elif task.state==0:
                    self.today.append(task)
                elif task.state==1:
                    self.future.append(task)

            def prepare(self):
                self.count_future = len(self.future)
                self.count_today = len(self.today)
                self.count_overdue = len(self.overdue)
                self.tasks = self.overdue + self.today + self.future
                self.overdue=[]
                self.future=[]
                self.today=[]

        class state_task():
            def __init__(self,state,task):
                self.state = state
                self.task = task
                # if int(task.id)==479:
                #     print self.task.request_due_date

        def get_state(task):
            """
            Для определения того, просроченная задача, сегодняшнаяя
            или в будущем
            """
            now = datetime.datetime.now()
            state=-9
            if task.due_date < now:
                state = -1
            elif task.due_date.date() == now.date():
                state = 0
            else:
                state = 1
            return state

        my_tasks = dict()
        for task in tasks:
            # пробуем, нет ли уже группы с этим исполнителем
            try:
                # если есть - то добавляем туда задачу
                my_tasks[task.worker].add_task(
                    state_task(get_state(task),task))
            except KeyError:
                # значит, ещё нет. создаём
                my_tasks[task.worker] = group(task.worker)
                my_tasks[task.worker].add_task(
                    state_task(get_state(task),task))
        # сортируем задачи по состоянию: просроченные, сегодня, \
        #                                на будущее
        for k,v in my_tasks.items():
            my_tasks[k].prepare()
        # делаем из задач список для отображения
        result = []
        for k,v in my_tasks.items():
            result.append(v)
        return result
    # получаем ошибку, если она установлена и сбрасываем её в запросах
    if request.session.get('my_error'):
        #TODO: учесть при переводе на multilanguage
        if type(request.session['my_error']) != list:
            my_error = [request.session.get('my_error'),]
        else:
            my_error = request.session.get('my_error')
    else:
        my_error=[]
    # print my_error.encode('utf8')
    request.session['my_error'] = ''
    user = request.user.username
    admin = False
    if user in admins:
        admin = True
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
        return False, HttpResponseRedirect('/tasks/')
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
        # для оповещения о новых заявках со ссылками на них
        tasks_id_list=[]
        rtasks_id_list=[]
        # получаем активные регулярные задачи
        try:
            # фильтр filter(start_date__lt=datetime.datetime.now()) удялет заявки, которые ещё не наступили
            # фильтр filter(when_to_reminder__lt=datetime.datetime.now()) удялет заявки, которые ещё не наступили
            regular_tasks = RegularTask.objects.filter(deleted = False).filter(worker=worker).filter(next_date__lt=datetime.datetime.now()).filter(when_to_reminder__lt=datetime.datetime.now())
        except:
            regular_tasks = ''# если задач нет - вывести это в шаблон

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


        # enhancement #47
        for task in list(set(chain(tasks_overdue,
                                   tasks_for_today,
                                   tasks_future))):
            tasks_id_list.append(task.id)
        for task in regular_tasks:
            rtasks_id_list.append(task.id)
        # end #47


        # https://github.com/Ishayahu/MJCC-tasks/issues/63
        # срок исполнения которых меньше 3-х дней, для выделения
        # оповещение должно выдаваться только раз за сессию!
        # и раз за день
        was_nearest_remining = request.session.get('nearest_remining',
                                                   False)
        today = str(datetime.datetime.now().date())
        last_nearest_remining_date = request.session.get(
            'nearest_remining_date', '1900-01-01')
        if last_nearest_remining_date != today:
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
            my_tasks = Task.objects.filter(deleted = False).\
                filter(client=worker,percentage__lt=100).\
                order_by('worker','due_date')
            # Теперь их надо разбить по тому, кому они адресованы и выделять цветом их просроченность/нет
            # my_tasks = tasks_separation(my_tasks)
        except:
            # если задач нет - вывести это в шаблон
            my_tasks = ''# если задач нет - вывести это в шаблон
            my_error.append('От Вас нет задач')
        # получаем регулярные заявки ОТ человека
        #
        try:
            my_regular_tasks = RegularTask.objects.filter(deleted =
                                            False).filter(
                client=worker,
                next_date__lt=datetime.datetime.now()).order_by(
                'worker')
            # Теперь их надо разбить по тому, кому они адресованы и выделять цветом их просроченность/нет
            # my_tasks = tasks_separation(my_tasks)
        except:
            # если задач нет - вывести это в шаблон
            my_regular_tasks = ''# если задач нет - вывести это в шаблон
            my_error.append('От Вас нет постоянных задач')

        # соединяем все исходящие задачи в один список и сортируем
        # его по исполнителю и по состоянию
        all_my_tasks = []

        class SimpleTask():
            def __init__(self,task,task_type):
                self.id = task.id
                self.description = task.description
                self.name = task.name
                self.worker = task.worker
                self.priority = task.priority
                self.category = task.category
                # fix #63
                try:
                    self.nearest = task.nearest
                except:
                    self.nearest = False
                # end fix #63
                # fix #53
                # if int(task.id)==479:
                #     print task.request_due_date
                #     print task.due_date_request_reason
                if (worker==task.client or admin)\
                    and task_type == 'one_time'\
                        and task.request_due_date:
                    # print 'OK'
                    self.request_due_date = task.request_due_date
                    self.due_date_request_reason =\
                        task.due_date_request_reason
                # end fix #53
                if task_type == 'one_time':
                    self.new_comment_anchor=''
                    if task.notifications:
                        for x in task.notifications.split(';'):
                            # print worker.login,x
                            if worker.login in x:
                                self.new_comment_anchor = x.split('|')[-1]
                                # print self.new_comment_anchor
                try:
                    self.due_date = task.due_date
                except:
                    self.due_date = task.next_date
                self.task_type = task_type

        for t in my_tasks:
            all_my_tasks.append(SimpleTask(t,'one_time'))
        for t in my_regular_tasks:
            all_my_tasks.append(SimpleTask(t,'regular'))
        tmp = list(tasks_overdue)
        tasks_overdue = []
        for t in tmp:
            tasks_overdue.append(SimpleTask(t,'one_time'))
        tmp = list(tasks_for_today)
        tasks_for_today = []
        for t in tmp:
            tasks_for_today.append(SimpleTask(t,'one_time'))
        tmp = list(tasks_future)
        tasks_future = []
        for t in tmp:
            tasks_future.append(SimpleTask(t,'one_time'))


        all_my_tasks = tasks_separation(all_my_tasks)
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

        # получаем непросмотренные сообщения
        notifications = Message_Visit.objects.filter(worker=worker)

        # получаем категории задач для создания панели с быстрыми
        # ссылками
        tasks_categories = get_full_option(
            '{0}_settings'.format(user), 'tasks_category_groups')
        if tasks_categories:
            tasks_categories = tasks_categories.value.split(';')

        # только для админов
        # admin = False
        all_tasks=[]
        tasks_to_confirm=[]
        # if user in admins:
        if admin:
            # admin = True
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
    # return render_to_response(languages[lang]+'tasks.html',
    return (True,
            ('tasks.html',
             {},
            {'my_error':my_error,'user':user,'worker':worker,
            'tasks_overdue':tasks_overdue,
            'tasks_for_today':tasks_for_today,
            'tasks_future':tasks_future,'my_tasks':all_my_tasks,
            'tasks_to_confirm':tasks_to_confirm,'all_tasks':all_tasks,
            'alert':alert,'admin':admin,'regular_tasks':regular_tasks,
             'tasks_categories': tasks_categories,
             'nearest_count':nearest_count, 'notifications': notifications,
             'tasks_id_string': ','.join(map(str,tasks_id_list)),
             'rtasks_id_string': ','.join(map(str,rtasks_id_list)),
            },
             request,
             app))

@login_required
def task(request,task_type,task_id):
    lang=select_language(request)
    if not acl(request,task_type,task_id):
        request.session['my_error'] =\
            u'Нет права доступа к этой задаче!'
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
        # удаляем оповещения о непрочитанных комментах
        if task_type == 'one_time':
            notifications = task_full.notifications
            if notifications:
                notifications = notifications.split(';')
                tmp = []
                for record in notifications:
                    if fio.login not in record:
                        tmp.append(record)
                task_full.notifications = ';'.join(tmp)
                task_full.save()
        # получаем связанные комментарии
        try:
            if task_type == 'one_time':
                tmp_notes = Note.objects.filter(for_task=task_full).\
                    order_by('-timestamp')
            if task_type == 'regular':
                tmp_notes = Note.objects.filter(
                    for_regular_task=task_full).order_by('-timestamp')
        except Note.DoesNotExist:
            tmp_notes = ('Нет подходящих комментариев',)
        # Строим дерево комментариев
        notes=[]
        for note in tmp_notes:
            notes.append(note_with_indent(note,0))
            build_note_tree(note,notes,1)
        # подготовка к выводу описания
        task_full.html_description = htmlize(task_full.description)
        # если регулярная задача - получаем человеческое описание
        # регулярности периода
        if task_type=='regular':
            task_full.russian_period = \
                crontab_to_russian(task_full.period)
        method = request.method
        if request.method == 'POST':
            # если вносим изменения в заявку
            form = l_forms[lang]['NoteToTicketAddForm'](request.POST)
            # проверяем валидность формы
            if form.is_valid():
                data = form.cleaned_data
                # если добавляем комментарий
                if request.POST.get('add_comment'):
                    note = Note(
                        timestamp = datetime.datetime.now(),
                        note = data['note'],
                        author = fio
                    )
                    note.save()
                    if task_type == 'one_time':
                        note.for_task.add(task_full)

                        # добавляем, кого оповестить о комменте
                        if not task_full.notifications:
                            task_full.notifications = ''
                        task_full.notifications =\
                            task_full.notifications.strip(';')
                        for person in data['workers']:
                            if person.login not in\
                                    task_full.notifications:
                                task_full.notifications =\
                                    task_full.notifications + \
                                    ';' + person.login + '|' +\
                                    str(note.id)
                        task_full.notifications =\
                            task_full.notifications.strip(';')

                    if task_type == 'regular':
                        note.for_regular_task.add(task_full)
                    # кому будем его отпарвлять
                    mails = \
                        [person.mail for person in data['workers']]
                    # вносим изменения в права на просмотр, чтобы
                    # тем, кому отправили комментарий, заявка тоже
                    # была доступна
                    acl_list = task_full.acl.split(';')
                    for person in data['workers']:
                        if person.login not in acl_list:
                            acl_list.append(person.login)
                    task_full.acl = ';'.join(acl_list)
                    task_full.save()
                    # print mails
                    send_email_html(
                        u"Новый комментарий к задаче: " +
                        task_full.name,
                        u"<b>Комментарий</b><table cellpadding='5' "
                        u"border='1'><tr><td>" +
                        htmlize(note.note) +
                        u"</td></tr></table><p>"
                        u"<b>Описание задачи</b>"
                        u"<table cellpadding='5' border='1'><tr>"
                        u"<td>" + task_full.description +  # уже html
                        u"</td></tr></table><p>"
                        u"<b>Посмотреть задачу можно тут</b>:<p>"
                        u"http://"+server_ip+"/task/" +
                        task_addr[task_type]+"/"+str(task_full.id),
                        mails)
                    set_last_activity(user,request.path)
                    return HttpResponseRedirect(request.
                                                get_full_path())
                elif request.POST.get('answer_to_comment'):
                    parent_note = Note.\
                        objects.get(id=int(
                        request.POST.get('to_note')))
                    note = Note(
                        timestamp = datetime.datetime.now(),
                        note = request.POST.get('answer'),
                        author = fio,
                    )
                    note.save()
                    note.parent_note.add(parent_note)
                    note.save()

                    # добавляем, кого оповестить о комменте
                    if not task_full.notifications:
                        task_full.notifications = ''
                    task_full.notifications =\
                        task_full.notifications.strip(';')
                    if parent_note.author.login not in\
                            task_full.notifications and \
                                    parent_note.author.login !=\
                                    fio.login:
                        task_full.notifications =\
                            task_full.notifications + \
                            ';' + parent_note.author.login + '|' +\
                            str(note.id)
                    task_full.notifications =\
                        task_full.notifications.strip(';')
                    task_full.save()

                    mails = \
                        (parent_note.author.mail
                         if parent_note.author.mail else '' ,)
                    send_email_html(
                        u"Ответ на ваш комментарий к задаче: " +
                        task_full.name,
                        u"<table cellpadding='5' border='1'>"
                        u"<tr><td>Ваш комментарий</td><td>" +
                        htmlize(parent_note.note) +
                        u"</td></tr><tr><td>Ответ</td><td>"
                        u"<table cellpadding='20'><tr><td> " +
                        htmlize(note.note) +
                        u"</td></tr></table></td></tr>"
                        u"</table>"
                        u"<b>Описание задачи</b>:"
                        u"<table border='1'><tr><td>" +
                        task_full.description +
                        u"</td></tr></table>"
                        u"<b>Посмотреть задачу можно тут:</b>"
                        u"http://" + server_ip + "/task/" +
                        task_addr[task_type] +
                        "/" + str(task_full.id),
                        mails)
                    set_last_activity(user,request.path)
                    return HttpResponseRedirect(request.get_full_path())
                elif request.POST.get('del_comment'):
                    note_to_del_id=request.POST.get('num')
                    note_to_del = Note.objects.get(id=note_to_del_id)
                    # Если есть дочерние комментарии - прикрепить к
                    #  родительской заметке или к задаче
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
                        # Если есть родительский комментарий
                        #  - прикрепляем к нему
                        if parent_note:
                            parent_note.children_note.\
                                add(children_note)
                            parent_note.save()
                        # Если родительского комментария нет
                        #  - прикрепляем к задаче
                        else:
                            if task_type == 'one_time':
                                children_note.for_task.add(task_full)
                            if task_type == 'regular':
                                children_note.for_regular_task.\
                                    add(task_full)
                            children_note.save()                    
                    note_to_del.delete()
                    set_last_activity(user,request.path)
                    return HttpResponseRedirect(
                        request.get_full_path())
                elif request.POST.get('edit_comment'):
                    note_to_edit_id = request.POST.get('num')
                    for note in notes:
                        if note.id != int(note_to_edit_id):
                            note.note = htmlize(note.note)
                    set_last_activity(user,request.path)
                    return render_to_response(
                        languages[lang]+'task.html',
                        {'user':user,'worker':fio,'task':task_full,
                         'admin':admin,
                         'notes':notes, 'form':form,
                         'note_to_edit_id':int(note_to_edit_id),
                         'task_type':task_type},
                        RequestContext(request))
                elif request.POST.get('save_edited_comment'):
                    note_to_edit_id = request.POST.get('num')
                    note_to_edit = Note.objects.get(id=note_to_edit_id)
                    old_comment = note_to_edit.note
                    note_to_edit.note = request.POST.get('text_note_to_edit')
                    note_to_edit.save()
                    send_email_html(
                        u"Отредактирован комментарий к задаче: " +
                        task_full.name,
                        u"<table cellpadding='5' border='1'>"
                        u"<tr><td>Старый комментарий</td><td>"+
                        htmlize(old_comment) +
                        u"</td></tr><tr><td>Новый комментарий</td>"
                        u"<td>" + htmlize(note_to_edit.note) +
                        u"</td></tr></table>"
                        u"<b>Посмотреть задачу можно тут</b>:"
                        u"http://"+server_ip+"/task"
                                                      "/"+task_addr[task_type]+"/"+str(task_full.id),[task_full.worker.mail,task_full.client.mail])
                    set_last_activity(user,request.path)
                    return HttpResponseRedirect(request.get_full_path())

        else:
            form = l_forms[lang]['NoteToTicketAddForm'](defaults = (task_full.worker.fio, task_full.client.fio),exclude = (fio,))
            for note in notes:
                note.note = htmlize(note.note)
            files=task_full.file.all()
            children_tasks = []
            build_tasks_tree(task_full,children_tasks,0)
            # files[0].file.url
            set_last_activity(user,request.path)
            # task_full.due_date_history = task_full.due_date_history.split('|')
            task_full.build_history()
            return render_to_response(languages[lang]+'task.html',
                                      {'files':files,'user':user,
                                       'worker':fio,'task':task_full,
                                       'notes':notes, 'form':form,
                                       'task_type':task_type,
                                       'admin':admin,
                                       'children_tasks':children_tasks},
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
        request.session['my_error'] = u'Нет права доступа к этой' \
                                      u' задаче!'
        return HttpResponseRedirect("/tasks/")

    task_to_close = Task.objects.get(id=task_to_close_id)
    method = request.method
    user = request.user.username
    admin = False
    if user in admins:
        admin = True
    try:
        fio = Person.objects.get(login=user)
    except Person.DoesNotExist:
        fio = FioError()
    try:
        tmp_notes = Note.objects.filter(for_task=task_to_close).\
            order_by('-timestamp')
    except Note.DoesNotExist:
        tmp_notes = ('Нет подходящих заметок',)
    notes=[]
    for note in tmp_notes:
        notes.append(note_with_indent(note,0))
        build_note_tree(note,notes,1)
    # если закрываем заявку
    if request.method == 'POST':
        form = l_forms[lang]['TicketClosingForm'](request.POST)
        # form = TicketClosingForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            task_to_close.pbw=data['pbw']
            task_to_close.done_date=data['done_date']
            task_to_close.percentage=100
            task_to_close.save()
            request.session['my_error'] = u'Задача благополучно' \
                                          u' закрыта! Ещё одну? ;)'
            send_email_html(u"Задача закрыта и требует"
                            u" подтверждения: " +
                            task_to_close.name,
                            u"<table "
                            u"cellpadding='5' border='1'>"
                            u"<tr><td>Описание задачи</td>"
                            u"<td>" +
                            htmlize(task_to_close.description) +
                            u"</td></tr><tr><td>Сделано для решения"
                            u" проблемы / Выявленныая проблема</td>"
                            u"<td>"+task_to_close.pbw.name+"</td>"
                            u"</table>"
                            u"<b>Посмотреть задачу можно"
                            u" тут</b>: " +
                            htmlize("http://"+server_ip+
                                   "/task/one_time/"+
                                   str(task_to_close.id)),
                                   [task_to_close.client.mail,]+
                                   admins_mail)#,fio)
            return HttpResponseRedirect('/tasks/')
    # если хотим закрыть заявку
    else: 
        # проверяем, есть ли незакрытые дочерние заявки. Если есть - выводим их список на новой странице
        try:
            not_closed_children_tasks = Task.objects.\
                filter(deleted = False).\
                filter(parent_task = task_to_close).\
                exclude(percentage__exact=100)
        except:
            not_closed_children_tasks = ''
        if not_closed_children_tasks:
            set_last_activity(user,request.path)
            return render_to_response(
                languages[lang]+'not_closed_children.html',
                {'user':user,'fio':fio,'task_to_close':task_to_close,
                 'not_closed_children_tasks':not_closed_children_tasks},
                RequestContext(request))
        form = l_forms[lang]['TicketClosingForm']\
            ({'done_date' : datetime.datetime.now(),})
    task_to_close.description = htmlize(task_to_close.description)
    for note in notes:
        note.note = htmlize(note.note)
    set_last_activity(user,request.path)

    # fix #11
    pwds = ProblemByWorker.objects.all()
    # font_size_min = 14
    # font_size_max = 60
    # нормируем размер шрифта, чтобы он не вылизал за эти границы
    # Для начала получим разборс весов, дальше смотрим сколько
    # "веса" надо для перехода в следующий размер и на основании
    # этого вычисляем размер шрифта
    sizes = [float(x.weight) for x in pwds]
    min_weight = min(sizes)
    max_weight = max(sizes)
    # print min_weight,max_weight
    # font_size_step = (max_weight-min_weight)/\
    #                  (font_size_max-font_size_min)
    # print font_size_step
    for pwd in pwds:
        # normalized_size = (pwd.weight-min_weight)/font_size_step +\
        #                   font_size_min
        # pwd.font_size = str(normalized_size).replace(',','.')
        pwd.weight = str(pwd.weight).replace(',','.')
        # pwd.link = "http://google.com"

    # end fix #11
    return render_to_response(languages[lang]+'close_ticket.html',
                              {'user':user,'fio':fio,'form':form,
                               'task':task_to_close,'notes':notes,
                               'pwds':pwds,'worker':fio,
                               'admin':admin},
                              RequestContext(request))
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
    send_email_html(
        u"Задача открыта заново: " + task_to_unclose.name,
        u"<b>Описание задачи</b><table cellpadding='5' border='1'>"
        u"<tr><td>" + task_to_unclose.description + u"</td></tr>"
        u"</table><b>Посмотреть задачу можно тут</b>: " +
        htmlize("http://" + server_ip + "/task/one_time/" +
                str(task_to_unclose.id)),
        [task_to_unclose.client.mail,
         task_to_unclose.worker.mail] + admins_mail,
        fio)
    set_last_activity(user,request.path)
    return HttpResponseRedirect('/tasks/')
@login_required
def to(request, to_who):
    lang=select_language(request)
    user = request.user.username
    method = request.method
    if user in admins:
        admin = True
    else:
        admin = False
    try:
        fio = Person.objects.get(login=user)
    except Person.DoesNotExist:
        fio = FioError()
    if request.session.get('my_error'):
        my_error = [request.session.get('my_error'),]
    else:
        my_error=[]
    request.session['my_error'] = ''
    # if user not in admins:
    #     return HttpResponseRedirect("/tasks/")
    tasks = list()
    for task_type in task_types:
        if task_type != 'regular':
            for task in task_types[task_type].objects.\
                    filter(client = fio).\
                    filter(deleted = False).\
                    filter(percentage__lt=100).\
                    filter(start_date__lt=datetime.datetime.now()).\
                    filter(when_to_reminder__lt=datetime.datetime.now()).\
                    filter(category=Categories.objects.get(name=to_who).id):
                task.task_type=task_type
                tasks.append(task)
        else:
            for task in task_types[task_type].objects.\
                    filter(client = fio).\
                    filter(deleted = False).\
                    filter(next_date__lt=datetime.datetime.now()).\
                    filter(when_to_reminder__lt=datetime.datetime.now()).\
                    filter(category=Categories.objects.get(name=to_who).id):
                task.task_type=task_type
                tasks.append(task)
    tasks_to = list(chain(tasks))
    notes={}
    for task in tasks_to:
        task.description = htmlize(task.description)
        try:
            notes[task.id] = Note.objects.filter(for_task=task).order_by('-timestamp')
        except Note.DoesNotExist:
            notes[task.id] = None
        except ValueError:
            notes[task.id] = None
    for note_to_id in notes:
        if notes[note_to_id]:
            for note in notes[note_to_id]:
                note.note = htmlize(note.note)
    # получаем категории задач для создания панели с быстрыми
    # ссылками
    tasks_categories = get_full_option(
        '{0}_settings'.format(user), 'tasks_category_groups')
    if tasks_categories:
        tasks_categories = tasks_categories.value.split(';')

    set_last_activity(user,request.path)
    return render_to_response(languages[lang]+'tasks_to.html',
                              {'worker':fio,'tasks':tasks_to,
                               'notes':notes,'to_who':to_who,
                               'method':method, 'admin':admin,
                               'tasks_categories':tasks_categories},
                              RequestContext(request))
@login_required
def confirm_task(request,task_to_confirm_id):
    lang=select_language(request)
    user = request.user.username
    if user not in admins:
        request.session['my_error'] = u'Нет права подтвердить закрытие задачи!'
        return HttpResponseRedirect("/tasks/")
    admin = True
    task_to_confirm = Task.objects.get(id=task_to_confirm_id)
    method = request.method
    try:
        fio = Person.objects.get(login=user)
    except Person.DoesNotExist:
        fio = FioError()
    if request.method == 'POST':
        # form = TicketConfirmingForm(request.POST)
        form = l_forms[lang]['TicketConfirmingForm'](request.POST)
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
        form = l_forms[lang]['TicketConfirmingForm']({'confirmed':True, 'confirmed_date':datetime.datetime.now()})
        # try:
        #     notes = Note.objects.filter(for_task=task_to_confirm).order_by('-timestamp')
        # except Note.DoesNotExist:
        #     notes = ('Нет подходящих заметок',)
        # for note in notes:
        #     note.note = htmlize(note.note)

        # fixing #29
        # https://github.com/Ishayahu/MJCC-tasks/issues/29
        try:
            tmp_notes = Note.objects.filter(for_task=task_to_confirm).order_by('-timestamp')
        except Note.DoesNotExist:
            tmp_notes = ('Нет подходящих заметок',)
        notes=[]
        for note in tmp_notes:
            notes.append(note_with_indent(note,0))
            build_note_tree(note,notes,1)
        for note in notes:
            note.note = htmlize(note.note)
        # end fixing #29

    task_to_confirm.description = htmlize(task_to_confirm.description)
    set_last_activity(user,request.path)
    return render_to_response(languages[lang]+'confirm_ticket.html',
                              {'form':form,'task':task_to_confirm,
                               'notes':notes,'method':method,
                               'fio':fio,'admin':admin,
                               'worker':fio,},
                              RequestContext(request))
@login_required
def edit_task(request, task_to_edit_id):
    lang=select_language(request)
    task = Task.objects.get(id=task_to_edit_id)
    method = request.method
    user = request.user.username
    admin = False
    if user in admins:
        admin = True
    try:
        fio = Person.objects.get(login=user)
    except Person.DoesNotExist:
        fio = FioError()

    # редактировать может только админ, работник или клиент
    # if not acl(request,'one_time',task_to_edit_id):
    # print fio
    # print task_to_edit.worker
    if not(admin or fio==task.client or fio==task.worker):
        request.session['my_error'] =\
            u'Нет права редактировать эту задачу!'
        return HttpResponseRedirect("/tasks/")
    if fio == task.worker:
        need_reason = True
    else:
        need_reason = False
    if request.method == 'POST':
        form = l_forms[lang]['TicketEditForm'](
            request.POST,request.FILES)
        # если меняется исполнитель - чтобы оповестить
        old_worker = task.worker
        old_pbu = task.pbu
        old_client = task.client
        old_start_date = task.start_date
        old_category = task.category
        old_due_date = task.due_date
        old_name = task.name

        # # старый варинат
        if form.is_valid():
            # проверка - есть ли файл надо добавить
            def save_file(files):
                instance = File(file=files['file'],
                                timestamp=datetime.datetime.now(),
                                file_name = 'file_name',
                                description = 'TEST',)
                instance.save()
                return instance
            if request.FILES:
                task.file.add(save_file(request.FILES))
                task.save(user=user)
            data = form.cleaned_data
            task.name = data['name']
            task.pbu = data['pbus']
            task.description = data['description']
            task.client = data['clients']
            task.priority = data['priority']
            task.category = data['category']
            task.start_date = data['start_date']
            task.worker = data['workers']

            # fix #53
            if fio == task.worker and not admin:
                task.request_due_date = data['due_date']
                task.due_date_request_reason = \
                    request.POST.get('due_date_request_reason')
            else:
                if task.due_date_editor_level >= fio.level or admin:
                    task.due_date=data['due_date']
                    task.due_date_editor_level = fio.level

            task.percentage=data['percentage']
            task.when_to_reminder=data['when_to_reminder']
            task.save(user=user)
            task_description = htmlize(task.description)
            if task.name != old_name:
                send_email_html(
                    u"Изменёно название задачи: " + old_name,
                    u"<table cellpadding='5' border='1'>"
                    u"<tr><td>Прежнее название</td><td>" +
                    old_name + u"</td></tr><tr><td>Новое название"
                    u"</td><td>" + task.name + u"</td></tr>"
                    u"</table><b>Описание задачи</b>"
                    u"<table cellpadding='5' border='1'><tr><td>" +
                    task_description + u"</td></tr>"
                    u"</table><b>Посмотреть задачу можно тут</b>: " +
                    htmlize("http://" + server_ip +
                            "/task/one_time/" + str(task.id)),
                    [task.worker.mail,
                     task.client.mail] + admins_mail)

            # fix #53
            if task.request_due_date != old_due_date:

                send_email_html(
                    u"Запрос на изменение срока выполнения задачи: " +
                    task.name,
                    u"<table cellpadding='5' border='1'>"
                    u"<tr><td>Прежний срок</td><td>" +
                    str(old_due_date) + u"</td></tr><tr><td>Новий срок"
                    u"</td><td>" + str(task.request_due_date) +
                    u"</td></tr>"
                    u"</table><b>Описание задачи</b>"
                    u"<table cellpadding='5' border='1'><tr><td>" +
                    task_description + u"</td></tr>"
                    u"</table><b>Посмотреть задачу можно тут</b>: " +
                    htmlize("http://" + server_ip +
                            "/task/one_time/" + str(task.id)),
                    [task.worker.mail,
                     task.client.mail] + admins_mail)

            if task.worker != old_worker:
                # добавление нового исполнителя в acl
                if task.worker.login not in task.acl:
                    task.acl = task.acl\
                                   + ";" + task.worker.login
                    task.save()
                send_email_html(
                    u"Изменён исполнитель задачи: " +
                    task.name,
                    u"<table cellpadding='5' border='1'><tr><td>"
                    u"Прежний исполнитель</td><td>" +
                    old_worker.fio + u"</td></tr><tr><td>"
                    u"Новый исполнитель</td><td>" +
                    task.worker.fio + u"</td></tr>"
                    u"</table><b>Описание задачи</b>"
                    u"<table cellpadding='5' border='1'><tr><td>" +
                    task_description+u"</td></tr></table>"
                    u"<b>Посмотреть задачу можно тут</b>: " +
                    htmlize("http://" + server_ip +
                            "/task/one_time/" + str(task.id)),
                    [task.worker.mail,
                     task.client.mail,
                     old_worker.mail] + admins_mail)
            if task.pbu != old_pbu:
                send_email_html(
                    u"Изменёно описание проблемы со слов пользователя"
                    u" для задачи: " + task.name,
                    u"<table cellpadding='5' border='1'><tr><td>"
                    u"Прежная проблема</td><td>" + old_pbu.name +
                    u"</td></tr><tr><td>Новая проблема</td><td>" +
                    task.pbu.name + u"</td></tr></table>"
                    u"<b>Описание задачи</b>"
                    u"<table cellpadding='5' border='1'><tr><td>" +
                    task_description + u"</td></tr></table>"
                    u"<b>Посмотреть задачу можно тут</b>: " +
                    htmlize("http://" + server_ip +
                            "/task/one_time/" + str(task.id)),
                    [task.worker.mail,
                         task.client.mail] + admins_mail)
            if task.client != old_client:
                # добавление нового заказчика в acl
                if task.client.login not in task.acl:
                    task.acl=task.acl \
                                     + ";" + task.client.login
                    task.save()
                send_email_html(
                    u"Изменён заказчик задачи: " + task.name,
                    u"<table cellpadding='5' border='1'><tr><td>"
                    u"Прежний заказчик</td><td>" + old_client.fio +
                    u"</td></tr><tr><td>Новый заказчик</td><td>" +
                    task.client.fio+u"</td></tr></table>"
                    u"<b>Описание задачи</b>"
                    u"<table cellpadding='5' border='1'><tr><td>" +
                    task_description + u"</td></tr></table>"
                    u"<b>Посмотреть задачу можно тут</b>: " +
                    htmlize("http://" + server_ip +
                            "/task/one_time/" + str(task.id)),
                    [task.worker.mail,
                     task.client.mail,
                     old_client.mail] + admins_mail)
            if task.category != old_category:
                send_email_html(
                    u"Изменёна категория задачи: " +
                    task.name,
                    u"<table cellpadding='5' border='1'><tr><td>"
                    u"Прежная категория</td><td>" +
                    old_category.name +
                    u"</td></tr><tr><td>Новая категория</td><td>" +
                    task.category.name + u"</td></tr></table>"
                    u"<b>Описание задачи</b>"
                    u"<table cellpadding='5' border='1'><tr><td>" +
                    task_description+u"</td></tr></table>"
                    u"<b>Посмотреть задачу можно тут</b>: " +
                    htmlize("http://" + server_ip +
                            "/task/one_time/" + str(task.id)),
                    [task.worker.mail,
                     task.client.mail] + admins_mail)
            if task.due_date != old_due_date:
                send_email_html(
                    u"Изменён срок выполонения задачи: "
                    + task.name,
                    u"<table cellpadding='5' border='1'><tr><td>"
                    u"Старый срок</td><td>" + str(old_due_date) +
                    u"</td></tr><tr><td>Новый срок</td><td>" +
                    str(task.due_date) +
                    u"</td></tr></table><b>Описание задачи</b>"
                    u"<table cellpadding='5' border='1'><tr><td>" +
                    task_description +
                    u"</td></tr></table>"
                    u"<b>Посмотреть задачу можно тут</b>: " +
                    htmlize("http://" + server_ip +
                            "/task/one_time/" + str(task.id)),
                    [task.worker.mail,
                     task.client.mail] + admins_mail)
            if task.start_date != old_start_date:
                send_email_html(
                    u"Изменена дата начала задачи: " +
                    task.name,
                    u"<table cellpadding='5' border='1'><tr><td>"
                    u"Прежняя дата начала</td><td>" +
                    str(old_start_date) +
                    u"</td></tr><tr><td>Новая дата начала</td><td>" +
                    str(task.start_date) +
                    u"</td></tr></table><b>Описание задачи</b>"
                    u"<table cellpadding='5' border='1'><tr><td>" +
                    task_description + u"</td></tr></table>"
                    u"<b>Посмотреть задачу можно тут</b>: " +
                    htmlize("http://" + server_ip +
                            "/task/one_time/" + str(task.id)),
                    [task.worker.mail,
                     task.client.mail] + admins_mail)
            set_last_activity(user,request.path)
            return HttpResponseRedirect('/tasks/')
    else:
        form = l_forms[lang]['TicketEditForm']({'name' : task.name,
            'pbus' : task.pbu,
            'description' : task.description,
            'clients' : task.client,
            'priority' : task.priority,
            'category' : task.category,
            'start_date' : task.start_date,
            'when_to_reminder' : task.when_to_reminder,
            'due_date' : task.due_date,
            'workers' : task.worker,
            'percentage' : task.percentage,
            # 'file':task_to_edit.file,
        })
        if fio.level > task.due_date_editor_level and not admin:
            del form.fields['due_date']
    set_last_activity(user,request.path)
    return render_to_response(languages[lang]+'new_ticket.html',
                              {'worker':fio,'form':form,
                               'admin':admin,'need_reason':need_reason,
                               'method':method},
    RequestContext(request))
@login_required
def delete_task(request,task_type,task_to_delete_id):
    lang=select_language(request)
    user = request.user.username
    task_to_delete = task_types[task_type].\
        objects.get(id=task_to_delete_id)
    task_to_delete.deleted = True
    task_to_delete.save()
    set_last_activity(user,request.path)
    return HttpResponseRedirect('/tasks/')
@login_required
def undelete_task(request,task_type,task_id):
    lang=select_language(request)
    user = request.user.username
    task = task_types[task_type].objects.get(id=task_id)
    task.deleted = False
    task.save(user=user)
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
        tmp_notes = Note.objects.filter(for_task=task).\
            order_by('-timestamp')
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
            for task in task_types[task_type].objects.\
                    filter(deleted = True):
                task.task_type=task_type
                tasks.append(task)
        tasks = list(chain(tasks))
    except:
        pass
    for task in tasks:
	try:
	    tmp_notes = Note.objects.filter(for_task=task).\
            order_by('-timestamp')
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
            for task in task_types[task_type].objects.\
                    filter(deleted = True):
                task.task_type=task_type
                tasks.append(task)
        tasks = list(chain(tasks))
    except:
        task = ('Нет таких задач',)
    set_last_activity(user,request.path)
    return render_to_response(languages[lang]+'deleted_tasks.html',
                              {'tasks':tasks,},
                              RequestContext(request))

@login_required
def all_tasks(request,page_number):
    lang=select_language(request)
    def find_parent_task(note,task_type):
        """
        Поиск родительской заявки для примечания
        """
        try:
            if note.parent_note:
                return find_parent_task(
                    note.parent_note.get(),task_type)
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
        # form = TicketSearchForm(request.POST)
        form = l_forms[lang]['TicketSearchForm'](request.POST)
        if form.is_valid():
            data = form.cleaned_data
            # какая-то фигня - поиск должен не зависеть от регистра. Если ищем ascii - работает, если кирилицу - нет(

            try:
                finded_tasks_names = Task.objects.filter(
                    name__icontains = data['name'])
                finded_tasks_desc = Task.objects.filter(
                    description__icontains = data['name'])
                finded_rtasks_names = RegularTask.objects.filter(
                    name__icontains = data['name'])
                finded_rtasks_desc = RegularTask.objects.filter(
                    description__icontains = data['name'])
                notes = Note.objects.filter(
                    note__icontains = data['name'])
                finded_tasks_notes=[]
                finded_rtasks_notes=[]
                for note in notes:
                    finded_tasks_notes = find_parent_task(
                        note = note,task_type='one_time')
                    finded_rtasks_notes = find_parent_task(
                        note = note,task_type='regular')

                # fix 42
                # https://github.com/Ishayahu/MJCC-tasks/issues/42
                task_list = list(set(chain(finded_tasks_names,
                                           finded_tasks_desc,
                                           finded_tasks_notes)))
                rtask_list = list(set(chain(finded_rtasks_names,
                                           finded_rtasks_desc,
                                           finded_rtasks_notes)))
                for task in task_list:
                    task.in_link_type = 'one_time'

                for task in rtask_list:
                    task.in_link_type = 'regular'

                finded_tasks = list(set(chain(task_list,
                                              rtask_list,)))
                # end fix 42

                if not finded_tasks:
                    not_finded = True


            except:
                # print 'exception'
                not_finded = True
            set_last_activity(user,request.path)
            return render_to_response(languages[lang]+'all_tasks.html',
                                      {'not_finded':not_finded,
                                       'finded_tasks':finded_tasks,
                                       'form':form, 'method':method,
                                       'admin':admin,'worker':fio},
                                      RequestContext(request))
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
    admin = False
    if user in admins:
        admin=True
    try:
        fio = Person.objects.get(login=user)
    except Person.DoesNotExist:
        fio = FioError()
    try:
        # находим родительскую задачу
        parent_task = task_types[parent_task_type].objects.get(id=parent_task_id)
    except:
        my_error=request.session.get('my_error')# если задач нет - вывести это в шаблон
        my_error.append('Не найдена родительская задача?!')
        return HttpResponseRedirect('/tasks/')
    if request.method == 'POST':
        form = l_forms[lang]['NewTicketForm'](request.POST)
        # form = NewTicketForm(request.POST)
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
    return render_to_response(languages[lang]+'new_ticket.html',
                              {'form':form, 'method':method,
                               'admin':admin, 'worker':fio},
                              RequestContext(request))

@login_required
def regular_task_done(request,task_id):
    # lang=select_language(request)
    user = request.user.username
    # method = request.method
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
    set_last_activity(user, request.path)
    return HttpResponseRedirect('/tasks/')

@login_required
# @shows_errors
def get_all_logged_in_users(request):
    lang = select_language(request)
    user = request.user.username
    if user in admins:
        last_activities=get_last_activities()
        for act in last_activities:
            act.day = act.timestamp.day
            act.month = act.timestamp.month
            act.year = act.timestamp.year
        return render_to_response(
            languages[lang]+'logged_in_user_list.html',
            {'last_activities': last_activities, 'admin': True},
            RequestContext(request))

@login_required
@multilanguage
@shows_errors
@for_admins
def get_user_activity_history(request,user_login,date):
    print user_login
    try:
        d,m,y = date.split('.')
        date = datetime.date(int(y), int(m), int(d))
    except:
        date = datetime.datetime.now().date()
    try:
        person = Person.objects.get(login=user_login)
    except Person.DoesNotExist:
        add_error(u"Не найден пользователь {0}".format(user_login),
                  request)
        # request.session.modified = True
        return (False,(HttpResponseRedirect('/users/')))
    last_activities = get_user_per_date_activities(date=date,
                                                   person=person)
    return (True,('user_activity.html',{},
                      {'title': 'История активности',
                       'last_activities': last_activities,
                       'user': person,
                       'date': date,},
                      request,
                      app))

@login_required
@multilanguage
@shows_errors
@for_admins
@admins_only
def messages_add(request):
    lang, login, user, method = get_info(request)
    if method == 'POST':
        form = get_localized_form('NewMessageForm', app, request)\
            (request.POST)
        if form.is_valid():
            data = form.cleaned_data
            m=Message(name=data['name'],
                      text=data['text'],
                      author=user,
                      timestamp=datetime.datetime.now(),)
            m.save()
            # добавляем оповещения для всех пользователей
            all_persons = Person.objects.all()
            for person in all_persons:
                if person != user:
                    mp = Message_Visit(message = m,
                                       worker = person)
                    mp.save()
        return (False,(HttpResponseRedirect('/tasks/')))
    return (True,('any_form.html',
                  {'NewMessageForm':{}},
                  {'title': 'Добавление сообщения',
                   'form_template_name':'form',
                   'user': user,},
                  request,
                  app))

@login_required
@multilanguage
@shows_errors
@for_admins
def messages_show_message(request,message_id):
    lang, login, user, method = get_info(request)
    message = Message.objects.get(id=int(message_id))
    message.text = htmlize(message.text)
    notification = Message_Visit.objects.filter(message=message).\
        filter(worker=user)
    notification.delete()
    return (True,('any_text.html',
                  {},
                  {'title': 'Cообщение №{0}'.format(message_id),
                   'message':message,
                   'user': user,},
                  request,
                  app))

@login_required
@multilanguage
@shows_errors
@for_admins
def accept_request_due_date(request,task_id):
    lang, login, user, method = get_info(request)
    task = Task.objects.get(id=task_id)
    if (user==task.client or user in admins):
        # task.due_date_history += u"|"+unicode(datetime.datetime.now())+u";user;accept"
        task.due_date = task.request_due_date
        task.request_due_date = None
        task.save(user=user)
        send_email_html(
                    u"Запрос на изменение срока выполнения задачи: " +
                    task.name + u" принят",
                    u"Новий срок: " + str(task.due_date) +
                    u"<p><b>Описание задачи</b>"
                    u"<table cellpadding='5' border='1'><tr><td>" +
                    htmlize(task.description) + u"</td></tr>"
                    u"</table><b>Посмотреть задачу можно тут</b>: " +
                    htmlize("http://" + server_ip +
                            "/task/one_time/" + str(task.id)),
                    [task.worker.mail,
                     task.client.mail] + admins_mail)
    else:
        add_error(u'Нет прав',request)
    return (False,(HttpResponseRedirect('/tasks/')))

@login_required
@multilanguage
@shows_errors
@for_admins
def reject_request_due_date(request,task_id):
    lang, login, user, method = get_info(request)
    task = Task.objects.get(id=task_id)
    if (user==task.client or user in admins):
        # task.due_date_history += u"|"+unicode(datetime.datetime.now())+u"user;reject"
        task.request_due_date = None
        task.save(user=user)
        send_email_html(
                    u"Запрос на изменение срока выполнения задачи: " +
                    task.name + u" отклонён",
                    u"Прежний срок: " + str(task.due_date) +
                    u"<p><b>Описание задачи</b>"
                    u"<table cellpadding='5' border='1'><tr><td>" +
                    htmlize(task.description) + u"</td></tr>"
                    u"</table><b>Посмотреть задачу можно тут</b>: " +
                    htmlize("http://" + server_ip +
                            "/task/one_time/" + str(task.id)),
                    [task.worker.mail,
                     task.client.mail] + admins_mail)
    else:
        add_error(u'Нет прав',request)
    return (False,(HttpResponseRedirect('/tasks/')))
