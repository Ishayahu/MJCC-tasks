# -*- coding:utf-8 -*-
# coding=<utf8>

#from django.conf.urls.defaults import patterns, include, url
from django.conf.urls import patterns, url, include
import todoes.views
import todoes.api
import assets.views
import save_state.api
import assets.test_view
import assets.api
import logs.views
import user_settings.views
import djlib
from django.contrib import admin
from django.contrib.auth.views import login, logout, password_change,password_change_done
from django.conf import settings
admin.autodiscover()

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
urlpatterns = patterns('',
    # просмотр задач
    url(r'^tasks/$', todoes.views.tasks),
    # просмотр всех задач по страницам
    url(r'^all_task/([^/]+)/$', todoes.views.all_tasks),
    # просмотр сообщения
    url(r'^messages/show/(\d+)/$', todoes.views.messages_show_message),


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
    url(r'^users/$', todoes.views.get_all_logged_in_users),
    url(r'^users/activity_history/([^/]+)/([^/]*)/$', todoes.views.get_user_activity_history),
    url(r'^tasks/to/([^/]+)/$', todoes.views.to),
    # добавление сообщения
    url(r'^messages/add/$', todoes.views.messages_add),
# APT для задач
    # Получение человеческого представления hardcore-style при
    # создании регулярной задачи
    url(r'^api/crontab_to_russian/([^/]+)/$', todoes.api.crontab_to_human),


    url(r'^accounts/$', login),
    url(r'^login/$', login),
    url(r'^accounts/login/$', login),
    url(r'^test/password2/$', password_change),
    url(r'^password_change_done/$', password_change_done),
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
    url(r'^bill/cash/add/$', assets.views.bill_cash_add),
    # Добавление счёта, где указывается плата + сколько там чего
    url(r'^bill/cashless/add/$', assets.views.bill_cashless_add),
    # Просмотр списка счетов, как по налу так и по безналу с фильтрами
    url(r'^all_bills/$', assets.views.all_bills),
    # Просмотр конкретного чека/счёта - тип,id
    url(r'^bill/show/([^/]+)/(\d*)/$', assets.views.show_bill),
    # Список всех удалённых чеков/счётов
    url(r'^all_deleted_bills/$', assets.views.all_deleted_bills),
    # Просмотр активов по категориям
    url(r'^assets_by_type/(\d*)/$', assets.views.assets_by_type),
    # Просмотр актива
    url(r'^asset/(\d*)/$', assets.views.asset_view),

# API для работы с активами
    # Выдача формы добавления актива, в качестве параметра - категория актива, префикс к имени полей формы (число)
    url(r'^api/get_asset_add_form/(\d+)/(\d*)/$', assets.api.get_asset_add_form),
    # Выдача заголовка для формы добавления актива
    url(r'^api/get_asset_add_form_header/$', assets.api.get_asset_add_form_header),
    # Выдача скрипта для формы добавления актива
    url(r'^api/get_asset_add_form_script/(\d+)/(\d*)/$', assets.api.get_asset_add_form_script),
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
    # Удалить конкретный чек/счёт - тип,id
    url(r'^api/bill/full_delete/([^/]+)/(\d*)/$', assets.api.full_delete_bill),
    url(r'^bill/full_delete/([^/]+)/(\d*)/$', assets.api.full_delete_bill),
    # Получение списка активов по категориям
    url(r'^api/assets_by_type/(\d+)/$', assets.api.assets_by_type),
    # Удаление актива - id актива, id категории к которой вернуться при ошибки
    url(r'^api/asset/delete/(\d+)/(\d+)/$', assets.api.asset_delete),
    # Редактирование актива - id актива
    url(r'^api/asset/edit/(\d+)/$', assets.api.asset_edit),
    # получение json списка моделей для типа активов- тип актива
    url(r'^api/asset_types/models/get/(\d+)/$', assets.api.get_models_list_json),
    # Получение формы для добавления нового типа актива
    url(r'^api/asset_types/type/add/$', assets.api.get_new_asset_type_add_form),
    # Сохраняем новый тип актива
    url(r'^api/asset_types/type/save/$', assets.api.get_new_asset_type_save),
    # Редактирование актива - id актива
    url(r'^api/asset/save_edited/(\d+)/$', assets.api.asset_save_edited),
    # Получаем форму для добавления актива - id типа актива, имя модели
    url(r'^api/get_new_model_add_form/(\d+)/(.+)/$', assets.api.get_new_asset_model_add_form),
    # Сохраняем новую модель актива- id типа актива
    url(r'^api/asset_types/model/save/(\d+)/$', assets.api.save_new_model),
    # Меняем пройденные этапы для счёта по безналу - номер счёта, название этапа, включить/выключить (провести/отменить проведение), послать таблицу или перенаправить страницу?
    url(r'^api/bill/cashless/edit/stages/(\d+)/([^/]+)/(\d+)/(\d+)$', assets.api.cashless_edit_stages),
# API для выдачи JSON
    # Список моделей актива для типа актива - id типа актива
    url(r'^api/json/get/models/(\d+)/$', assets.api.json_models),
    # Получение цены и срока гарантии для последнего купленного актива этой модели этой фирмы. Данные передаются через POST запрос
    url(r'^api/json/get/price_and_warranty/$', assets.api.json_price_and_warranty),
# Логирование и т.п.
    url(r'^show_last_logs/(\d*)/$', logs.views.show_last_logs),
# API для сохранения статусов
    # сохранение статуса через http
    url(r'^api/state/save_by_http/([^/]+)/([^/]+)/([^/]+)/(\d+)/([^/]*)/(\d+)/([^/]+)/$',
        save_state.api.save_by_http),
    # просмотр статусов
    url(r'^api/state/show_states/([^/]+)/$',
        save_state.api.show_states),



# Настройки
    url(r'^settings/$', user_settings.views.show_settings),
    # Сохранить настройку после редактирования
    url(r'^api/setting/save/([^/]+)/([^/]+)/$', user_settings.views.save_edited_setting),
    # Выдать форму для редактирования настроек, берущихся из БД
    url(r'^api/setting/edit_from_bd/([^/]+)/([^/]+)/$', user_settings.views.edit_from_bd),
    # Сохранить настройку из БД после редактирования
    url(r'^api/setting/save_from_bd/([^/]+)/([^/]+)/$', user_settings.views.save_from_bd),


# Тестированание
    # url(r'^test/bill/add/$', assets.test_view.bill_add),
    url(r'^test/test_cm/$', assets.test_view.test_cm),
    # url(r'^test/password/$', assets.test_view.password),
    # (r'^change-password/$', 'django.contrib.auth.views.password_change'), 
    # (r'^password-changed/$', 'django.contrib.auth.views.password_change_done'),
    url(r'^test/cashless_maintenance/$', assets.test_view.cashless_maintenance),
    
    (r'^i18n/', include('django.conf.urls.i18n')),
)
if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
