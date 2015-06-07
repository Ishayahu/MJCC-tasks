# -*- coding:utf-8 -*-
# coding=<utf8>

__author__ = 'Ishayahu'

class ParentField(object):
    def __init__(self):
        pass
    def __get_column_sql_check__(self):
        """
        Выдаёт SQL код для проверки существования нужного столбца таблицы
        """
        raise NotImplementedError("Must be replaced in children class")
    def __get_column_sql_create__(self):
        """
        Выдаёт SQL код для создания нужного столбца таблицы
        """
        raise NotImplementedError("Must be replaced in children class")
class IntegerField(ParentField):
    def __init__(self):
        pass
    def __get_column_sql_check__(self):
        """
        Выдаёт SQL код для проверки существования нужного столбца таблицы
        """
        raise NotImplementedError("Must be replaced in children class")
    def __get_column_sql_create__(self):
        """
        Выдаёт SQL код для создания нужного столбца таблицы
        """
        return "Create IntegerField for {0},\n".format((self.__attr_name__))
class TextField(ParentField):
    def __init__(self):
        pass
    def __get_column_sql_check__(self):
        """
        Выдаёт SQL код для проверки существования нужного столбца таблицы
        """
        raise NotImplementedError("Must be replaced in children class")
    def __get_column_sql_create__(self):
        """
        Выдаёт SQL код для создания нужного столбца таблицы
        """
        return "Create TextField for {0},\n".format((self.__attr_name__))
class DataField(ParentField):
    def __init__(self):
        pass
    def __get_column_sql_check__(self):
        """
        Выдаёт SQL код для проверки существования нужного столбца таблицы
        """
        raise NotImplementedError("Must be replaced in children class")
    def __get_column_sql_create__(self):
        """
        Выдаёт SQL код для создания нужного столбца таблицы
        """
        return "Create DataFiled for {0},\n".format((self.__attr_name__))