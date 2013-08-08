from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext

languages={'ru':'RUS/',
            }
# l_forms = {'ru':forms_RUS,          
    # }
def select_language(request):
    if request.session.get('language'):
        lang = request.session.get('language')
    else:
        lang='ru'
    return lang
@login_required    
def change_language(request,lang):
    request.session['language']=lang
    return HttpResponseRedirect('/')
def register_lang(code,prefics):
    global languages
    languages[code]=prefics
# def register_app(app_name):
    # global app
    # app=app_name
def get_localized_name(name,request):
    lang=select_language(request)
    return languages[lang]+'/'+name
def get_localized_form(name,app,request):
    lang=select_language(request)
    app_module_name = app+'.'+'forms_'+languages[lang].lower()
    forms_module_name = 'forms_'+languages[lang].lower()
    app_module = __import__(app_module_name)
    forms_module = getattr(app_module,forms_module_name)
    return getattr(forms_module,name)
def multilanguage(fn):
    """
     Декоратор для того, чтобы сделать функцию многоязычной. Определяет язык сессии, заменяет соответстующие формы и шаблоны на локализованные аналоги
     Пока единственный недостаток - если форма нужна внутри функции для обработки данных. Видимо это должно решаться дополнительным вызовом вспомогательной функции
     Пример того, что должна возвращать функция, которую декорируют:
     return (decorate_or_not,('all_bills.html',{'form_name':(form_param1,form_param2),},{'cashs':cashs, 'cashlesss':cashlesss},request,app))
    """
    def wrapped(*args,**kwargs):
        # print "in multilanguage for "+str(args[0].path)+" calling function, my_error:"+str(args[0].session['my_error'])
        decorate_or_not, result = fn(*args,**kwargs)
        if not decorate_or_not:
            return result
        template,forms_dict,dict,request,app=result
        # print "after calling for "+str(args[0].path)+" in multilanguage: "+str(request.session['my_error'])
        # dict.update(request.session.get('to_dict'))
        # request.session.get('to_dict')=''
        # dict['my_error'] = request.session.get('my_error')
        # dict['admin'] = request.session.get('admin')
        # request.session.get('admin')=False
        # request.session.get('my_error')=[]
        lang=select_language(request)
        l_template=languages[lang]+'/'+template
        forms={}
        # a=__name__
        # b=__package__
        app_module_name = app+'.'+'forms_'+languages[lang].lower()
        forms_module_name = 'forms_'+languages[lang].lower()
        app_module = __import__(app_module_name)
        forms_module = getattr(app_module,forms_module_name)
        # a=dir(app_module)
        # forms_module=getattr(app_module,'forms_'+languages[lang].lower())
        for form in forms_dict:
            a=getattr(forms_module,form)            
            # forms[form]=(a(**forms_dict[form]))
            # print form, forms_dict[form]
            forms[form]=(a(**forms_dict[form]))
        dict.update(forms)
        # raise ImportError
        # print l_template
        # print dict
        # print "in multilanguage for "+str(args[0].path)+" before return dict="+str(dict)
        return render_to_response(l_template, dict,RequestContext(request)) 
    return wrapped