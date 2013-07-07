# -*- coding:utf-8 -*-
# coding=<utf8>

import datetime
# import logging
# from assets.models import Logging
# from todoes.models import Person
from logs.models import Logging

def log(user,message,sql_request):
    log = Logging(  user = user,
                    goal = message,
                    request = sql_request)
    log.save()
    return log.id
def confirm_log(id):
    log = Logging.objects.get(id=id)
    log.done = True
    log.save()
    return True
def make_request_with_logging(user,message,sql_request,sql_request_params):
    log = Logging(  user = user,
                    goal = message,
                    datetime = datetime.datetime.now())
    log.save()
    result = sql_request(**sql_request_params)
    try:
        log.request = str(result.query)
    except AttributeError:
        pass
    log.done = True
    log.save()
    return result
    
    