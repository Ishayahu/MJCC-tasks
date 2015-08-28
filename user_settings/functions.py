# -*- coding:utf-8 -*-
# coding=<utf8>

from user_settings.settings import config_file
import ConfigParser

class Option():
    def __init__(self,
                 section,
                 option,
                 opt_id,
                 val,
                 name,
                 desc,
                 help_message,
                 from_bd,
                 option_type = 'TEXT'):
        self.section = section
        self.option = option
        if option_type in ("CONNECT","CHECKBOX"):
            if val=='True':
                self.value = True
            else:
                self.value = False

        else:
            self.value = val
        self.name = name
        self.description = desc
        self.help_message = help_message
        try:
            self.html_value = unicode(val).replace(u'\n',u'<p>')
        except UnicodeDecodeError:
            self.html_value = val.replace('\n','<p>')
        self.from_bd = from_bd
        self.id = opt_id
        self.option_type = option_type
def get_section_description(section):
    config=ConfigParser.RawConfigParser()
    config.read(config_file)
    desc = config.get(section,"section_description")
    return desc
def get_stages(separator):
    config=ConfigParser.RawConfigParser()
    config.read(config_file)
    if separator:
        stages = separator.join(config.get('cashless','stages').split(';'))
    else:
        # stages = [a[1] for a in config.items("cashless")]
        stages = config.get('cashless','stages')
    return stages
def get_full_option(section,option):
    config=ConfigParser.RawConfigParser()
    config.read(config_file)
    try:
        val = config.get(section,option)
    except:
        return None
        # return Option(section,option, None,'','','','',0)
    desc = config.get(section,option+"_description")
    name = config.get(section,option+"_name")
    help_message = None
    try:
        help_message = config.get(section,option+"_help")   
    except ConfigParser.NoOptionError:
        pass
    return Option(section,option, None,val,name,desc,help_message,0)
def get_full_section(section):
    res = []
    config=ConfigParser.RawConfigParser()
    config.read(config_file)
    for option in config.items(section):
        option = option[0]
        if option.split('_')[-1] in ('name',
                                     'description'):
            continue
        val = config.get(section,option)
        desc = config.get(section,option+"_description")
        name = config.get(section,option+"_name")
        help_message = None
        try:
            help_message = config.get(section,option+"_help")
        except ConfigParser.NoOptionError:
            pass
        res.append(Option(section,
                          option,
                          None,
                          val,
                          name,
                          desc,
                          help_message,
                          0))
    return res
def get_full_bd_option(section,option):
    config=ConfigParser.RawConfigParser()
    config.read(config_file)
    app_name = config.get(section,"__bd__app__"+option)
    model_name = config.get(section,"__bd__model__"+option)
    field_name = config.get(section,"__bd__field__"+option)
    id = config.get(section,"__bd__option__"+option)
    
    app_module_name = app_name+'.models'
    app_module = __import__(app_module_name)
    models_module = getattr(app_module,'models')
    model = getattr(models_module,model_name)
    try:
        opt = model.objects.get(id=id)
        opt_val = getattr(opt,field_name)
    except:
        opt_val = u"Не существует в БД"
    
    name = config.get(section,"__bd__name__"+option)
    opt_id = config.get(section,"__bd__option__"+option)
    desc = config.get(section,"__bd__description__"+option)
    help_message = None
    try:
        help_message = config.get(section,"__bd__help__"+option)   
    except ConfigParser.NoOptionError:
        pass
    return Option(section,option,opt_id,opt_val,name,desc,help_message,1)
def get_bd_option_variants(section,option):
    # __bd__name__default_place = Место по умолчанию
    # __bd__option__default_place = 1
    # __bd__app__default_place = assets
    # __bd__model__default_place = Place
    # __bd__field__default_place = place
    # __bd__description__default_place = Место, которое выставляется по умолчанию для нового актива при создании счёта
    class Option():
        def __init__(self,id,val):
            self.id = id
            self.val = val
    config=ConfigParser.RawConfigParser()
    config.read(config_file)
    app_name = config.get(section,"__bd__app__"+option)
    model_name = config.get(section,"__bd__model__"+option)
    field_name = config.get(section,"__bd__field__"+option)
    id = config.get(section,"__bd__option__"+option)
    
    app_module_name = app_name+'.models'
    app_module = __import__(app_module_name)
    models_module = getattr(app_module,'models')
    model = getattr(models_module,model_name)
    opts_intances = model.objects.all()
    opts = []
    for opt in opts_intances:
        opts.append(Option(opt.id,getattr(opt,field_name)))
    return opts