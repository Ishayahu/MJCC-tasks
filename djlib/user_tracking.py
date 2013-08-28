# -*- coding:utf-8 -*-
# coding=<utf8>
from todoes.models import Activity, Person
import datetime

def set_last_activity_model(login,url,url_not_to_track=[],url_one_record=[]):
    """
    Сохраняем последную деятельность пользователя на сайте - что и когда
    Если url = /tasks/, то есть просто обновляется страница с заявками, чтобы не плодить мусор в БД просто обновляется последнее аналогичное посещение
    """
    if url not in url_not_to_track and url not in url_one_record:
        la = Activity()
        la.login = login
        la.last_page = url
        la.timestamp =datetime.datetime.now()
        la.save()
    elif url in url_one_record:
        try:
            la = Activity.objects.filter(login=login,last_page=url)[0]
        except (Activity.DoesNotExist,IndexError):
            la = Activity()
            la.login = login
            la.last_page = url
            la.timestamp =datetime.datetime.now()
            la.save()
        else:
            la.timestamp =datetime.datetime.now()
            la.save()
def get_last_activities():
    """
    Получаем список последних действий пользователей - когда и что
    """
    # получаем список пользователей
    users = Person.objects.all()
    # для каждого пользователя получаем его последний url и дату и добавляем их в возвращаемый [] и давно ли это было
    # первый элемент равен True, если последнее событие было в пределах последних 15 минут
    last_activities=[]
    for user in users:
        try:
            la = Activity.objects.filter(login=user.login)[0]
            last_activities.append((la.timestamp >= datetime.datetime.now() - datetime.timedelta(minutes=15) ,user.fio, la.last_page, la.timestamp))
        except IndexError:
            pass
    return last_activities