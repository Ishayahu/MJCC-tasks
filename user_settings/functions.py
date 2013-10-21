def get_stages(separator):
    fn=r"user_settings/config.txt"
    import ConfigParser
    config=ConfigParser.RawConfigParser()
    config.read(fn)
    if separator:
        stages = separator.join([a[1] for a in config.items("cashless_stages")])
    else:
        stages = [a[1] for a in config.items("cashless_stages")]
    return stages