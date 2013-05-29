# -*- coding:utf-8 -*-
# coding=<utf8>

import datetime, re

def htmlize(str=''):
    # print 'in htmlize',str.encode('koi8-r')
    links = re.findall(r'https?://\S*',str)
    # links += re.findall(r'https://\S*',str)       
    html = ''
    # заменяем \r\n на \n для более простой обработки построения страницы. На выводе это никак не сказывается
    str = str.replace('\r\n','\n')
    inBold = False
    inItalic = False
    # для таблицы
    inTable = False
    inRow = False
    inCell = False
    tegs = {True:'</', False:'<'}
    count = 0
    while count < len(str):
        if str[count] == '\n' and not inTable:
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
        elif str[count] == '\\' and count+1==len(str):
            html += '\\'
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
        # обработка создания таблиц
        elif count+3<len(str) and str[count]=='|' and str[count+1]=='|':
            # обрабатываем создание начала таблицы
            if (str[count-1]=='\n' or count-1<0) and not inTable:
                html += '<table border="1"><tr><td>'
                inTable = True
                inRow = True
                inCell = True
            elif inTable and not inRow:
                html += '<tr><td>'
                inRow = True
                inCell = True
            elif inCell:
                if str[count+2]!='\n':
                    html+='</td><td>'
                    inCell = True
                if str[count+2] == '\n':
                    html+='</td></tr>'
                    inCell = False
                    inRow=False
                    count+1
                    if str[count+3]!='|':
                        html+='</table>'
                        inTable=False
            count+=1
        elif (count+2>=len(str) and inTable) or (count+3<len(str) and str[count+2]=='\n' and inTable and str[count+3]!='|'):
            if inCell:
                html += '</td>'
                inCell = False
            if inRow:
                html += '</tr>'
                inRow = False
            html+='</table>'
            inTable = False
            count+=1
            
        else:
            html += str[count]
        count +=1
    for link in links:
        html = html.replace(link.replace('&','&amp'),'<a href='+link+'>'+link+'</a>')
    return html
