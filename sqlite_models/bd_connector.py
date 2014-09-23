# -*- coding:utf-8 -*-
# coding=<utf8>


import sqlite3
from user_settings.settings import sqlite_file

class BDConnector():
    """
    Класс для подключения к БД sqlite, Если получает аргумент 'd', то работает в режиме отладки
    при записи, то есть, ничего в файл не записывается, а выводится в stdout
    """
    def __init__(self,if_debug='o'):
        self.debug=False
        self.con=sqlite3.connect(sqlite_file)
        self.cursor=self.con.cursor()
        if if_debug=='d':
                self.debug=True
    def check(self, models, create):
        """
        Проверяет, созданы ли таблицы, для переданных моделей, вызывая их метод __get_sql_check_table, для
        получения кода SQL для проверки таблиц. Если второй аргумент равен True, то вызываются их
        методы __get_sql_create_table для создания этих таблиц
        """

    # def execute(self, sql):
    #     self.cursor.execute(sql)
    # def __del__(self):
    #     del self.cursor
    #     del self.con
    # def print_select(self,SELECT,number):
    #     """
    #     print result of SELECT querry to stdout
    #     number - number of selecting columns in select statemetn
    #     """
    #     self.cursor.execute(SELECT)
    #     var=list(range(number))
    #     for var in self.cursor:
    #         print (';'.join((str(k) for k in var)))
    # def get_select(self,SELECT,number):
    #     """
    #     print result of SELECT querry to stdout
    #     number - number of selecting columns in select statemetn
    #     """
    #     self.cursor.execute(SELECT)
    #     var=list(range(number))
    #     for var in self.cursor:
    #         if number==1:
    #             return str(var[0])
    #         else:
    #             return ';'.join((str(k) for k in var))
    # def print_update_mass(self,UPDATE):
    #     """
    #     print result of UPDATE querry to stdout
    #     """
    #     print (UPDATE)
    #     self.cursor.execute(UPDATE)
    #     self.con.commit()
    #     print ('done')
    # def update_with_confirm(self,SELECT,UPDATE,file):
    #     """
    #     Выводит запрос SELECT, который выбирает все записи, которые должны быть изменены, сохраняет их в файл file. После чего выполняет запрос UPDATE. Оба запроса тоже записываются в file
    #     """
    #     f = open(file,'w')
    #     print (SELECT)
    #     f.write(SELECT+'\n\n')
    #     self.cursor.execute(SELECT)
    #     for line in self.cursor:
    #         f.write(str(line)+'\n')
    #     a = input("Продолжаем? Y/N")
    #     if a.upper()=='Y':
    #         self.cursor.execute(UPDATE)
    #         self.con.commit()
    #         print (UPDATE)
    #         f.write('\n\n'+UPDATE)
    #     print ('done')
    #
    # def write_select(self,SELECT,number,filename,HEADER=None):
    #     """
    #     write result of SELECT querry to file with filename
    #     number - number of selecting columns in select statemetn
    #     """
    #     file=open(filename,'w',encoding='utf8')
    #     if HEADER:
    #         file.write(HEADER)
    #     print (SELECT)
    #     res=self.cursor.execute(SELECT)
    #     print ('\n\n',res,'\n\n')
        # var=list(range(number))
        # print (self.cursor.arraysize,'\n',len(var),self.cursor.rowcount)
        # for var in self.cursor:
        #     file.write(';'.join((str(k).replace('\n',' ') for k in var))+'\n')
            # file.write(';'.join((str(k).replace('\n',' ').replace('\r',' ') for k in var))+'\n')
        # file.close()
    # def write_select_region(self,SELECT,number,filename,HEADER,REGION):
    #     """
    #     write result of SELECT querrys, in each querry used one of string from LIST, to file with filename
    #     number - number of selecting columns in select statemetn
    #     """
    #     file=open(filename,'w',encoding='utf8')
    #     if HEADER:
    #         file.write(HEADER)
    #     res=self.cursor.execute(SELECT.format(string.upper()))
    #     print ('\n\n',res,'\n\n')
        # var=list(range(number))
        # print (self.cursor.arraysize,'\n',len(var),self.cursor.rowcount)
        # for var in self.cursor:
        #     file.write(';'.join((str(k).replace('\n',' ') for k in var))+'\n')
            # print ('*',end="")
            # file.write(';'.join((str(k).replace('\n',' ').replace('\r',' ') for k in var))+'\n')
        # file.close()
    # def write_select_list(self,SELECT,number,filename,HEADER,LIST):
    #     """
    #     write result of SELECT querrys, in each querry used one of string from LIST, to file with filename
    #     number - number of selecting columns in select statemetn
    #     """
    #     file=open(filename,'w',encoding='utf8')
    #     if HEADER:
    #         file.write(HEADER)
    #     file.close()
    #     for string in LIST:
    #         file=open(filename,'a',encoding='utf8')
    #         print (string.upper())
    #         res=self.cursor.execute(SELECT.format(string.upper()))
    #         print ('\n\n',res,'\n\n')
            # var=list(range(number))
            # print (self.cursor.arraysize,'\n',len(var),self.cursor.rowcount)
            # for var in self.cursor:
            #     file.write(';'.join((str(k).replace('\n',' ') for k in var))+'\n')
                # print ('*',end="")
                # file.write(';'.join((str(k).replace('\n',' ').replace('\r',' ') for k in var))+'\n')
            # file.close()
    # def write_select_if(self,SELECT,number,stmt,stmtNumber,filename,inline=False,inlineNumber=0,sep=',',quote=''):
    #     """
    #     write result of SELECT querry filtering with stmt condition to file with filename
    #     number - number of selecting columns in select statemetn
    #     stmt - condition
    #     stmtNumber - number of column to witch condition must be aplly
    #     inline - if True, all output is placed in one string
    #     inlineNumber - number of column witch is placed to file if inline=True
    #     sep - separator for values if inline=True
    #     quote - to quote values in inline output give in this argument quotation mark
    #     """
    #     file=open(filename,'w')
    #     self.cursor.execute(SELECT)
    #     var=list(range(number))
    #     for var in self.cursor:
    #         if self.debug: print (var[stmtNumber-1])
    #         if self.debug: print (var[stmtNumber-1]==stmt)
    #         if self.debug:
    #             file.write(';'.join((str(k).replace('\n',' ').replace('\r',' ') for k in var))+'\n'+stmt+'\n')
    #         else:
    #             if not inline:
    #                 if stmt in var[stmtNumber-1]:
    #                     file.write(';'.join((str(k).replace('\n',' ').replace('\r',' ') for k in var))+'\n')
    #             else:
    #                 if stmt in var[stmtNumber-1]:
    #                     file.write(quote+str(var[inlineNumber])+quote+sep)
    #     file.close()
#