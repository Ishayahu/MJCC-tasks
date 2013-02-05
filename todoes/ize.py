# -*- coding:utf-8 -*-
# coding=<utf8>
# testing git
import datetime, re
def decronize(fstring):
    minute,hour,day,month,wday = fstring.split('\t')
    def get_interval(fstr,min,max):
        # max - предел интервала:
        # минута
        # * или 0-59
        # час
        # * или 0-23
        # число
        # * или 1-31
        # месяц
        # *, 1-12 или имя месяца (см. ниже)
        # день-недели
        # *, 0-7 или имя дня (воскресенье - это 0 и 7)
        max+=1
        # если любой интервал
        if fstr[0]=='*':
            # совсем любой * - от 0 до 59
            if len(fstr)==1:
                return list(range(0,max))
            # любой, но с интервалом */2 - каждые два часа
            elif len(fstr)>1:
                return list(range(0,max,int(fstr[2:])))
        # если перечисление интервала
        elif ',' in fstr:
            return list(map(int,fstr.split(',')))
        # если интервал
        elif '-' in fstr:
            # если интервал с периодом 2-15/2
            if '/' in fstr:
                interval = int(fstr.split('/')[1])
                start,end = list(map(int,fstr.split('/')[0].split('-')))
                return list(range(start,end,interval))
            # если интервал просто 2-15
            else:
                start,end = list(map(int,fstr.split('-')))
                return list(range(start,end))
        else:
            return (int(fstr),)
    minute = get_interval(minute,0,59)
    hour = get_interval(hour,0,23)
    month = get_interval(month,1,12)
    if (day !='*' and wday !='*') or (day =='*' and wday =='*'):
        day = get_interval(day,1,31)
        wday = get_interval(wday,0,6)
    elif day=='*' and wday != '*':
        day = list()
        wday = get_interval(wday,0,6)
    elif day != '*' and wday=='*':
        day = get_interval(day,1,31)
        wday = list()
    return {'minute':minute,'hour':hour,'day':day,'month':month,'wday':wday}
    
def crontab_to_russian(fstr):
    result = u'В {hour[0]} часов {minute[0]} минут каждый {day} день месяца или каждый {wday} день недели в месяцах {month}'.format(**decronize(fstr))
    return result
    
def generate_next_reminder(ranges, stop_date):
    print ranges
    minute = datetime.datetime.now().minute
    hour = datetime.datetime.now().hour
    day = datetime.datetime.now().day
    month = datetime.datetime.now().month
    wday = datetime.datetime.now().weekday()
    year = datetime.datetime.now().year
    crit_dict = {'month':month,'day':day,'hour':hour,'minute':minute,'wday':wday}
    crit_max = {'month':13,'day':32,'hour':24,'minute':60,'wday':7}
    crit_min = {'month':1,'day':1,'hour':0,'minute':0,'wday':0}
    to_next = False
    for criteria in ('minute','hour','day','month'):
        if criteria != 'day':
            # if criteria == 'month':
                # print crit_dict
                # print to_next
            if to_next:
                crit_dict[criteria] += 1
                to_next = False
                if crit_dict[criteria] == crit_max[criteria]:
                    crit_dict[criteria] = crit_min[criteria]
                    to_next = True
            while True: #crit_dict[criteria] <= crit_max[criteria]:
                if crit_dict[criteria] in ranges[criteria]:
                    break
                crit_dict[criteria] +=1
                if crit_dict[criteria] >= crit_max[criteria]:
                    crit_dict[criteria] = crit_min[criteria]
                    to_next = True
        else:
            if to_next:
                print 'here'
                crit_dict['day'] += 1
                crit_dict['wday'] += 1
                if crit_dict['wday'] == 7:
                    crit_dict['wday'] = 1
                to_next = False
            while True: # crit_dict['day'] <= crit_max['day'] and crit_dict['wday'] <= crit_max['wday']:
                print crit_dict
                if crit_dict['day'] in ranges['day'] or  crit_dict['wday'] in ranges['wday']:
                    break
                crit_dict['day'] += 1
                crit_dict['wday'] += 1
                if crit_dict['day'] >= crit_max['day']:
                    crit_dict['day'] = crit_min['day']
                    to_next = True
                if crit_dict['wday'] >= crit_max['wday']:
                    crit_dict['wday'] = crit_min['wday']
                    # to_next = True
    if to_next:
        year += 1
    next_reminder = datetime.datetime(year,crit_dict['month'],crit_dict['day'],crit_dict['hour'],crit_dict['minute'])
    # return crit_dict['minute'],crit_dict['hour'],crit_dict['day'],crit_dict['month'],crit_dict['wday']
    if stop_date and next_reminder > stop_date:
        return False
    return next_reminder
    
def htmlize(str=''):
    # print 'in htmlize',str.encode('koi8-r')
    links = re.findall(r'https?://\S*',str)
    # links += re.findall(r'https://\S*',str)       
    html = ''
    inBold = False
    inItalic = False
    tegs = {True:'</', False:'<'}
    count = 0
    while count < len(str):
        if str[count] == '\n':
            html += '<br />'
        elif str[count] == '*' and count+1<len(str) and str[count+1] != '*':
            html = html + tegs[inBold] + 'b>'
            inBold = not inBold
        elif str[count] == '*' and count+1<len(str) and str[count+1] == '*':
            html = html + tegs[inItalic] + 'i>'
            count +=1
            inItalic = not inItalic
        elif str[count] == '*' and inBold:
            html = html + '</b>'
        elif str[count] == '\\':
            html += str[count+1]
            count += 1
        elif str[count] == '<':
            html += '&lt'
            # count +=1
        elif str[count] == '>':
            html += '&gt'
            count +=1
        elif str[count] == '&':
            html += '&amp'
            # count +=1
        else:
            html += str[count]
        count +=1
    for link in links:
        html = html.replace(link.replace('&','&amp'),'<a href='+link+'>'+link+'</a>')
    return html
