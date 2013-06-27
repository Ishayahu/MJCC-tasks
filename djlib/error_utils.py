# -*- coding:utf-8 -*-
# coding=<utf8>

class FioError():
    def __init__(self):
        self.mail=''
        self.message='Нет такого пользователя'
    def __str__(self):
        return self.message
class ErrorMessage():
    def __init__(self,message):
        self.message='Нет такого пользователя'
    def __str__(self):
        return self.message