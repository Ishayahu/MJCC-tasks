#!/bin/bash
nmap -sP 172.22-28.0-7.1-254 > /usr/home/ishayahu/nmap.out
python2.7 /usr/home/ishayahu/tasks/snmp/nmap_processing.py
chown ishayahu: /usr/home/ishayahu/django.nmap.out