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
from djlib.mail_utils import send_email_alternative, send_email_html
from djlib.auxiliary import get_info
from djlib.logging_utils import log, confirm_log,\
    make_request_with_logging

from user_settings.settings import server_ip, admins, admins_mail
import socket
from pysnmp.entity.rfc3413.oneliner import cmdgen

def OLDget_switch_mac_port_dict(ip, communitiny_string):
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
                                     communitiny_string, 1)
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
                                     communitiny_string, 1)
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

def get_switch_mac_port_dict(ip, communitiny_string):
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
                                     communitiny_string, 1)
    transport = cmdgen.UdpTransportTarget((ip, 161))
    real_fun = getattr(generator, 'nextCmd')
    res = (errorIndication, errorStatus, errorIndex, varBinds) =\
        real_fun(comm_data, transport, value)
    if not errorIndication is None  or errorStatus is True:
           print "Error: %s %s %s %s" % res
    else:
        for x in varBinds:
            mac_dict['.'.join(map(str,x[0][0]))
            [len(mac_request)+1:]]=x[0][1]._value.encode('hex')
    value = port_request
    generator = cmdgen.CommandGenerator()
    generator.ignoreNonIncreasingOid = True
    comm_data = cmdgen.CommunityData('server',
                                     communitiny_string, 1)
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
                    '.'.join(map(str,x[0][0]))
                    [len(mac_request)+1:]]]=x[0][1]._value
                port_count[x[0][1]._value] =\
                    port_count.get(x[0][1]._value,0)+1
            except KeyError:
                print x
    mac_port_dict['port_count'] = port_count
    return mac_port_dict


class MAC:
    def __init__(self, mac):
        if ':' in mac:
            self.human_mac = mac
            self.string_mac = mac.replace(':','')
        else:
            self.string_mac = mac
            self.human_mac = mac[:2]+":"+mac[2:4]+":"+mac[4:6]+":"+mac[6:8]+":"+mac[8:10]+":"+mac[10:12]
    def lower(self):
        return self.human_mac.lower()

def check_connected_devices():
    res = dict()
    mac_info = dict()
    for line in open('/usr/home/ishayahu/tasks/snmp/Gdrive/for_tasks_snmp.out','r').readlines():
        try:
            mac,ip,name = line.split(';')
            mac = mac.replace(':','')
            mac_info[mac.lower()] = [ip,name]
        except ValueError:
            print line

    for switch in Switch.objects.all():
        mac_port_dict = get_switch_mac_port_dict(switch.ip,switch.commutiny_string)
        for mac, port in mac_port_dict.items():
            try:
                mac_info[mac]
            except KeyError:
                if mac !="port_count":
                    res[mac.lower()] = (switch,mac_port_dict[mac.lower()])
    html = u"<table border=1>"
    html += u"<tr><td>MAC</td><td>Switch ip</td><td>Место свича</td><td>Switch port</td></tr>"
    for key,val in res.items():
        mac = MAC(key)
        html += (u"<tr><td>"+unicode(mac.human_mac)+
                 u"</td><td><a href='http://172.22.0.138:8080/api/snmp/show_router_mapping_by_id/"+unicode(val[0].id)+"/#"+mac.string_mac+"'>"+unicode(val[0].ip)+u"</a>"+
                 u"</td><td>"+unicode(val[0].location)+
                 u"</td><td>"+unicode(val[1])+
                 u"</td></tr>")
    html += u"</table>"
    send_email_html(u"Неизвестные устройства",html,("meoc-it@mail.ru",))
    print res
