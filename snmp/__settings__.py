# -*- coding:utf-8 -*-
# coding=<utf8>
__author__ = 'Ishayahu'

from djlib.module_utils import Link, Module


# class Link:
#     def __init__(self, name, href):
#         self.name = name
#         self.href = href


# class Module:
#     def __init__(self):
#         self.links = [
#             Link(u'Показать роутер',
#                  '/api/snmp/show_router_mapping/9c59d8f079/172.22.5.105/'),
#             Link(u'Показать роутер по id',
#                  '/api/snmp/show_router_mapping_by_id/{0}/'),
#             Link(u'Найти MAC',
#                  '/api/snmp/find_by_mac/74:d4:35:b1:e4:e3/'),
#
#         ]

links = [
            Link(u'Показать роутер',
                 u'/api/snmp/show_router_mapping/{Community string}/{ip}/'),
            Link(u'Показать роутер по id',
                 u'/api/snmp/show_router_mapping_by_id/{id}/'),
            Link(u'Найти MAC',
                 u'/api/snmp/find_by_mac/{MAC}/'),

        ]