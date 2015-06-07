# -*- coding:utf-8 -*-
# coding=<utf8>
"""
Этот модуль предоставляет класс ModelParent, от которого можно создать свои модели
для работы с БД sqlite.
"""
__author__ = 'Ishayahu'
from sqlite_models.fields import *
import inspect

class ParentModel(object):
    """
    Родительский класс для создания моделей для работы с БД
    Например, должен поддерживаться такой класс:

    class Cashless():
        month_year
        remains

    a = Cashless()
    c = a.get(month_year = '09/2013')
    c.remains -= 100
    c.save()
    """
    def __init__(self):
        """
        Констурктор создаёт отображение модели на записи в БД. То есть, делает интроспецкию по полям в определении
        класса и где-то их сохраняет для дальнейшено использования
        """
    def __create(self):
        """
        Создаёт соответствующую таблицу в БД. Нужен при инициализации
        """
    def get(self):
        """
        Получить один экзмепляр из БД по заданному параметру. Если несклько - выдать ошибку
        """
    def filter(self):
        """
        Получить несколько экзмепляров из БД по заданному параметру
        """
    def all(self):
        """
        Получить все записи из БД из соответствующей таблицы
        """
    def save(self):
        """
        Сохраняет изменения в БД
        """
    @staticmethod
    def __pprint__(text):
        """
        Делает из текста в много строк с пробелами текст в одну строку, удаляя все лишние пробелы в начале
        и конце каждой строки

        >>> a='''
        ...    CREATE TABLE {0} (
        ...    {1}
        ...    );
        ...    '''
        >>> ParentModel().__pprint__(a)
        'CREATE TABLE {0} ({1});'
        """
        return ''.join([line.strip() for line in text.strip().split('\n')])
    def __get_sql_check_table__(self):
        """
        Выдаёт SQL код для проверки существования нужной таблицы
        """
        pass
    def __get_sql_create_table__(self):
        """
        Выдаёт SQL код для создания нужной таблицы
        CREATE TABLE test1 (
            id    INTEGER PRIMARY KEY AUTOINCREMENT,
            int   INTEGER NOT NULL,
             month DATE
        );

        >>> class TestModel(ParentModel):
        ...     text = TextField()
        ...     integer = IntegerField()
        >>> a = TestModel()
        >>> print a.__get_sql_create_table__()
        CREATE TABLE TestModel (Create IntegerField for TestModel,Create TextField for TestModel);

        """
        #TODO: надо исправить тест - должно ожидаться корректное SQL выражение
        raise NotImplementedError ("надо исправить тест - должно ожидаться корректное SQL выражение")
        template = """
        CREATE TABLE {0} (
            {1}
        );
        """
        table_name = self.__class__.__name__
        table_fields=''
        self.__add_attr_name__()
        result = ''
        for k,v in self.attr_dict:
            if issubclass(v.__class__,ParentField):
                table_fields +=v.__get_column_sql_create__()
        template = template.format(table_name,table_fields.strip()[:-1])
        return self.__pprint__(template)
    def __add_attr_name__(self):
        """
        Добавляет в каждый аттрибут, являющийся потомком ParentField (то есть, полем модели) атрибут __attr_name__
        с именем класса, в котором он определён

        >>> class TestModel(ParentModel):
        ...     text = TextField()
        ...     integer = IntegerField()
        >>> a = TestModel()
        >>> a.__add_attr_name__()
        >>> print a.text.__attr_name__
        TestModel
        >>> print a.integer.__attr_name__
        TestModel
        """
        self.attr_dict = inspect.getmembers(self)
        for k,v in self.attr_dict:
            if issubclass(v.__class__,ParentField):
                v.__attr_name__ = str(self.__class__.__name__)