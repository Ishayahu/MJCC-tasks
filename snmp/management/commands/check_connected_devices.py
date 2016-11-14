# -*- coding:utf-8 -*-
# coding=<utf8>

from django.core.management.base import BaseCommand, CommandError
from snmp.utils import check_connected_devices

class Command(BaseCommand):
    help = 'Check connected devices'

    def handle(self, *args, **options):
        check_connected_devices()