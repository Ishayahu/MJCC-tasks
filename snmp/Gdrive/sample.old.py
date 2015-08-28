#!/usr/local/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2012 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""Command-line skeleton application for Drive API.
Usage:
  $ python sample.py

You can also get help on all the command-line flags the program understands
by running:

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
# Получаем и обрабатываем аргументы
import argparse, os, sys
# Переменная, которая хранит код кода завершения для словаря
exit_code_key = 0
# Словарь кодов завершения
exit_code_dict = {'ok':0,
                  'google_args_error':1,
                  'dhcp_files_were_not_replaced':2,
                  'google_returned_empty_file':3,
                  'import_error':10,
                }

parser = argparse.ArgumentParser(description='Converting datas from google "IP range" table to dhcp.conf file. It use only that records, that have MAC address in table.')
parser.add_argument("-g", "--gdrive_path",help="path to drive library catalog, by default - working dir",default='.')

parser.add_argument("--A_col",help="Number of column with 1st part of IP, by default - 1",default='1')
parser.add_argument("--B_col",help="Number of column with 2nd part of IP, by default - 2",default='2')
parser.add_argument("--C_col",help="Number of column with 3rd part of IP, by default - 3",default='3')
parser.add_argument("--D_col",help="Number of column with 4th part of IP, by default - 4",default='4')
parser.add_argument("--Subnet_col",help="Number of column with subnet's part of IP, by default - 2",default='2')

parser.add_argument("--MAC_col",help="Number of column with MAC number, by default - 5",default='5')
parser.add_argument("--PC_name_col",help="Number of column with Subnet number, by default - 8",default='8')
parser.add_argument("--IP_table_name",help="Name of table from Google Docs, by default - IP range",default='IP range')
parser.add_argument("--dhcp_template",help="File with template for dhcp file. First string - template, by default - dhcp_template.txt",default='dhcp_template.txt')

parser.add_argument("--make_files_for_squid",help="Prepare squid files too",action='store_true',default=False)
parser.add_argument("--only_squid",help="Only prepare squid files",action='store_true',default=False)
parser.add_argument("--squid_path",help="full path to squid file catalog, by default - /etc/squid/",default='/etc/squid/')
parser.add_argument("--Squid_col",help="Number of column with Squid file names number, by default - 11",default='11')
# parser.add_argument("--IP_full_col",help="Number of column with full IP, by default - 10",default='10')
parser.add_argument("--Comment_col",help="Number of column with comment for IP, by default - 6",default='6')

parser.add_argument("-t", "--temp_path",help="path to temp catalog, by default - working dir",default='.')
parser.add_argument("-d", "--dhcp_path",help="full path to dhcp file catalog, by default - /etc/dhcp/",default='/etc/dhcp/')
parser.add_argument("-f", "--file_name",help="prefix for file name, by default - net_",default='net_')

parser.add_argument("-e", "--error_log",help="full path to error_log file, by default - ./error.log",default='error.log')
parser.add_argument("-m", "--mails",help="mails to send logs and alerts",default='meoc-it@mail.ru;karpion@rambler.ru')
parser.add_argument("--script_debug",help="do not delete temp files",action='store_true')
parser.add_argument("-c", "--client_secrets",help="full path to client_secrets.json file. If there aren't -c key and there is -g key, path to client_secrets.json construct from -g path and client_secrets.json filename. If there aren't -g and -c keys use file ./client_secrets.json")
parser.add_argument("--noauth_local_webserver",help="option for google.script",action='store_true')
args = parser.parse_args()
sys.path.insert(0,args.gdrive_path)
TEMP_FILE = os.path.join(args.temp_path,'IP_range.ods')
TEMP_FILE2 = os.path.join(args.temp_path,'IP_range.csv')
error_log_file_name = args.error_log

dhcp_dir_name = args.dhcp_path
dhcp_file_prefix_name = args.file_name
if dhcp_dir_name[-1] != '/': dhcp_dir_name = dhcp_dir_name + '/'
dhcp_file_full_name = dhcp_dir_name+dhcp_file_prefix_name

script_debug = args.script_debug
dhcp_template = open(args.dhcp_template).readline()+'\n'

A_col=int(args.A_col)
B_col=int(args.B_col)
C_col=int(args.C_col)
D_col=int(args.D_col)
Subnet_col=int(args.Subnet_col)

MAC_col = int(args.MAC_col)
PC_name_col = int(args.PC_name_col)
IP_table_name = args.IP_table_name

Squid_col=int(args.Squid_col)
# IP_full_col=int(args.IP_full_col)
Comment_col=int(args.Comment_col)
# no_squid = not args.make_files_for_squid
make_files_for_squid = args.make_files_for_squid
only_squid = args.only_squid
squid_path = args.squid_path
if squid_path[-1] != '/': squid_path = squid_path + '/'



admins=args.mails.split(';')
#print sys.path

try:
    import gflags
except ImportError:
    print "gflags not installed. see http://www.freshports.org/devel/py-gflags/"
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

FLAGS = gflags.FLAGS

# CLIENT_SECRETS, name of a file containing the OAuth 2.0 information for this
# application, including client_id and client_secret.
# You can see the Client ID and Client secret on the API Access tab on the
# Google APIs Console <https://code.google.com/apis/console>
if args.client_secrets:
    CLIENT_SECRETS = args.client_secrets
elif args.gdrive_path:
    CLIENT_SECRETS = os.path.join(args.gdrive_path,'client_secrets.json')
else:
    CLIENT_SECRETS='client_secrets.json'
    
# Helpful message to display if the CLIENT_SECRETS file is missing.
MISSING_CLIENT_SECRETS_MESSAGE = """
WARNING: Please configure OAuth 2.0

To make this sample run you will need to download the client_secrets.json file
and save it at:

   %s

""" % os.path.join(os.path.dirname(__file__), CLIENT_SECRETS)


#print
#print TEMP_FILE, TEMP_FILE2,dhcp_file_name

#exit()


#TEMP_FILE = '/home/ishayahu/IP range.ods'
#TEMP_FILE2 = '/home/ishayahu/IP range.csv'
#dhcp_file_name = '/home/ishayahu/dhcp'


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


# The gflags module makes defining command-line options easy for
# applications. Run this program with the '--help' argument to see
# all the flags that it understands.
gflags.DEFINE_enum('logging_level', 'ERROR',
    ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
    'Set the level of logging detail.')

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
      print 'An error occurred: %s' % error
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
  #download_url = drive_file.get('downloadUrl')
  download_url = drive_file[u'exportLinks'][u'application/x-vnd.oasis.opendocument.spreadsheet']
  if download_url:
    resp, content = service._http.request(download_url)
    if resp.status == 200:
      #print 'Status: %s' % resp
      return content
    else:
      print 'An error occurred: %s' % resp
      return None
  else:
    # The file doesn't have any content stored on Drive.
    return None

def ods2csv(content):  

  import sys,zipfile,re,os,csv  
  try:
    from pyquery import PyQuery as pq  
  except ImportError:
    print "pyquery not installed. see http://www.freshports.org/www/py-pyquery/"
    sys.exit(exit_code_dict['import_error'])
  from lxml.cssselect import CSSSelector
  from StringIO import StringIO
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
    sending_log("DHCP_ERROR: script got an error","<b>Google returned empty file</b>, script ended without any changes made!")
    # print 3
    sys.exit(exit_code_dict['google_returned_empty_file'])
  #print data[1][0]
  #exit()

  #root,ext=os.path.splitext(filepath)  
  #with open(''.join([root,'.csv']),'wb') as f:  
  #  for row in data:  
  #    dw = csv.writer(f)  
  #    dw.writerow(row)  
      
def csv2dhcp(data):
  rep_dict={"а".decode('utf-8'):'a',
          "с".decode('utf-8'):'c',
          "е".decode('utf-8'):'e',
          "А".decode('utf-8'):'a',
          "Е".decode('utf-8'):'e',
          "С".decode('utf-8'):'c',
          "В".decode('utf-8'):'b',
          }
  ips=set()
  macs=set()
  pc_names=set() #datetime.datetime.now().microsecond
  logger_mac=logging.getLogger("Wrong MAC")
  logger_ip=logging.getLogger("Wrong IP")
  logger_pc_name=logging.getLogger("Wrong PC-NAME")
  #dhcp_file=open(dhcp_file_name,'w')
  # datas = []
  datas = dict()
  squid_datas = dict()
  for line in data:#open(filepath,'r'):
    # Сокращаем время работы разбивая строку один раз:
    #line = line.strip().split(',')
    str_line="<b>"+";\t".join([a.decode('utf-8') for a in line])+"</b>"
    # формат полученной строки:
    # 1 - A
    # 2 - B
    # 3 - C
    # 4 - D
    # 5 - MAC
    # 6 - Место
    # 7 - Кто
    # 8 - PC-Name
    # 9 - Полный IP адресс
    # 10 - Имя файла для squid'a
    # 11 - 
    # Пропускаем первую строку:
    if line[A_col]=="A":
        continue
    # Пропускаем отсутствующие ПК, у которых не указан МАК
    if not line[MAC_col]:
        continue
    # Проверка наличия имени ПК:
    try:
        if not line[PC_name_col]:
            logger_pc_name.warning("Empty PC-name: %s" % str_line)
            continue
        else: # Проверка того, что в имени только буквы-цифры и тире
            valid = re.match('^[\w-]+$', line[PC_name_col]) is not None
            if not valid:
                logger_pc_name.warning("PC-name contain worng symbol: %s" % str_line)
                continue
    except IndexError:
        logger_pc_name.warning("Empty PC-name: %s" % str_line)
        continue
    # Проверка Мака
    if len(line[MAC_col])>17:
        # Проверяем и меняем  ("а", "с", "е") c русских на английские, если есть:
        # ";".join([a.decode('utf-8') for a in line])
        mac = line[MAC_col]
        for char in mac.decode('utf-8'):
            if char in "асеАЕСВ".decode('utf-8'):
                mac = mac.decode('utf-8').replace(char,rep_dict[char]).decode('ascii')
                logger_mac.warning("MAC contain wrong symbol: <b>%s</b>;replaced to <b>%s</b>: %s" % (char,rep_dict[char],str_line))
        line[MAC_col] = mac
        # for char in mac.decode('utf-8'):
            # if char.upper() not in "abcdef1234567890:".decode('utf-8').upper():
                # logger_mac.warning("MAC contain wrong symbol: <b>%s</b>;replaced to <b>%s</b>: %s" % (char,rep_dict[char],str_line))
                
    if len(line[MAC_col])!=17:
        logger_mac.warning("MAC contain wrong count of symbols: %s" % str_line)
        continue
    else:
        to_continue = True
        mac=line[MAC_col][:2]+line[MAC_col][3:5]+line[MAC_col][6:8]+line[MAC_col][9:11]+line[MAC_col][12:14]+line[MAC_col][15:17]
        for char in mac.decode('utf-8'):
            if char.lower() not in "0123456789abcdef".decode('utf-8'):
                logger_mac.warning("MAC contain wrong symbol: <b>%s</b>: %s" % (char,str_line))
                print char.decode('utf-8')
                to_continue = False
            line[MAC_col]=mac[:2]+':'+mac[2:4]+':'+mac[4:6]+':'+mac[6:8]+':'+mac[8:10]+':'+mac[10:]
    # Если в маке неверный символ
    if not to_continue:
        continue
    # Проверка IP, все 4 части
    if line[A_col].isdigit():
        if not 0<int(line[A_col])<255:
            logger_ip.warning("A_col less 0 or more 255: %s" % str_line)
            continue
    else:
        logger_ip.warning("A_col isn't a digit: %s" % str_line)
        continue
    if line[B_col].isdigit():
        if not 0<=int(line[B_col])<255:
            logger_ip.warning("B_col less 0 or more 255: %s" % str_line)
            continue
    else:
        logger_ip.warning("B_col isn't a digit: %s" % str_line)
        continue
    if line[C_col].isdigit():
        if not 0<=int(line[C_col])<255:
            logger_ip.warning("C_col less 0 or more 255: %s" % str_line)
            continue
    else:
        logger_ip.warning("C_col isn't a digit: %s" % str_line)
        continue
    if line[D_col].isdigit():
        if not 0<int(line[D_col])<255:
            logger_ip.warning("D_col less 0 or more 255: %s" % str_line)
            continue
    else:
        logger_ip.warning("D_col isn't a digit: %s" % str_line)
        continue
    
    # Возвращаем список записей для файла
    # составляем IP адрес
    ip = str(line[A_col])+'.'+str(line[B_col])+'.'+str(line[C_col])+'.'+str(line[D_col])
    if ip not in ips:
        if line[MAC_col] not in macs:
            ips.add(ip)
            macs.add(line[MAC_col])
            if line[PC_name_col] not in pc_names:
                pc_names.add(line[PC_name_col])
            else:
                logger_pc_name.warning("Repeated PC-name found: %s" % str_line)
                line[PC_name_col]+=str(datetime.datetime.now().microsecond)
                pc_names.add(line[PC_name_col])
            # Проверяем уникальность имени ПК, если не уникален - добавляем 
            # datetime.datetime.now().microsecond
            #dhcp_file.write("host %s { hardware ethernet %s; fixed-address 192.168.%s.%s; }\n" % (line[PC_name_col],line[MAC_col],line[Subnet_col],line[IP_col]))
            # text=text.decode('utf8').format({'number':cashless.bill_number,'where':places,'date':str(cashless.date_of_invoice),'price':price,'what':what,'who':fio.fio,'phones':fio.tel,'date2':str(datetime.datetime.now()).split('.')[0]}).replace('\n','<p>')
            # raise NotImplementedError ("writing separate file for each subnet")
            if not only_squid:
                if line[Subnet_col] in datas:
                    datas[line[Subnet_col]].append(dhcp_template.format({'host_name':line[PC_name_col],'mac':line[MAC_col],'a':line[A_col],'d':line[D_col],'b':line[B_col],'c':line[C_col]}))
                else:
                    datas[line[Subnet_col]]=[]
                    datas[line[Subnet_col]].append(dhcp_template.format({'host_name':line[PC_name_col],'mac':line[MAC_col],'a':line[A_col],'d':line[D_col],'b':line[B_col],'c':line[C_col]}))
            if make_files_for_squid:
                if line[Squid_col]:
                    ip = line[A_col]+'.'+line[B_col]+'.'+line[C_col]+'.'+line[D_col]
                    # if script_debug: print Squid_col,line[Squid_col]
                    if line[Squid_col] in squid_datas:
                        squid_datas[line[Squid_col]].append(ip+" #"+line[Comment_col])
                    else:
                        squid_datas[line[Squid_col]]=[]
                        squid_datas[line[Squid_col]].append(ip+" #"+line[Comment_col])
            # datas.append("host %s { hardware ethernet %s; fixed-address 192.168.%s.%s; }\n" % (line[PC_name_col],line[MAC_col],line[Subnet_col],line[IP_col]))
        else:
            logger_mac.warning("Repeated mac founded: <b>%s</b>" % line[MAC_col])
    else:
        logger_ip.warning("Repeated ip founded: <b>%s</b>" % ip)
    
  #dhcp_file.close()
  #print len(data)
  #print
  #print len(datas)
  #exit()
  if script_debug:
    for x in squid_datas:
        print x
        print len(squid_datas[x])
  return (datas,squid_datas)
def replacing_file(datas,squid_datas): # old new_dhcp_datas
    # raise NotImplementedError ("writing separate file for each subnet")
    if not only_squid:
        not_replaced_at_all = False
        for subnet in datas:
            new_dhcp_datas = datas[subnet]
            dhcp_file_name = dhcp_file_full_name+str(subnet)
            
            new_dhcp_set=set(new_dhcp_datas)
            iteration_set=set(new_dhcp_datas)
            try:
                old_dhcp_set=set(open(dhcp_file_name,'r').readlines())
                old_records = len(old_dhcp_set)
            except (OSError,IOError):
                old_dhcp_set=set()
            #print len(new_dhcp_set)
            #print
            #print len(old_dhcp_set)
            #exit()
            message = ""
            
            if not 0.67<len(old_dhcp_set)/len(new_dhcp_set)<1.5:
                message = "<b>Difference between new and old files is too big. Please check if all is correct!</b><br />"
            
            for record in iteration_set:
                if record in old_dhcp_set:
                    old_dhcp_set.remove(record)
                    new_dhcp_set.remove(record)
            #print 
            #print "After ineration"
            #print new_dhcp_set
            #print
            #print old_dhcp_set
            #exit()
            # Если нет разницы в файлах - оба множества пусты
            if not old_dhcp_set and not new_dhcp_set:
                not_replaced_at_all = True
                # sending_log("DHCP_OK: file was not replaced","<b>File was not replaced because it has the same content</b><br />")
                # sys.exit(2)
            # записываем в лог отличия в файлах -- и ++ и потом посылаем. После чего перезаписываем файлы
            try:
                os.rename(dhcp_file_name,dhcp_file_name+'.'+datetime.datetime.now().__str__()[:-7].replace(':','-'))
            except (IOError,OSError) as e:
                message=message+"<br /><b>Old file "+dhcp_file_name+" was not renamed because following error:<br />I/O error(<i>{0}</i>): <i>{1}</i></b><br />".format(e.errno, e.strerror)
            # dhcp_dir_name = args.dhcp_path
            # dhcp_file_prefix_name = args.file_name    
            # raise NotImplementedError ("writing separate file for each subnet")
            dhcp_file = open(dhcp_file_name,'w')
            #print new_dhcp_set,"\n",dhcp_file_name
            for line in iteration_set:
                dhcp_file.write(line)
            dhcp_file.close()
            if old_dhcp_set:
                message = message + "<br /><br />That records was in old dhcp file but there are no in new file:<br /><ol>"
                for record in old_dhcp_set:
                    message = message +"<li>" +record + "</li>"
                message = message + "</ol>"
            if new_dhcp_set:
                message = message + "<br /><br />That records are in new dhcp file but there was not in old file:<br />"
                for record in new_dhcp_set:
                    message = message+"<li>" + record + "</li>"
                message = message + "</ol>"
        if not_replaced_at_all:
            sending_log("DHCP_OK: file was not replaced","<b>File was not replaced because it has the same content</b><br />")
            exit_code_key = 'dhcp_files_were_not_replaced'
            if not make_files_for_squid:
                # print 2
                sys.exit(exit_code_dict['dhcp_files_were_not_replaced'])
        sending_log("DHCP_OK:File was succefull replaced",message)
    message = ''
    if make_files_for_squid:
        for file in squid_datas:
            fn = squid_path + file
            try:
                os.rename(fn,fn+'.'+datetime.datetime.now().__str__()[:-7].replace(':','-'))
            except (IOError,OSError) as e:
                message=message+"<br /><b>Old file "+fn+" was not renamed because following error:<br />I/O error(<i>{0}</i>): <i>{1}</i></b><br />".format(e.errno, e.strerror)
            f = open(fn,'w')
            for line in squid_datas[file]:
                f.write(line+'\n')
            f.close()
    sending_log("SQUID_OK:File was succefull replaced",message)
    if exit_code_key:
        sys.exit(exit_code_dict[exit_code_key])
def sending_log(header,message):
    log = open(error_log_file_name,'r').readlines()
    if log:
        message = message + "<br /><br /><b>Entries of the log</b>:<br /><ol>"
        for line in log:
            message = message+'<li>'+line
        message = message + "</ol>"
        send_email(header,message,admins)
    else:
        send_email(header,message,admins)
def main(argv):
  print make_files_for_squid
  print only_squid

  # Let the gflags module process the command-line arguments
  try:
    argv = FLAGS(argv)
  except gflags.FlagsError, e:
    print '%s\\nUsage: %s ARGS\\n%s' % (e, argv[0], FLAGS)
    # print 1
    sys.exit(exit_code_dict['google_args_error'])


  logging.basicConfig(filename=error_log_file_name, filemode='w',level=logging.WARNING)
  logger_script=logging.getLogger("Script Error")
  # Set the logging according to the command-line flag
  #logging.getLogger().setLevel(getattr(logging, FLAGS.logging_level))
  #exit()
  # If the Credentials don't exist or are invalid, run through the native
  # client flow. The Storage object will ensure that if successful the good
  # Credentials will get written back to a file.
  storage = Storage('sample.dat')
  credentials = storage.get()

  if credentials is None or credentials.invalid:
    credentials = run(FLOW, storage)

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
	    #pprint.pprint (entry)
	    #print entry[u'exportLinks'][u'application/x-vnd.oasis.opendocument.spreadsheet']
	    #print "Writing content to %s" % TEMP_FILE
	    #open(TEMP_FILE,'w').write(download_file(service, entry))
	    #print "Converting ods to csv"
	    #ods2csv(download_file(service, entry))
	    #csv2dhcp(ods2csv(download_file(service, entry)))
            replacing_file(*csv2dhcp(ods2csv(download_file(service, entry))))
    if not found:
        print "not found"
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
def send_email(subject,message,reciver):
    import smtplib
    from email.MIMEText import MIMEText
    from email.MIMEMultipart import  MIMEMultipart 
    from_email = "meoc-it@mail.ru"
    # SMTP-сервер
    server = "192.168.1.1"
    port = 25
    #user_name = "support.tonics@gmail.com"
    #user_passwd = "password"
    
    server = "smtp.gmail.com"
    port = "25"
    user_name = "ishayahu@gmail.com"
    user_passwd = '"kkbitdfkt2371@'

    #reciver = "meoc-it@mail.ru"

    # формирование сообщения
    #msg = MIMEText(message, "", "utf-8")
    msg = MIMEMultipart('mixed')
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = ', '.join(reciver)
    
    # Формируем письмо
    part1 = MIMEText(message, 'html','utf-8')
    #part2 = MIMEText('Содержимое приложенного файла', 'text/html;name="tasks.htm"', 'utf-8')
    msg.attach(part1)
    #msg.attach(part2)
    
    # отправка
    s = smtplib.SMTP(server, port)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login(user_name, user_passwd)
    s.sendmail(from_email, msg['To'], msg.as_string())
    s.quit()

if __name__ == '__main__':
  #print sys.argv
  my_args=("-g", "--gdrive_path","-t", "--temp_path","-d", "--dhcp_path","-c", "--client_secrets","-e","--error_log","--dhcp_template","-f", "--file_name")
  my_no_pair_args = ("--script_debug",'--Subnet_col','--A_col','--B_col','--C_col','--D_col',"--Subnet_col","--MAC_col","--PC_name_col","--IP_table_name","--make_files_for_squid","--squid_path","--Squid_col","--IP_full_col","--Comment_col","--only_squid")
  for _ in my_args:
      if _ in sys.argv:
        #print sys.argv.index(_),sys.argv.index(_)+1
        sys.argv.pop(sys.argv.index(_)+1)
        sys.argv.pop(sys.argv.index(_))
  for _ in my_no_pair_args:  
    if _ in sys.argv:
        sys.argv.pop(sys.argv.index(_))
  #sending_log("DHCP_TEST: Testing script","testing sending message with log")
  #exit()
  main(sys.argv)