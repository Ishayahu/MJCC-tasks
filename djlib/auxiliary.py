# out=open("catalogue.py.new",'w')
# for line in open("catalogue.py",'r'):
    # if '[' in line and ']' in line:
        # to_parse=line[line.index('[')+1:line.index(']')]
        # start_line=line[:line.index('[')]
        # to_write=start_line+'('+[(record.strip()[1:-1],record.strip()[1:-1]) for record in to_parse.split(',')].__str__()[1:-1]+')\n'
        # out.write(to_write)
    # else:
        # out.write(line)
# out.close()
from djlib.error_utils import FioError
from djlib.multilanguage_utils import select_language
from todoes.models import  Person 

def get_info(request):
    lang=select_language(request)
    user = request.user.username
    try:
        fio = Person.objects.get(login=user)
    except Person.DoesNotExist:
        fio = FioError()
    method = request.method
    return lang,user,fio,method