__author__ = 'Ishayahu'
__version__ = '0.0.1'

import re
mac_ip_dict = dict()
ip = ''
mac = ''
name = ''
factory = ''
out = open('/usr/home/ishayahu/django.nmap.out','w')
for line in open('/usr/home/ishayahu/nmap.out').readlines():
    if line.startswith('Nmap scan report for '):
        res = re.findall(r'Nmap scan report for ?(.*)? \(?(\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3})\)?',line)[0]
        name = res[0]
        try:
            ip = res[1]
        except:
            print line
            exit()
    if line.startswith('MAC Address:'):
        res = re.findall(r'MAC Address: ([0-9a-fA-F]{2}:[0-9a-fA-F]{2}:[0-9a-fA-F]{2}:[0-9a-fA-F]{2}:[0-9a-fA-F]{2}:[0-9a-fA-F]{2})? ?\(?([^)]*)\)?',line)[0]
        factory = res[1]
        mac = res[0]
    if mac and ip:
        out.write("{0};{1};{2};{3}\n".format(mac,ip,name,factory))
        mac = ''
        ip = ''
        name = ''
        factory =''
out.close()
