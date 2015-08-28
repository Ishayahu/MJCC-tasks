# -*- coding:utf-8 -*-
# coding=<utf8>

import datetime
from itertools import chain

from django.http import HttpResponse, Http404, HttpResponseRedirect,\
    HttpResponseForbidden
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.template import RequestContext
from snmp.models import Switch

from djlib.cron_utils import decronize, crontab_to_russian,\
    generate_next_reminder
from djlib.text_utils import htmlize
from djlib.acl_utils import acl, for_admins, admins_only
from djlib.user_tracking import set_last_activity_model,\
    get_last_activities
from djlib.mail_utils import send_email_alternative
from djlib.auxiliary import get_info
from djlib.logging_utils import log, confirm_log,\
    make_request_with_logging

from user_settings.settings import server_ip, admins, admins_mail
try:
    from user_settings.settings import assets_url_not_to_track as \
        url_not_to_track
except ImportError:
    url_not_to_track = ('',)
try:
    from user_settings.settings import assets_url_one_record as \
        url_one_record
except ImportError:
    url_one_record = ('',)


from djlib.error_utils import FioError, ErrorMessage, add_error,\
    shows_errors

from djlib.multilanguage_utils import select_language, multilanguage,\
    register_lang
from pysnmp.entity.rfc3413.oneliner import cmdgen
register_lang('ru', 'RUS')
register_lang('eng', 'ENG')
app = 'snmp'


@login_required
@multilanguage
@shows_errors
@admins_only
def show_router_mapping(request, community, ip):
    mac_request = "1.3.6.1.2.1.17.4.3.1.1"
    port_request = "1.3.6.1.2.1.17.4.3.1.2"
    # from pysnmp.entity.rfc3413.oneliner import cmdgen
    import socket
    # ip='172.22.0.100'
    # community='zwziolss'
    value = mac_request
    generator = cmdgen.CommandGenerator()

    # cmdGen = cmdgen.CommandGenerator()
    # cmdGen.ignoreNonIncreasingOid = True
    # for HP JG538A
    generator.ignoreNonIncreasingOid = True


    comm_data = cmdgen.CommunityData('server', community, 1) # 1 means version SNMP v2c
    transport = cmdgen.UdpTransportTarget((ip, 161))
    real_fun = getattr(generator, 'nextCmd')
    res = (errorIndication, errorStatus, errorIndex, varBinds) =\
        real_fun(comm_data, transport, value)
    mac_dict = dict()
    # print "SNMP result: %s" % [res]
    if not errorIndication is None  or errorStatus is True:
           print "Error: %s %s %s %s" % res
    else:
        for x in varBinds:
            mac_dict['.'.join(map(str,x[0][0]._value))
            [len(mac_request)+1:]]=x[0][1]._value.encode('hex')
    # raise ImportError()
    value = port_request
    generator = cmdgen.CommandGenerator()
    generator.ignoreNonIncreasingOid = True
    comm_data = cmdgen.CommunityData('server', community, 1)
    # 1 means version SNMP v2c
    transport = cmdgen.UdpTransportTarget((ip, 161))
    real_fun = getattr(generator, 'nextCmd')
    res = (errorIndication, errorStatus, errorIndex, varBinds) =\
        real_fun(comm_data, transport, value)
    mac_port_dict=dict()
    # print "SNMP result: %s" % [res]
    if not errorIndication is None  or errorStatus is True:
           print "Error: %s %s %s %s" % res
    else:
        for x in varBinds:
            try:
                mac_port_dict[mac_dict[
                    '.'.join(map(str,x[0][0]._value))
                    [len(mac_request)+1:]]]=x[0][1]._value
            except KeyError:
                print x

    class MacPort():
        def __init__(self,mac,port):
            self.mac = ":".join(map(''.join, zip(*[iter(mac)]*2)))
            self.brand_mac = "-".join(map(''.join, zip(*[iter(mac)]*2))[:3])
            self.port = port
    mac_port = []
    for k,v in mac_port_dict.items():
        mac_port.append(MacPort(k,v))
    mac_port = sorted(mac_port,key=lambda x: x.port)
    mac_info = dict()
    # for line in open('/usr/home/ishayahu/django.nmap.out','r').readlines():
    #     mac,ip,name,brand = line.split(';')
    #     mac_info[mac.lower()] = [ip,name,brand]
    for line in open('/usr/home/ishayahu/tasks/snmp/Gdrive/for_tasks_snmp.out','r').readlines():
        try:
            mac,ip,name = line.split(';')
            mac_info[mac.lower()] = [ip,name]
        except ValueError:
            pass
    for number,record in enumerate(mac_port):
        record.number = number
        try:
            record.ip = mac_info[record.mac.lower()][0]
            record.name = mac_info[record.mac.lower()][1]
            if not record.name.strip():
                try:
                    record.name = socket.gethostbyaddr(record.ip)[0]
                except socket.herror:
                    pass
        except KeyError:
            pass
    return (True,
            ('show_map.html',
              {},
              {'mac_port_dict': mac_port, 'title': u'Карта сети'},
              request,app)
            )


def show_router_mapping_by_id(request, switch_id):
    switch = Switch.objects.get(id=int(switch_id))
    return show_router_mapping(request,
                               switch.commutiny_string,
                               switch.ip)


@login_required
@multilanguage
@shows_errors
@admins_only
def brand_by_mac(request, mac):
    import httplib, urllib,re
    payload = {'x':mac}
    params = urllib.urlencode(payload)
    conn = httplib.HTTPConnection("standards.ieee.org")
    conn.request("POST", "/cgi-bin/ouisearch", params)
    response = conn.getresponse()
    data = response.read()
    conn.close()
    text = re.findall(r'<pre>([\s\S]*)</pre>',data,re.M)[0]
    brand = re.findall(r'<b>.*</b>\s*\(hex\)\s(.*)',text)
    brand = brand[0].strip()
    return (True,('help.html',{},
                  {'text':brand,},
                  request,app))\


@login_required
@multilanguage
@shows_errors
@admins_only
def name_by_ip(request, ip):
    import socket
    print ip
    try:
        name = socket.gethostbyaddr(ip)[0]
    except socket.herror:
        name = "NOT_FOUND"
    # ('WIN-QDHFP707KLL', [], ['172.22.0.153'])
    return (True,('help.html',{},
                  {'text':name,},
                  request,app))


def get_switch_dict(ip, commutiny_string):
    mac_request = "1.3.6.1.2.1.17.4.3.1.1"
    port_request = "1.3.6.1.2.1.17.4.3.1.2"
    # получаем корневой свич
    mac_dict = dict()
    mac_port_dict = dict()
    port_count = dict()
    value = mac_request
    generator = cmdgen.CommandGenerator()
    generator.ignoreNonIncreasingOid = True
    comm_data = cmdgen.CommunityData('server',
                                     commutiny_string, 1)
    transport = cmdgen.UdpTransportTarget((ip, 161))
    real_fun = getattr(generator, 'nextCmd')
    res = (errorIndication, errorStatus, errorIndex, varBinds) =\
        real_fun(comm_data, transport, value)
    if not errorIndication is None  or errorStatus is True:
           print "Error: %s %s %s %s" % res
    else:
        for x in varBinds:
            mac_dict['.'.join(map(str,x[0][0]._value))
            [len(mac_request)+1:]]=x[0][1]._value.encode('hex')
    value = port_request
    generator = cmdgen.CommandGenerator()
    generator.ignoreNonIncreasingOid = True
    comm_data = cmdgen.CommunityData('server',
                                     commutiny_string, 1)
    transport = cmdgen.UdpTransportTarget((ip, 161))
    real_fun = getattr(generator, 'nextCmd')
    res = (errorIndication, errorStatus, errorIndex, varBinds) =\
        real_fun(comm_data, transport, value)
    if not errorIndication is None  or errorStatus is True:
           print "Error: %s %s %s %s" % res
    else:
        for x in varBinds:
            try:
                mac_port_dict[mac_dict[
                    '.'.join(map(str,x[0][0]._value))
                    [len(mac_request)+1:]]]=x[0][1]._value
                port_count[x[0][1]._value] =\
                    port_count.get(x[0][1]._value,0)+1
            except KeyError:
                print x
    mac_port_dict['port_count'] = port_count
    return mac_port_dict


@login_required
@multilanguage
@shows_errors
@admins_only
def find_by_mac(request, mac):
    # class SimpleSwitch:
    #     def __init__(self, switch, port):
    #         self.name = switch.name
    #         self.port = port
    #         self.community_string = switch.commutiny_string
    #         self.ip = switch.ip
    # mac_request = "1.3.6.1.2.1.17.4.3.1.1"
    # port_request = "1.3.6.1.2.1.17.4.3.1.2"
    def trace_mac(mac,switch,trace):
        print switch
        mac_port_dict = get_switch_dict(switch.ip,switch.commutiny_string)
        try:
            port = mac_port_dict[mac]
        except KeyError:
            # не найден
            return False
        switch.port = port
        switch.port_count = mac_port_dict['port_count'][port]
        # raise ImportError()
        trace.append(switch)
        chilren = Switch.objects.filter(parent_switch = switch)
        for child in chilren:
            return trace_mac(mac,child,trace)
    mac = mac.replace(':','')
    # получаем корневой свич
    roots = Switch.objects.filter(parent_switch__isnull=True)
    trace = []
    for root in roots:
        res = trace_mac(mac,root,trace)
        if res:
            break
    start_count = float("inf")
    for record in trace:
        if record.port_count < start_count:
            start_count = record.port_count
        else:
            record.probably_not = True
    return (True,('show_trace.html',{},
                  {'trace':trace,
                   'title':u'Поиск мака'},
                  request,app))
