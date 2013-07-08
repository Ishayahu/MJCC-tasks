# -*- coding:utf-8 -*-
# coding=<utf8>

from django.conf.urls.defaults import patterns, include, url
import todoes.views 
import assets.views
import assets.api
import logs.views
import djlib
from django.contrib import admin
from django.contrib.auth.views import login, logout
from django.conf import settings
admin.autodiscover()

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
urlpatterns = patterns('',
    # просмотр задач
    url(r'^tasks/$', todoes.views.tasks),
    # просмотр всех задач
    url(r'^all_task/$', todoes.views.all_tasks),

# обычные задачи
    url(r'^new_ticket/$', todoes.views.new_ticket),
    url(r'^edit/([^/]+)/$', todoes.views.edit_task),
    # закрытие / отмена закрытия заявки
    url(r'^close/([^/]+)/$', todoes.views.close_task),
    url(r'^unclose/([^/]+)/$', todoes.views.unclose_task),
    # подтверждение выполнения задачи
    url(r'^confirm/([^/]+)/$', todoes.views.confirm_task),
# повторяющиеся задачи    
    # создание повторяющейся задачи
    url(r'^new_regular_ticket/$', todoes.views.new_regular_ticket),
    # редактирование повторяющейся задачи
    url(r'^edit_regular/([^/]+)/$', todoes.views.edit_regular_task),
    # отметка как сделанная повторяющейся задачи
    url(r'^regular_task_done/([^/]+)/$', todoes.views.regular_task_done),
# общее для всех задач    
    url(r'^task/([^/]+)/(\d+)/$', todoes.views.task),
    # установка напоминалки повторяющейся задачи
    # удаление повторяющейся задачи
    url(r'^deleted_tasks/$', todoes.views.deleted_tasks),
    url(r'^delete/([^/]+)/(\d+)/$', todoes.views.delete_task),
    url(r'^completle_delete/([^/]+)/(\d+)/$', todoes.views.completle_delete_task),
    url(r'^undelete/([^/]+)/(\d+)/$', todoes.views.undelete_task),
    url(r'^add_children_task/([^/]+)/(\d+)/$', todoes.views.add_children_task),
    # http://192.168.1.157:8080/move_to_call/47 - изменение категории на "Звонки"
    url(r'^move_to_call/([^/]+)/(\d+)/$', todoes.views.move_to_call),
    # http://192.168.1.157:8080/set_reminder/47 - установка напоминания для задачи
    url(r'^set_reminder/([^/]+)/(\d+)/$', todoes.views.set_reminder), 
# Для администратора:
    url(r'^users/', todoes.views.get_all_logged_in_users),
    url(r'^tasks/to/([^/]+)/$', todoes.views.to),

    
    url(r'^accounts/$', login),
    url(r'^accounts/login/$', login),
    url(r'^accounts/register/$', todoes.views.register),
    url(r'^accounts/logout/$', logout),
    url(r'^accounts/profile/$', todoes.views.profile),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', todoes.views.tasks),

# изменение языка интерфейса
    url(r'^language/([^/]+)/$', djlib.multilanguage_utils.change_language),

# Работа с активами
    # Добавление чека, где указывается плата + сколько там чего
    url(r'^bill/add/$', assets.views.bill_add),
    # Просмотр списка счетов, как по налу так и по безналу с фильтрами
    url(r'^all_bills/$', assets.views.all_bills),
    # Просмотр конкретного чека/счёта - тип,id
    url(r'^bill/show/([^/]+)/(\d*)/$', assets.views.show_bill),
    # Список всех удалённых чеков/счётов
    url(r'^all_deleted_bills/$', assets.views.all_deleted_bills),
    # Просмотр активов по категориям
    url(r'^assets_by_type/(\d*)/$', assets.views.assets_by_type),
# API для работы с активами
    # Выдача формы добавления актива, в качестве параметра - категория актива, префикс к имени полей формы (число)
    url(r'^api/get_asset_add_form/(\d+)/(\d*)/$', assets.api.get_asset_add_form),
    # Выдача списка поставщиков, в качестве параметра - тот поставщик, который должен быть указан, name
    url(r'^api/get_contractors_list/([^/]*)/$', assets.api.get_contractors_list),
    # Выдача формы добавления поставщика, в качестве параметра - название
    url(r'^api/get_new_contractor_add_form/([^/]*)/$', assets.api.get_new_contractor_add_form),
    # Сохраняем нового поставщика
    url(r'^api/save_new_contractor/$', assets.api.save_new_contractor),    
    # Получаем список типов активов, в качестве парамета - id выбранного
    url(r'^api/get_asset_type_list/(\d*)/$', assets.api.get_asset_type_list),    
    # Пометить конкретный чек/счёт к удалению - тип,id
    url(r'^api/bill/delete/([^/]+)/(\d*)/$', assets.api.mark_as_deleted_bill),
    url(r'^bill/delete/([^/]+)/(\d*)/$', assets.api.mark_as_deleted_bill),
    # Пометить конкретный чек/счёт к удалению - тип,id
    url(r'^api/bill/full_delete/([^/]+)/(\d*)/$', assets.api.full_delete_bill),
    url(r'^bill/full_delete/([^/]+)/(\d*)/$', assets.api.full_delete_bill),
    # Получение списка активов по категориям
    url(r'^api/assets_by_type/(\d+)/$', assets.api.assets_by_type),
    # Удаление актива - id актива, id категории к которой вернуться при ошибки
    url(r'^api/asset/delete/(\d+)/(\d+)/$', assets.api.asset_delete),
    # Редактирование актива - id актива
    url(r'^api/asset/edit/(\d+)/$', assets.api.asset_edit),
    
# Логирование и т.п.
    url(r'^show_last_logs/(\d*)/$', logs.views.show_last_logs),
)
if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
