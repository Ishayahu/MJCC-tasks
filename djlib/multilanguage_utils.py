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