# -*- coding:utf-8 -*-
# coding=<utf8>

from user_settings.settings import config_file
import ConfigParser

def get_stages(separator):
    config=ConfigParser.RawConfigParser()
    config.read(config_file)
    if separator:
        stages = separator.join(config.get('cashless','stages').split(';'))
    else:
        # stages = [a[1] for a in config.items("cashless")]
        stages = config.get('cashless','stages')
    return stages
def get_option_with_description(section,option):
    config=ConfigParser.RawConfigParser()
    config.read(config_file)
    opt = config.get(section,option)
    desc = config.get(section,option+"_description")
    return opt,desc
def get_bd_option_with_description(section,option):
    # __bd__name__default_place = Место по умолчанию
    # __bd__option__default_place = 1
    # __bd__app__default_place = assets
    # __bd__model__default_place = Place
    # __bd__field__default_place = place
    # __bd__description__default_place = Место, которое выставляется по умолчанию для нового актива при создании счёта
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
    opt = model.objects.get(id=id)
    
    name = config.get(section,"__bd__name__"+option)
    opt_id = config.get(section,"__bd__option__"+option)
    opt_val = getattr(opt,config.get(section,"__bd__field__"+option))
    desc = config.get(section,"__bd__description__"+option)

    return name,opt_id,opt_val,desc
def get_option_description(section,option):
    config=ConfigParser.RawConfigParser()
    config.read(config_file)
    desc = config.get(section,option+"_description")
    return desc
def get_section_description(section):
    config=ConfigParser.RawConfigParser()
    config.read(config_file)
    desc = config.get(section,"section_description")
    return desc