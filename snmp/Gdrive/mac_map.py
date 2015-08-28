#!/usr/local/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2012 Google Inc.
# Под версию 2.x
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
  $ python mac_map.py

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
  
  # Коды возврата команды
  # 1 - Если вовзращённый гуглом файл пустой
  # 2 - Если новый файл не отличается от старого
"""
# Получаем и обрабатываем аргументы
import argparse, os, sys
parser = argparse.ArgumentParser(description='Converting datas from google "IP range" table to dhcp.conf file. It use only that records, that have MAC address in table.')
parser.add_argument("-g", "--gdrive_path",help="path to drive library catalog, by default - working dir",default='.')

parser.add_argument("--IP_col",help="Number of column with IP number, by default - 2",default='2')
parser.add_argument("--Subnet_col",help="Number of column with Subnet number, by default - 1",default='1')
parser.add_argument("--MAC_col",help="Number of column with MAC number, by default - 3",default='3')
parser.add_argument("--PC_name_col",help="Number of column with Subnet number, by default - 1",default='6')
parser.add_argument("--IP_table_name",help="Name of table from Google Docs, by default - IP range",default='IP range')

parser.add_argument("-f", "--file",help="path to file with mac data, by default - ./mac.txt",default='./mac.txt')
# parser.add_argument("-d", "--dhcp_path",help="full path to dhcp file, by default - ./dhcp.conf",default='dhcp.conf')
parser.add_argument("-e", "--error_log",help="full path to error_log file, by default - ./error.log",default='error.log')
parser.add_argument("-m", "--mails",help="mails to send logs and alerts",default='meoc-it@mail.ru;karpion@rambler.ru')
# parser.add_argument("--script_debug",help="do not delete temp files",action='store_true')
parser.add_argument("-c", "--client_secrets",help="full path to client_secrets.json file. If there aren't -c key and there is -g key, path to client_secrets.json construct from -g path and client_secrets.json filename. If there aren't -g and -c keys use file ./client_secrets.json")
parser.add_argument("--noauth_local_webserver",help="option for google.script",action='store_true')

# Разбираем аргументы
args = parser.parse_args()
sys.path.insert(0,args.gdrive_path)
# TEMP_FILE = os.path.join(args.temp_path,'IP_range.ods')
# TEMP_FILE2 = os.path.join(args.temp_path,'IP_range.csv')
error_log_file_name = args.error_log
map_file = args.file
# script_debug = args.script_debug

IP_col=int(args.IP_col)
Subnet_col = int(args.Subnet_col)
MAC_col = int(args.MAC_col)
PC_name_col = int(args.PC_name_col)
IP_table_name = args.IP_table_name

admins=args.mails.split(';')

# Гугловая часть из руководства
import gflags
import httplib2
import logging
import datetime
import pprint
import os,sys

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
  from pyquery import PyQuery as pq  
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
    sys.exit(1)

      
def csv2map(data):
  rep_dict={"а".decode('utf-8'):'a',
          "с".decode('utf-8'):'c',
          "е".decode('utf-8'):'e',
          "А".decode('utf-8'):'a',
          "Е".decode('utf-8'):'e',
          "С".decode('utf-8'):'c',
          "В".decode('utf-8'):'b',
          }
  result_file=open('mac_map.txt','w')
  datas = []
  # Делаем словарь из полученных данных, который затем используем для дешифровки мак вдресов
  mac_name_dict=dict()
  mac_port_dict=dict()
  for line in data: # MAC:NAME
    if len(line)>MAC_col and len(line)>PC_name_col:
      # print line, MAC_col, PC_name_col
      mac_name_dict[line[MAC_col].lower()]=line[PC_name_col]
  # Готовим данные из файла с маками по порту (MAC:PORT)
  for line in open(map_file,'r'):
    mac_port_dict[line.split('\t')[1].lower()] = line.split('\t')[2][3:]
  # А теперь делаем файл с картой
  result_file.write('MAC;Name;Port\n')
  for k in mac_port_dict:
    result_file.write(';'.join((k,mac_name_dict.get(k,'NOT IN TABLE'),mac_port_dict[k])))
  result_file.close()
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
  # Let the gflags module process the command-line arguments
  try:
    argv = FLAGS(argv)
  except gflags.FlagsError, e:
    print '%s\\nUsage: %s ARGS\\n%s' % (e, argv[0], FLAGS)
    sys.exit(1)


  logging.basicConfig(filename=error_log_file_name, filemode='w',level=logging.WARNING)
  logger_script=logging.getLogger("Script Error")
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
            csv2map(ods2csv(download_file(service, entry)))
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
  my_args=('-c',"-g", "--gdrive_path","-t", "--temp_path","-d", "--dhcp_path","-c", "--client_secrets","-e","--error_log",)
  my_no_pair_args = ("--script_debug",'--IP_col',"--Subnet_col","--MAC_col","--PC_name_col","--IP_table_name",)
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