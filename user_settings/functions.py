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