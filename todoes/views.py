# -*- coding:utf-8 -*-
# coding=<utf8>

from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render_to_response
import datetime
from todoes.models import Note, Resource, File, Person, Task, ProblemByWorker, ProblemByUser, Categories, RegularTask, Activity
from todoes.forms import NewTicketForm, NoteToTicketAddForm, UserCreationFormMY, TicketClosingForm, TicketConfirmingForm, TicketEditForm,TicketSearchForm, NewRegularTicketForm, EditRegularTicketForm, File_and_NoteToTicketAddForm
from django.contrib.auth.decorators import login_required
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.template import RequestContext
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from itertools import chain

from djlib.cron_utils import decronize, crontab_to_russian, generate_next_reminder
from djlib.text_utils import htmlize
from djlib.acl_utils import acl
from djlib.user_tracking import set_last_activity_model, get_last_activities
from djlib.mail_utils import send_email_alternative

from user_settings import server_ip, admins, admins_mail
from user_settings import todoes_url_not_to_track as url_not_to_track
from user_settings import todoes_url_one_record as url_one_record

from todoes.utils import build_note_tree, note_with_indent, FioError

task_types = {'one_time':Task,'regular':RegularTask}
task_addr = {'one_time':'one_time','regular':'regular'}


def set_last_activity(login,url):
    set_last_activity_model(login,url,url_not_to_track,url_one_record)

@login_required
def new_ticket(request):
    user = request.user.username
    try:
        fio = Person.objects.get(login=user)
    except Person.DoesNotExist:
        fio = FioError
    method = request.method
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
            # отправляем уведомление исполнителю по мылу
            send_email_alternative(u"Новая задача: "+t.name,t.description+u"\nПосмотреть задачу можно тут:\nhttp://"+server_ip+"/task/one_time/"+str(t.id),[data['workers'].mail,data['clients'].mail],fio)
            set_last_activity(user,request.path)
            return HttpResponseRedirect('/tasks/')
    else:
        form = NewTicketForm({'percentage':0,'start_date':datetime.datetime.now(),'due_date':datetime.datetime.now(),'priority':3})
    set_last_activity(user,request.path)
    return render_to_response('new_ticket.html', {'form':form, 'method':method},RequestContext(request))

@login_required
def new_regular_ticket(request):
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
            send_email_alternative(u"Новая повторяющаяся задача: "+t.name,t.description+u"\nПосмотреть задачу можно тут:\nhttp://"+server_ip+"/task/regular/"+str(t.id),[data['workers'].mail,data['clients'].mail],fio)
            set_last_activity(user,request.path)
            return HttpResponseRedirect('/tasks/')
    else:
        form = NewRegularTicketForm({'start_date':datetime.datetime.now(),'due_date':datetime.datetime.now(),'priority':3})
    set_last_activity(user,request.path)
    return render_to_response('new_regular_task.html', {'form':form, 'method':method},RequestContext(request))
@login_required
def edit_regular_task(request,task_to_edit_id):
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
            task_to_edit.save()
            if task_to_edit.period != old_period:
                send_email(u"Изменёна периодичность выполонения задачи: "+task_to_edit.name,u"Старый срок:"+crontab_to_russian(period)+u"\nНовый срок:"+crontab_to_russian(task_to_edit.period)+u"\nПосмотреть задачу можно тут:\nhttp://"+server_ip+"/task/regular/"+str(task_to_edit.id),[task_to_edit.worker.mail,task_to_edit.client.mail,old_worker.mail]+admins_mail)
                
            if task_to_edit.name != old_name:
                send_email_alternative(u"Изменёно название задачи: "+old_name,
                           u"Прежнее название:"+old_name+u"\nНовое название:"+task_to_edit.name+u"\nОписание задачи:\n"+task_to_edit.description+u"\nПосмотреть задачу можно тут:\nhttp://"+server_ip+"/task/regular/"+str(task_to_edit.id),
                           [task_to_edit.worker.mail,task_to_edit.client.mail]+admins_mail,
                           fio
                           )
            if task_to_edit.worker != old_worker:
                # добавление нового исполнителя в acl
                if task_to_edit.worker.login not in task_to_edit.acl:
                    task_to_edit.acl=task_to_edit.acl+";"+task_to_edit.worker.login
                    task_to_edit.save()
                send_email_alternative(u"Изменён исполнитель задачи: "+task_to_edit.name,
                           u"Прежний исполнитель:"+old_worker.fio+u"\nНовый исполнитель:"+task_to_edit.worker.fio+u"\nОписание задачи:\n"+task_to_edit.description+u"\nПосмотреть задачу можно тут:\nhttp://"+server_ip+"/task/regular/"+str(task_to_edit.id),
                           [task_to_edit.worker.mail,task_to_edit.client.mail,old_worker.mail]+admins_mail,
                           fio
                           )
            if task_to_edit.stop_date != old_stop_date:
                send_email_alternative(u"Изменёна дата завершения регулярной задачи: "+task_to_edit.name,
                           u"Прежная проблема:"+str(old_stop_date)+u"\nНовая проблема:"+str(task_to_edit.stop_date)+u"\nОписание задачи:\n"+task_to_edit.description+u"\nПосмотреть задачу можно тут:\nhttp://"+server_ip+"/task/regular/"+str(task_to_edit.id),
                           [task_to_edit.worker.mail,task_to_edit.client.mail]+admins_mail,
                           fio
                           )
            if task_to_edit.client != old_client:
                # добавление нового исполнителя в acl
                if task_to_edit.client.login not in task_to_edit.acl:
                    task_to_edit.acl=task_to_edit.acl+";"+task_to_edit.client.login
                    task_to_edit.save()
                send_email_alternative(u"Изменён заказчик задачи: "+task_to_edit.name,
                           u"Прежний заказчик:"+old_client.fio+u"\nНовый заказчик:"+task_to_edit.client.fio+u"\nОписание задачи:\n"+task_to_edit.description+u"\nПосмотреть задачу можно тут:\nhttp://"+server_ip+"/task/regular/"+str(task_to_edit.id),
                           [task_to_edit.worker.mail,task_to_edit.client.mail,old_client.mail]+admins_mail,
                           fio
                           )
            if task_to_edit.category != old_category:
                send_email_alternative(u"Изменёна категория задачи: "+task_to_edit.name,
                           u"Прежная категория:"+old_category.name+u"\nНовая категория:"+task_to_edit.category.name+u"\nОписание задачи:\n"+task_to_edit.description+u"\nПосмотреть задачу можно тут:\nhttp://"+server_ip+"/task/regular/"+str(task_to_edit.id),
                           [task_to_edit.worker.mail,task_to_edit.client.mail]+admins_mail,
                           fio
                           )
            if task_to_edit.period != old_period:
                send_email_alternative(u"Изменёна периодичность выполонения задачи: "+task_to_edit.name,
                           u"Старый срок:"+crontab_to_russian(period)+u"\nНовый срок:"+crontab_to_russian(task_to_edit.period)+u"\nОписание задачи:\n"+task_to_edit.description+u"\nПосмотреть задачу можно тут:\nhttp://"+server_ip+"/task/regular/"+str(task_to_edit.id),
                           [task_to_edit.worker.mail,task_to_edit.client.mail]+admins_mail,
                           fio
                           )                
            set_last_activity(user,request.path)
            return HttpResponseRedirect('/tasks/')
    else:
        form = EditRegularTicketForm({'name' : task_to_edit.name,
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
    return render_to_response('new_regular_task.html', {'form':form, 'method':method,'period':task_to_edit.period,'russian_period':crontab_to_russian(task_to_edit.period)},RequestContext(request))

    
@login_required
def set_reminder(request,task_type,task_id):
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
        request.session['my_error'] = u'Задача почему-то не найдена. Номер ошибки set_reminder_125!'
        return HttpResponseRedirect('/tasks/')
    if request.method == 'POST':
        if 'datepicker' in request.POST:
            data = request.POST['datepicker']
        if 'time' in request.POST:
            time = request.POST['time']
        dtt = datetime.datetime(*map(int,([data.strip().split('/')[2],data.strip().split('/')[1],data.strip().split('/')[0]]+time.strip().split(':'))))
        task_full.when_to_reminder = dtt
        task_full.save()
        set_last_activity(user,request.path)
        return HttpResponseRedirect('/tasks/')
    else:
        after_hour = str(datetime.datetime.now().hour+1)+":"+str(datetime.datetime.now().minute)
        today = str(datetime.datetime.now().day)+"/"+str(datetime.datetime.now().month)+"/"+str(datetime.datetime.now().year)
    set_last_activity(user,request.path)
    return render_to_response('set_reminder.html', {'method':method,'today':today,'after_hour':after_hour},RequestContext(request))
@login_required
def move_to_call(request,task_type,task_id):
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
    return render_to_response('set_reminder.html', {'method':method,'today':today,'after_hour':after_hour},RequestContext(request))

@login_required    
def register(request):
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
        form = UserCreationFormMY()
    return render_to_response("registration/register.html",{'form':form},RequestContext(request))
@login_required    
def profile(request):
    user = request.user.username
    set_last_activity(user,request.path)
    return HttpResponseRedirect("/tasks/")
@login_required
def tasks(request):
    # получаем ошибку, если она установлена и сбрасываем её в запросах
    if request.session.get('my_error'):
        my_error = [request.session.get('my_error'),]
    else:
        my_error=[]
    request.session['my_error'] = ''
    user = request.user.username
    method = request.method
    if  request.method == 'POST':
        for task_to_confirm_id in request.POST.getlist('task_to_confirm_id'):
            task_to_confirm = Task.objects.get(id=int(task_to_confirm_id))
            task_to_confirm.confirmed = True
            task_to_confirm.confirmed_date = datetime.datetime.now()
            task_to_confirm.save()
            send_email(u"Завершение задачи подтверждено: "+task_to_confirm.name,u"\nОписание задачи:\n"+task_to_confirm.description+u"\nПосмотреть задачу можно тут:\nhttp://"+server_ip+"/task/one_time/"+str(task_to_confirm.id),[task_to_confirm.worker.mail,task_to_confirm.client.mail])
        request.session['my_error'] = u'Выполнение задач успешно подтверждено!'
        set_last_activity(user,request.path)
        return HttpResponseRedirect('/tasks/')
    else:
        try:
            worker = Person.objects.get(login=user)
        except Person.DoesNotExist:
            worker = 'Нет такого пользователя'
        # получаем заявки ДЛЯ человека
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
        # получаем заявки ОТ человека
        try:
            # отображаем только НЕ закрытые заявки, т.е. процент выполнения которых меньше 100
            try:
                client = Person.objects.get(login=user)
            except Person.DoesNotExist:
                client = 'Нет такого пользователя'
            my_tasks = Task.objects.filter(deleted = False).filter(client=client,percentage__lt=100)
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
                all_tasks = Task.objects.filter(deleted = False).filter(percentage__lt=100).exclude(client=client).exclude(worker=worker)#.order_by("priority")
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
            return render_to_response('tasks.html',{'my_error':my_error,'user':user,'worker':worker,'tasks_overdue':tasks_overdue,'tasks_for_today':tasks_for_today,'tasks_future':tasks_future,'my_tasks':my_tasks,'tasks_to_confirm':tasks_to_confirm,'all_tasks':all_tasks,'alert':alert,'admin':admin,'regular_tasks':regular_tasks},RequestContext(request))
    set_last_activity(user,request.path)
    return render_to_response('tasks.html',{'my_error':my_error,'user':user,'worker':worker,'tasks_overdue':tasks_overdue,'tasks_for_today':tasks_for_today,'tasks_future':tasks_future,'my_tasks':my_tasks,'alert':alert,'regular_tasks':regular_tasks},RequestContext(request))
@login_required
def task(request,task_type,task_id):

    if not acl(request,task_type,task_id):
        request.session['my_error'] = u'Нет права доступа к этой задаче!'
        return HttpResponseRedirect("/tasks/")
    user = request.user.username
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
                    send_email_alternative(u"Новый комментарий к задаче: "+task_full.name,note.note+u"\nОписание задачи:\n"+task_full.description+u"\nПосмотреть задачу можно тут:\nhttp://1"+server_ip+"/task/"+task_addr[task_type]+"/"+str(task_full.id),mails,fio)
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
                    send_email_alternative(u"Ответ на ваш комментарий к задаче: "+task_full.name,u"Ваш комментарий:\n"+parent_note.note+u"\nОтветили:\n"+note.note+u"\nОписание задачи:\n"+task_full.description+u"\nПосмотреть задачу можно тут:\nhttp://"+server_ip+"/task/"+task_addr[task_type]+"/"+str(task_full.id),mails,fio)
                    set_last_activity(user,request.path)
                    return HttpResponseRedirect(request.get_full_path())
                elif request.POST.get('del_comment'):
                    note_to_del_id=request.POST.get('num')
                    note_to_del = Note.objects.get(id=note_to_del_id)
                    note_to_del.delete()
                    set_last_activity(user,request.path)
                    return HttpResponseRedirect(request.get_full_path())
                elif request.POST.get('edit_comment'):
                    note_to_edit_id = request.POST.get('num')
                    for note in notes:
                        if note.id != int(note_to_edit_id):
                            note.note = htmlize(note.note)
                    set_last_activity(user,request.path)
                    return render_to_response('task.html',{'user':user,'fio':fio,'task':task_full,'notes':notes, 'form':form,'note_to_edit_id':int(note_to_edit_id),'task_type':task_type},RequestContext(request))
                elif request.POST.get('save_edited_comment'):
                    note_to_edit_id = request.POST.get('num')
                    note_to_edit = Note.objects.get(id=note_to_edit_id)
                    old_comment = note_to_edit.note
                    note_to_edit.note = request.POST.get('text_note_to_edit')
                    note_to_edit.save()
                    send_email_alternative(u"Отредактирован комментарий к задаче: "+task_full.name,u"Старый комментарий:"+old_comment+u"\nНовый комментарий"+note_to_edit.note+u"\nПосмотреть задачу можно тут:\nhttp://"+server_ip+"/task/"+task_addr[task_type]+"/"+str(task_full.id),[task_full.worker.mail,task_full.client.mail],fio)
                    set_last_activity(user,request.path)
                    return HttpResponseRedirect(request.get_full_path())

        else:
            form = NoteToTicketAddForm(defaults = (task_full.worker.fio, task_full.client.fio),exclude = (fio,))
            for note in notes:
                note.note = htmlize(note.note)
            set_last_activity(user,request.path)
            return render_to_response('task.html',{'user':user,'fio':fio,'task':task_full,'notes':notes, 'form':form,'task_type':task_type},RequestContext(request))
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
            send_email_alternative(u"Задача закрыта и требует подтверждения: "+task_to_close.name,u"\nПосмотреть задачу можно тут:\nhttp://"+server_ip+"/task/one_time/"+str(task_to_close.id),[task_to_close.client.mail,]+admins_mail,fio)
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
            return render_to_response('not_closed_children.html', {'user':user,'fio':fio,'task_to_close':task_to_close,'not_closed_children_tasks':not_closed_children_tasks},RequestContext(request))
        form = TicketClosingForm({'done_date' : datetime.datetime.now(),})
    task_to_close.description = htmlize(task_to_close.description)
    for note in notes:
        note.note = htmlize(note.note)
    set_last_activity(user,request.path)
    return render_to_response('close_ticket.html', {'user':user,'fio':fio,'form':form, 'task':task_to_close,'notes':notes},RequestContext(request))
@login_required
def unclose_task(request,task_to_unclose_id):
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
    send_email(u"Задача открыта заново: "+task_to_unclose.name,u"\nПосмотреть задачу можно тут:\nhttp://192.168.1.157:8080/task/"+str(task_to_unclose.id),[task_to_unclose.client.mail,task_to_unclose.worker.mail]+admins_mail)
    set_last_activity(user,request.path)
    return HttpResponseRedirect('/tasks/')
@login_required
def to(request, to_who):
    user = request.user.username
    method = request.method
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
    return render_to_response('tasks_to.html', {'tasks':tasks_to,'notes':notes,'to_who':to_who, 'method':method},RequestContext(request))
@login_required
def confirm_task(request,task_to_confirm_id):
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
                send_email(u"Завершение задачи подтверждено: "+task_to_confirm.name,u"\nПосмотреть задачу можно тут:\nhttp://"+server_ip+"/task/"+str(task_to_confirm.id),[task_to_confirm.worker.mail,task_to_confirm.client.mail])
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
        form = TicketConfirmingForm({'confirmed':True, 'confirmed_date':datetime.datetime.now()})
        for note in notes:
            note.note = htmlize(note.note)
    task_to_confirm.description = htmlize(task_to_confirm.description)
    set_last_activity(user,request.path)
    return render_to_response('confirm_ticket.html', {'form':form,'task':task_to_confirm,'notes':notes,'method':method,'fio':fio},RequestContext(request))    
@login_required
def edit_task(request,task_to_edit_id):
    if not acl(request,'one_time',task_to_edit_id):
        request.session['my_error'] = u'Нет права доступа к этой задаче!'
        return HttpResponseRedirect("/tasks/")

    task_to_edit = Task.objects.get(id=task_to_edit_id)
    method = request.method
    
    user = request.user.username
    try:
        fio = Person.objects.get(login=user)
    except Person.DoesNotExist:
        fio = FioError()
    
    if request.method == 'POST':
        form = TicketEditForm(request.POST)
        # если меняется исполнитель - чтобы оповестить
        old_worker = task_to_edit.worker
        old_pbu = task_to_edit.pbu
        old_client = task_to_edit.client
        old_category = task_to_edit.category
        old_due_date = task_to_edit.due_date
        old_name = task_to_edit.name
        if form.is_valid():
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
            task_to_edit.save()
            if task_to_edit.name != old_name:
                send_email_alternative(u"Изменёно название задачи: "+old_name,
                           u"Прежнее название:"+old_name+u"\nНовое название:"+task_to_edit.name+u"\nОписание задачи:\n"+task_to_edit.description+u"\nПосмотреть задачу можно тут:\nhttp://"+server_ip+"/task/one_time/"+str(task_to_edit.id),
                           [task_to_edit.worker.mail,task_to_edit.client.mail]+admins_mail,
                           fio
                           )
            if task_to_edit.worker != old_worker:
                # добавление нового исполнителя в acl
                if task_to_edit.worker.login not in task_to_edit.acl:
                    task_to_edit.acl=task_to_edit.acl+";"+task_to_edit.worker.login
                    task_to_edit.save()
                send_email_alternative(u"Изменён исполнитель задачи: "+task_to_edit.name,
                           u"Прежний исполнитель:"+old_worker.fio+u"\nНовый исполнитель:"+task_to_edit.worker.fio+u"\nОписание задачи:\n"+task_to_edit.description+u"\nПосмотреть задачу можно тут:\nhttp://"+server_ip+"/task/one_time/"+str(task_to_edit.id),
                           [task_to_edit.worker.mail,task_to_edit.client.mail,old_worker.mail]+admins_mail,
                           fio
                           )
            if task_to_edit.pbu != old_pbu:
                send_email_alternative(u"Изменёно описание проблемы со слов пользователя для задачи: "+task_to_edit.name,
                           u"Прежная проблема:"+old_pbu.name+u"\nНовая проблема:"+task_to_edit.pbu.name+u"\nОписание задачи:\n"+task_to_edit.description+u"\nПосмотреть задачу можно тут:\nhttp://"+server_ip+"/task/one_time/"+str(task_to_edit.id),
                           [task_to_edit.worker.mail,task_to_edit.client.mail]+admins_mail,
                           fio
                           )
            if task_to_edit.client != old_client:
                # добавление нового заказчика в acl
                if task_to_edit.client.login not in task_to_edit.acl:
                    task_to_edit.acl=task_to_edit.acl+";"+task_to_edit.client.login
                    task_to_edit.save()
                send_email_alternative(u"Изменён заказчик задачи: "+task_to_edit.name,
                           u"Прежний заказчик:"+old_client.fio+u"\nНовый заказчик:"+task_to_edit.client.fio+u"\nОписание задачи:\n"+task_to_edit.description+u"\nПосмотреть задачу можно тут:\nhttp://"+server_ip+"/task/one_time/"+str(task_to_edit.id),
                           [task_to_edit.worker.mail,task_to_edit.client.mail,old_client.mail]+admins_mail,
                           fio
                           )
            if task_to_edit.category != old_category:
                send_email_alternative(u"Изменёна категория задачи: "+task_to_edit.name,
                           u"Прежная категория:"+old_category.name+u"\nНовая категория:"+task_to_edit.category.name+u"\nОписание задачи:\n"+task_to_edit.description+u"\nПосмотреть задачу можно тут:\nhttp://"+server_ip+"/task/one_time/"+str(task_to_edit.id),
                           [task_to_edit.worker.mail,task_to_edit.client.mail]+admins_mail,
                           fio
                           )
            if task_to_edit.due_date != old_due_date:
                send_email_alternative(u"Изменён срок выполонения задачи: "+task_to_edit.name,
                           u"Старый срок:"+str(old_due_date)+u"\nНовый срок:"+str(task_to_edit.due_date)+u"\nОписание задачи:\n"+task_to_edit.description+u"\nПосмотреть задачу можно тут:\nhttp://"+server_ip+"/task/one_time/"+str(task_to_edit.id),
                           [task_to_edit.worker.mail,task_to_edit.client.mail]+admins_mail,
                           fio
                           )
            set_last_activity(user,request.path)
            return HttpResponseRedirect('/tasks/')
    else:
        form = TicketEditForm({'name' : task_to_edit.name,
            'pbus' : task_to_edit.pbu,
            'description' : task_to_edit.description,
            'clients' : task_to_edit.client,
            'priority' : task_to_edit.priority,
            'category' : task_to_edit.category,
            'start_date' : task_to_edit.start_date,
            'when_to_reminder' : task_to_edit.when_to_reminder,
            'due_date' : task_to_edit.due_date,
            'workers' : task_to_edit.worker,
            'percentage' : task_to_edit.percentage
        })
    set_last_activity(user,request.path)
    return render_to_response('new_ticket.html', {'form':form, 'method':method},RequestContext(request))
@login_required
def delete_task(request,task_type,task_to_delete_id):
    user = request.user.username
    task_to_delete = task_types[task_type].objects.get(id=task_to_delete_id)
    task_to_delete.deleted = True
    task_to_delete.save()
    set_last_activity(user,request.path)
    return HttpResponseRedirect('/tasks/')
@login_required
def undelete_task(request,task_type,task_id):
    task = task_types[task_type].objects.get(id=task_id)
    task.deleted = False
    task.save()
    set_last_activity(user,request.path)
    return HttpResponseRedirect('/tasks/')    
@login_required
def completle_delete_task(request,task_type,task_to_delete_id):
    user = request.user.username
    if user not in admins:
        return HttpResponseRedirect("/tasks/")
    task_to_delete = task_types[task_type].objects.get(id=task_to_delete_id)
    task_to_delete.delete()
    set_last_activity(user,request.path)
    return HttpResponseRedirect('/tasks/')
@login_required
def deleted_tasks(request):
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
    return render_to_response('deleted_tasks.html', {'tasks':tasks,},RequestContext(request))
def send_email(subject,message,to):
    good_mails=[mail for mail in to if mail!='']
    send_mail(subject,message,"meoc-it@mail.ru",good_mails)

@login_required
def all_tasks(request):
    user = request.user.username
    not_finded = False
    finded_tasks = False
    method = request.method
    if request.method == 'POST':
        form = TicketSearchForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            try:
                finded_tasks_names = Task.objects.filter(name__icontains = data['name'])
                finded_tasks_desc = Task.objects.filter(description__icontains = data['name'])
                finded_rtasks_names = RegularTask.objects.filter(name__icontains = data['name'])
                finded_rtasks_desc = RegularTask.objects.filter(description__icontains = data['name'])
                notes = Note.objects.filter(note__icontains = data['name'])
                for note in notes:
                    finded_tasks_notes = Task.objects.filter(note = note)
                    finded_rtasks_notes = RegularTask.objects.filter(note = note)
                finded_tasks = list(chain(finded_tasks_names, finded_tasks_desc, finded_rtasks_names,finded_rtasks_desc,finded_tasks_notes,finded_rtasks_notes))
                if not finded_tasks:
                    not_finded = True
            except:
                print 'exception'
                not_finded = True
            set_last_activity(user,request.path)
            return render_to_response('all_tasks.html', {'not_finded':not_finded,'finded_tasks':finded_tasks,'form':form, 'method':method},RequestContext(request))
    else:
        form = TicketSearchForm()
        if request.session.get('my_error'):
            my_error = [request.session.get('my_error'),]
        else:
            my_error=[]
        request.session['my_error'] = ''
        try:
            # отображаем все НЕ закрытые заявки, т.е. процент выполнения которых меньше 100
            tasks = Task.objects.filter(deleted = False).filter(percentage__lt=100)
        except:
            tasks = ''# если задач нет - вывести это в шаблон
        try:
            # отображаем все повторяющиеся задачи
            regular_tasks = RegularTask.objects.filter(deleted = False)
        except:
            regular_tasks = ''# если задач нет - вывести это в шаблон
        try:
            # отображаем все закрытые заявки не подтверждённые
            closed_tasks = Task.objects.filter(deleted = False).filter(percentage__exact=100).filter(confirmed__exact=False)
        except:
            closed_tasks = ''# если задач нет - вывести это в шаблон
            # my_error.append('Для Вас нет задач')
        try:
            # отображаем все подтверждённые заявки
            confirmed_tasks = Task.objects.filter(deleted = False).filter(confirmed__exact=True)
        except:
            confirmed_tasks = ''# если задач нет - вывести это в шаблон
    set_last_activity(user,request.path)
    return render_to_response('all_tasks.html', {'my_error':my_error,'tasks':tasks,'closed_tasks':closed_tasks,'confirmed_tasks':confirmed_tasks,'regular_tasks':regular_tasks,'form':form, 'method':method},RequestContext(request))
@login_required
def add_children_task(request,parent_task_type,parent_task_id):
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
            send_email(u"Новая подзадача: "+t.name+u" для задачи "+parent_task.name,t.description+u"\nПосмотреть подзадачу можно тут:\nhttp://"+server_ip+"/task/"+str(t.id)+u"\nПосмотреть задачу можно тут:\nhttp://"+server_ip+"/task/"+str(parent_task.id),[data['workers'].mail,])
            set_last_activity(user,request.path)
            return HttpResponseRedirect('/tasks/')
    else:
        form = NewTicketForm({'percentage':0,'start_date':datetime.datetime.now(),'due_date':datetime.datetime.now(),'priority':parent_task.priority,'category':parent_task.category})
    set_last_activity(user,request.path)
    return render_to_response('new_ticket.html', {'form':form, 'method':method},RequestContext(request))
@login_required
def regular_task_done(request,task_id):
    user = request.user.username
    method = request.method
    try:
        # находим задачу
        task = RegularTask.objects.get(id=task_id)
    except:
        my_error=request.session.get('my_error')# если задач нет - вывести это в шаблон
        my_error.append('Не найдена задача?!')
        return HttpResponseRedirect('/tasks/')
    task.next_date = generate_next_reminder(decronize(task.period), task.stop_date)
    task.when_to_reminder = task.next_date
    task.save()
    set_last_activity(user,request.path)
    return HttpResponseRedirect('/tasks/')

@login_required
def get_all_logged_in_users(request):
    user = request.user.username
    if user in admins:
        last_activities=get_last_activities()
        return render_to_response('logged_in_user_list.html', {'last_activities':last_activities,},RequestContext(request))
