# -*- coding:utf-8 -*-
# coding=<utf8>

class FioError():
    def __init__(self):
        self.mail=''
        self.message='Нет такого пользователя'
    def __str__(self):
        return self.message
class ErrorMessage():
    def __init__(self,message):
        self.message='Нет такого пользователя'
    def __str__(self):
        return self.message
def add_error(message,request):
    # print "adding error in add_error for "+request.path
    if 'my_error' not in request.session:
        # print "my_error not in session"
        request.session['my_error']=[]
    if type(request.session['my_error'])!=list:
        if request.session['my_error']:
            # print "addin new error to old one"
            tmp=request.session['my_error']
            request.session['my_error']=[]
            request.session['my_error'].append(tmp)
        else:
            request.session['my_error']=[]
    request.session['my_error'].append(message)
    # print "error in "+request.path+" appended: "+str(request.session['my_error'])
def shows_errors(fn):
    """
     Декоратор для того, чтобы добавить ошибки в словарь для отображения. 
    """
    def wrapped(*args,**kwargs):
        # print "in shows_errors "+str(args[0].path)+" before calling function"
        # a=fn(*args,**kwargs)
        # print a
        # raise TabError
        decorate_or_not, result = fn(*args,**kwargs)
        # raise TypeError
        if not decorate_or_not:
            return decorate_or_not, result
        template,forms_dict,dict,request,app=result
        if 'my_error' in request.session:
            # print "adding error to dict"
            dict['my_error']=request.session['my_error']
            request.session['my_error']=[]
        # raise ImportError
        # print "in shows_error "+str(request.path)+" before return dict="+str(dict)
        return decorate_or_not, (template,forms_dict,dict,request,app)
    return wrapped