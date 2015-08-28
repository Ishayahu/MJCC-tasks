#!/usr/local/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2014 LasSil by Ishayahu Lastov
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""
Command-line skeleton application for Drive API.
Usage:
  $ python sample.py

You can also get help on all the command-line flags the program
understands by running:

  $ python sample.py --help

To get detailed log output run:

  $ python sample.py --logging_level=DEBUG
  
Для работы надо поставить gdata:
  
  $ pip install gdata
  $ pip install pyquery
  
Подключение API:

  https://developers.google.com/drive/quickstart-python
  
  Коды возврата команды
  1 - Если вовзращённый гуглом файл пустой
  2 - Если новый файл не отличается от старого
"""

from __future__ import print_function
BACKUP = False # делать ли бакуп старых файлов

# Импортируем всё, что надо
# Переменная, которая хранит код кода завершения для словаря
# exit_code_key = 0
# Словарь кодов завершения
exit_code_dict = {'ok':0,
                  'google_args_error':1,
                  'dhcp_files_were_not_replaced':2,
                  'google_returned_empty_file':3,
                  'import_error':10,
                  }

import argparse
import sys
import zipfile
import re
import os
import csv
try:
    from pyquery import PyQuery as pq
except ImportError:
    print ("pyquery not installed."
            "see http://www.freshports.org/www/py-pyquery/")
    sys.exit(exit_code_dict['import_error'])
from lxml.cssselect import CSSSelector
from StringIO import StringIO
import smtplib
from email.MIMEText import MIMEText
from email.MIMEMultipart import  MIMEMultipart
try:
    import gflags
except ImportError:
    print ("gflags not installed."
           "see http://www.freshports.org/devel/py-gflags/")
    sys.exit(exit_code_dict['import_error'])

import httplib2
import logging
import datetime
import pprint
import os,sys
import re

from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import AccessTokenRefreshError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.tools import run
from apiclient import errors


def print_to_stderr(string):
    print(string, file=sys.stderr)


def retrieve_all_files(service):
  """Retrieve a list of File resources.

  Args:
    service: Drive API service instance.
  Returns:
    List of File resources.
  """
  result = []
  page_token = None
  while True:
    try:
      param = {}
      if page_token:
        param['pageToken'] = page_token
      files = service.files().list(**param).execute()

      result.extend(files['items'])
      page_token = files.get('nextPageToken')
      if not page_token:
        break
    except errors.HttpError, error:
      print ('An error occurred: %s' % error)
      break
  return result

def download_file(service, drive_file):
  """Download a file's content.

  Args:
    service: Drive API service instance.
    drive_file: Drive File instance.

  Returns:
    File's content if successful, None otherwise.
  """
  download_url = drive_file[u'exportLinks'][u'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet']
  # https://docs.google.com/spreadsheets/export?id=1B-OeCz6zAbZToSuSgN21u7vvdNjTZPxPEpcVzl1LBcY&exportFormat=xlsx
  # xlsx shold be changed to ods
  download_url = download_url.replace('xlsx','ods')

  if download_url:
    resp, content = service._http.request(download_url)
    if resp.status == 200:
      return content
    else:
      print ('An error occurred: %s' % resp)
      return None
  else:
    # The file doesn't have any content stored on Drive.
    return None

def ods2csv(content,admins=''):  

  file_like_object = StringIO(content)

  xml = zipfile.ZipFile(file_like_object).read('content.xml')  
    
  def rep_repl(match):  
    return '<table:table-cell>%s' %match.group(2) * int(match.group(1))  
  def repl_empt(match):  
    n = int(match.group(1))  
    pat = '<table:table-cell/>'  
    return pat*n if (n<100) else pat  
      
  p_repl = re.compile(r'<table:table-cell [^>]*?repeated="(\d+)[^/>]*>(.+?table-cell>)')  
  p_empt = re.compile(r'<table:table-cell [^>]*?repeated="(\d+)[^>]*>')  
  xml = re.sub(p_repl, rep_repl, xml)  
  xml = re.sub(p_empt, repl_empt, xml)  
      
  d = pq(xml, parser='xml')  
  ns={'table': 'urn:oasis:names:tc:opendocument:xmlns:table:1.0'}  
  selr = CSSSelector('table|table-row', namespaces=ns)  
  selc = CSSSelector('table|table-cell', namespaces=ns)  
  rowxs = pq(selr(d[0]))  
  data = []  
  for ir,rowx in enumerate(rowxs):  
    cells = pq(selc(rowx))  
    if cells.text():  
      data.append([cells.eq(ic).text().encode('utf-8') for ic in range(len(cells))])  
  if data:
    return data
  else:
    logger_script=logging.getLogger("Script Error")
    logger_script.warning("Google retuned empty file for table <b>%s</b>" % IP_table_name)
    sending_log("DHCP_ERROR: script got an error","<b>Google returned empty file</b>, script ended without any changes made!",error_log_file_name=error_log_file_name,admins=admins)
    sys.exit(exit_code_dict['google_returned_empty_file'])
      
def replacing_file(datas, error_log_file_name='',
                   admins='', out_file_fn='',templates={} ,test=False, compare_with_old = True):
    message = ""
    # not_replaced_at_all = False

    # сравнивать или нет -  compare_with_old
    if compare_with_old:
        datas.sort()
        new_set=set(datas)
        iteration_set=set(datas)
        try:
            old_set=set(open(out_file_fn,'r').readlines())
            old_records = len(old_set)
        except (OSError,IOError):
            old_set=set()
        if not 0.67<len(old_set)/len(new_set)<1.5:
            message = "<b>Difference between new and old files is too big. Please check if all is correct!</b><br />"
        for record in iteration_set:
            if record in old_set:
                old_set.remove(record)
                new_set.remove(record)
        if not old_set and not new_set:
            # not_replaced_at_all = True
            message=message+"<br />Old file "+out_file_fn+" was not replaced becouse it has now new content<br />"
            sending_log("SCRIPT_OK:File was not replaced",message,error_log_file_name=error_log_file_name,admins=admins)
            return
        else:
            if old_set:
                message += "<br /><br />That records was in old dhcp file but there are no in new file:<br /><ol>"
                for record in old_set:
                    message = message +"<li>" +record + "</li>"
                message = message + "</ol>"
            if new_set:
                message = message + "<br /><br />That records are in new dhcp file but there was not in old file:<br />"
                for record in new_set:
                    message = message+"<li>" + record + "</li>"
                message = message + "</ol>"

    # если out_file_fn пустой - вывод в stdout
    if out_file_fn:
        if BACKUP:
            try:
                os.rename(out_file_fn,out_file_fn+'.'+datetime.datetime.now().__str__()[:-7].replace(':','-')+'.bak')
            except (IOError,OSError) as e:
                message=message+"<br /><b>Old file "+out_file_fn+" was not renamed because following error:<br />I/O error(<i>{0}</i>): <i>{1}</i></b><br />".format(e.errno, e.strerror)
        out_file = open(out_file_fn,'w')
        write_out = lambda x: out_file.write(x+'\n')
    else:
        write_out = lambda x: print(x)
    # пишем данные    
    write_out(templates['header'])
    for line in datas:
        write_out(line.strip())
    # raise NotImplementedError ('footer')
    if out_file_fn:
        write_out(templates['footer'])
    print_to_stderr("File "+out_file_fn+" was created")





    # not_replaced_at_all = False
    # datas.sort()
    # new_set=set(datas)
    # iteration_set=set(datas)
    # if compare_with_old:
        # try:
            # old_set=set(open(out_file_fn,'r').readlines())
            # old_records = len(old_set)
        # except (OSError,IOError):
            # old_set=set()
    # message = ""
    
    # if not 0.67<len(old_set)/len(new_set)<1.5:
        # message = "<b>Difference between new and old files is too big. Please check if all is correct!</b><br />"

    # for record in iteration_set:
        # if record in old_set:
            # old_set.remove(record)
            # new_set.remove(record)
    # # Если нет разницы в файлах - оба множества пусты
    # if not old_set and not new_set:
        # not_replaced_at_all = True
        # message=message+"<br />Old file "+out_file_fn+" was not replaced becouse it has now new content<br />"
    
    # else:
        # записываем в лог отличия в файлах -- и ++ и потом посылаем. После чего перезаписываем файлы
        # try:
            # os.rename(out_file_fn,out_file_fn+'.'+datetime.datetime.now().__str__()[:-7].replace(':','-')+'.bak')
        # except (IOError,OSError) as e:
            # message=message+"<br /><b>Old file "+out_file_fn+" was not renamed because following error:<br />I/O error(<i>{0}</i>): <i>{1}</i></b><br />".format(e.errno, e.strerror)
        # if out_file_fn:
            # out_file = open(out_file_fn,'w')
            # #raise NotImplementedError ('header')
            # out_file.write(templates['header']+'\n')
        # else:
            # print(templates['header'])
        # for line in iteration_set:
        # for line in datas:
            # if out_file_fn:
                # out_file.write(line.strip()+'\n')
            # else:
                # print(line.strip())
        # # raise NotImplementedError ('footer')
        # if out_file_fn:
            # out_file.write(templates['footer'])
            # out_file.close()
        # else:
            # print(templates['footer'])
        # print_to_stderr("File "+out_file_fn+" was created")
        # if old_set:
            # message += "<br /><br />That records was in old dhcp file but there are no in new file:<br /><ol>"
            # for record in old_set:
                # message = message +"<li>" +record + "</li>"
            # message = message + "</ol>"
        # if new_set:
            # message = message + "<br /><br />That records are in new dhcp file but there was not in old file:<br />"
            # for record in new_set:
                # message = message+"<li>" + record + "</li>"
            # message = message + "</ol>"
    sending_log("SCRIPT_OK:File was succefull replaced",message,error_log_file_name=error_log_file_name,admins=admins)
    message = ''
def sending_log(header,message,error_log_file_name,admins=''):
    if admins:
        log = open(error_log_file_name,'r').readlines()
        if log:
            # message = message + "<br /><br /><b>Entries of the log</b>:<br /><ol>"
            # for line in log:
                # message = message+'<li>'+line
            # message = message + "</ol>"
            message = message + "<br /><br /><b>Entries of the log</b>:<br /><table border='1'>"
            for line in log:
                message = message+'<tr><td>'+line.replace(';','</td><td>')+'</td></tr>'
            message = message + "</table>"
            send_email(header,message,admins)
        else:
            send_email(header,message,admins)
def send_email(subject,message,reciver):
    from_email = "ishayahu@gmail.com"

    server = "smtp.gmail.com"
    port = "25"
    user_name = "onlyforscripts13@gmail.com"
    user_passwd = '264eba9a86c5e3107310ae07757bdc2b'


    # формирование сообщения
    msg = MIMEMultipart('mixed')
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = ', '.join(reciver)
    
    # Формируем письмо
    part1 = MIMEText(message, 'html','utf-8')
    msg.attach(part1)
    
    # отправка
    s = smtplib.SMTP(server, port)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login(user_name, user_passwd)
    s.sendmail(from_email, msg['To'], msg.as_string())
    s.quit()
def main(IP_table_name='',test=False,
         run_first=True,admins='',templates={}):
    """
    если test = True (определён только в аргументах main, нигде больше),
    то вместо аналогичных аргументов командной строки используются
    аргументы функции нужно для тестирования
    """
    if test:
        print("RUNNING IN TEST MODE LINE 277 aprox")
        print_to_stderr("RUNNING IN TEST MODE LINE 277 aprox")
    def csv2files(data,debug = False):
        # logger_mac=logging.getLogger("Wrong MAC")
        if debug:
            print("IN DEBUG MODE ON LINE 469 aprox")
            print_to_stderr("IN DEBUG MODE ON LINE 469 aprox")
            open('debug.data.dat','w').write(str(data))
        datas = []
        first = True
        column_names = []
        for line in data:
            # Получаем из первой строки названия столбцов:
            if first:
                for col in line:
                    column_names.append(col)
                first = False
                continue
            # Создаём временный словарик для записи
            # print (column_names)
            tmp_dict = dict()
            for i,col_name in enumerate(column_names):
                # tmp_dict[col_name] = line[i]
                try:
                    tmp_dict[col_name] = line[i]
                except IndexError:
                    print (str(line))
                    print (i)
                    exit(99)
            # Создаём список записей для файла
            datas.append(templates['record'].format(tmp_dict))
        if script_debug:
            for x in datas:
                print (len(datas[x]))
        if debug:
            print("IN DEBUG MODE ON LINE 319 aprox")
            print_to_stderr("IN DEBUG MODE ON LINE 319 aprox")
            open('debug.datas.dat','w').write(str(datas))
        return datas


    # region ARGUMENTS_DEFINITION
    parser = argparse.ArgumentParser(description='Converting datas from google "IP range" table to dhcp.conf file. It use only that records, that have MAC address in table.')
    parser.add_argument("-g", "--gdrive_path",help="path to drive library catalog, by default - working dir",default='.')
    parser.add_argument("--IP_table_name",help="Name of table from Google Docs, by default - IP range",default='IP range')
    parser.add_argument("-f","--template_fn",help="File with template for output file. see example in ip-pc.template.txt string - template, by default - ip-pc.template.txt", default='ip-pc.template.txt')
    parser.add_argument("-o","--file_name",help="Output filename, by default - file.out", default='')
    parser.add_argument("--compare_with_old",help="Compare output with old file", action='store_true')
    parser.add_argument("-e", "--error_log",help="full path to error_log file, by default - ./error.log",default='error.log')
    parser.add_argument("-m", "--mails",help="mails to send logs and alerts",default='meoc-it@mail.ru')#;karpion@rambler.ru')
    parser.add_argument("--script_debug",help="verbouse output for debug",action='store_true')
    parser.add_argument("-c", "--client_secrets",help="full path to client_secrets.json file. If there aren't -c key and there is -g key, path to client_secrets.json construct from -g path and client_secrets.json filename. If there aren't -g and -c keys script use file ./client_secrets.json")
    parser.add_argument("--sample_dat",help="full path to sample.dat file with credentials. If there aren't --sample_dat key and there is -g key, path to sample.dat construct from -g path and sample.dat filename. If there aren't -g and -c keys script use file ./sample.dat")
    parser.add_argument("--noauth_local_webserver",help="option for google.script",action='store_true')
    args = parser.parse_args()
    # endregion


    sys.path.insert(0,args.gdrive_path)
    error_log_file_name = args.error_log
    script_debug = args.script_debug
    
    # Если вывод в файл - то вообще можно сравнивать, иначе - не с чем
    if args.file_name:
        compare_with_old = args.compare_with_old
    else:
        compare_with_old = False


    # region TEMPLATE_FILE_PROCESSING
    # получаем шаблоны для заголовка, конца и записей
    try:
        template = open(args.template_fn).read()
    except IOError:
        print ("file "+args.template_fn+" not found. You have to specify path to that file with option --template")
        sys.exit(exit_code_dict['import_error'])
    if not template:
        print ("File "+args.template_fn+" doesn't content template and is empty! Specify correct path to template file with option --template")
        sys.exit(exit_code_dict['import_error'])

    try:
        template_header=re.search(r'{%\s*header\s*%}\n?(\n*(.|\n)*\n*)\n{%\s*endheader\s*%}',
                              template).groups()[0]
    except AttributeError:
        print("Error by parsing header in template file {0}. Header set as empty string".format(args.template_fn))
        template_header = ''

    try:
        template_record=re.search(r'{%\s*record\s*%}\n?(\n*(.|\n)*\n*)\n{%\s*endrecord\s*%}',
                              template).groups()[0]
    except AttributeError:
        print("Error by parsing record in template file {0}. Record set as empty string".format(args.template_fn))
        template_record = ''

    try:
        template_footer=re.search(r'{%\s*footer\s*%}\n?(\n*(.|\n)*\n*)\n{%\s*endfooter\s*%}',
                              template).groups()[0]
    except AttributeError:
        print("Error by parsing footer in template file {0}. Footer set as empty string".format(args.template_fn))
        template_footer = ''
        
    templates = {'header':'' or template_header,
                 'record':'' or template_record,
                'footer':'' or template_footer}
    # endregion



    if not test:
        IP_table_name = args.IP_table_name

    if not test:
        admins=args.mails.split(';')


    # region STANDART_GOOGLE_ACCESS
    FLAGS = gflags.FLAGS

    # CLIENT_SECRETS, name of a file containing the OAuth 2.0 information for this
    # application, including client_id and client_secret.
    # You can see the Client ID and Client secret on the API Access tab on the
    # Google APIs Console <https://code.google.com/apis/console>
    
    # if gdrive_path specified all warks, with -c - lynx, w/out - 404
    if args.client_secrets:
        # linx
        CLIENT_SECRETS = args.client_secrets
    elif args.gdrive_path:
        # all works
        CLIENT_SECRETS = os.path.join(args.gdrive_path,'client_secrets.json')
    else:
        # w/out - 404
        CLIENT_SECRETS='client_secrets.json'

    # Helpful message to display if the CLIENT_SECRETS file is missing.
    MISSING_CLIENT_SECRETS_MESSAGE = """
    WARNING: Please configure OAuth 2.0

    To make this sample run you will need to download the client_secrets.json file
    and save it at:

       %s

    """ % CLIENT_SECRETS
    # """ % os.path.join(os.path.dirname(__file__), CLIENT_SECRETS)


    # Set up a Flow object to be used for authentication.
    # Add one or more of the following scopes. PLEASE ONLY ADD THE SCOPES YOU
    # NEED. For more information on using scopes please see
    # <https://developers.google.com/+/best-practices>.
    FLOW = flow_from_clientsecrets(CLIENT_SECRETS,
                                   scope=[
                                       'https://www.googleapis.com/auth/drive',
                                       'https://www.googleapis.com/auth/drive.apps.readonly',
                                       'https://www.googleapis.com/auth/drive.metadata.readonly',
                                       'https://www.googleapis.com/auth/drive.file',
                                       'https://www.googleapis.com/auth/drive.scripts',
                                       'https://www.googleapis.com/auth/drive.readonly',
                                       ],
                                   message=MISSING_CLIENT_SECRETS_MESSAGE)

    # При тестировании, при выполнении второго теста, тут жалуется.
    # Сделаю костыль, чтобы вызывалось только при запуске первого теста
    if run_first:
        # The gflags module makes defining command-line options easy for
        # applications. Run this program with the '--help' argument to see
        # all the flags that it understands.
        gflags.DEFINE_enum('logging_level', 'ERROR',
                           ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
                           'Set the level of logging detail.')

    # If the Credentials don't exist or are invalid, run through the native
    # client flow. The Storage object will ensure that if successful the good
    # Credentials will get written back to a file.
    if args.sample_dat:
        storage_path = args.sample_dat
    elif args.gdrive_path:
        storage_path = os.path.join(args.gdrive_path,'sample.dat')
    else:
        storage_path='sample.dat'
    # storage = Storage('sample.dat')
    storage = Storage(storage_path)
    credentials = storage.get()

    # endregion

    # region DELETING_MY_ARGS
    my_args=("-g", "--gdrive_path","-c", "--client_secrets","-e","--error_log","-f","--template_fn","-o", "--file_name","-m","--mails")
    my_no_pair_args = ("--script_debug","--IP_table_name","--sample_dat","--compare_with_old")
    for _ in my_args:
        if _ in sys.argv:
            sys.argv.pop(sys.argv.index(_)+1)
            sys.argv.pop(sys.argv.index(_))
    for _ in my_no_pair_args:
        if _ in sys.argv:
            sys.argv.pop(sys.argv.index(_))

    # Let the gflags module process the command-line arguments
    try:
        argv = FLAGS(sys.argv)
    except gflags.FlagsError, e:
        print ('%s\\nUsage: %s ARGS\\n%s' % (e, argv[0], FLAGS)) #google_args_error
        sys.exit(exit_code_dict['google_args_error'])
    # endregion


    logging.basicConfig(filename=error_log_file_name, filemode='w',level=logging.WARNING)
    logger_script=logging.getLogger("Script Error")

    if credentials is None or credentials.invalid:
        # credentials = run(FLOW, storage)
        print_to_stderr ("credential are None")
        raise IOError("credential are None")

    # Create an httplib2.Http object to handle our HTTP requests and authorize it
    # with our good Credentials.
    http = httplib2.Http()
    http = credentials.authorize(http)

    service = build('drive', 'v2', http=http)

    try:
        logger_script.info( "Login success! Starting to work.")
        found = False
        for entry in retrieve_all_files(service):
            if entry[u'title']==IP_table_name:
                found = True
                replacing_file(csv2files(ods2csv(download_file(service,
                                                                entry),
                                                 admins=admins),
                                        debug = False),
                               error_log_file_name=error_log_file_name,
                               admins=admins,
                               out_file_fn = args.file_name,
                               test = test,
                               templates = templates,
                               compare_with_old = compare_with_old)
        if not found:
            # print ("not found")
            logger_script.warning("Table %s doesn't exitst in Google Docs!" % IP_table_name)
    # For more information on the Drive API API you can visit:
    #
    #   https://developers.google.com/drive/
    #
    # For more information on the Drive API API python library surface you
    # can visit:
    #
    #   https://google-api-client-libraries.appspot.com/documentation/drive/v2/python/latest/
    #
    # For information on the Python Client Library visit:
    #
    #   https://developers.google.com/api-client-library/python/start/get_started

    except AccessTokenRefreshError:
        print ("The credentials have been revoked or expired, please re-run"
               "the application to re-authorize")
if __name__ == '__main__':
    main()