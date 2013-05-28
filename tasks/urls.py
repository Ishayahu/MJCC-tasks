# -*- coding:utf-8 -*-
# coding=<utf8>

from django.conf.urls.defaults import patterns, include, url
import todoes.views as views
from django.contrib import admin
from django.contrib.auth.views import login, logout
from django.conf import settings
admin.autodiscover()

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
urlpatterns = patterns('',
    # �������� �����
    url(r'^tasks/$', views.tasks),
    # �������� ���� �����
    url(r'^all_task/$', views.all_tasks),

# ������� ������
    url(r'^new_ticket/$', views.new_ticket),
    url(r'^edit/([^/]+)/$', views.edit_task),
    # �������� / ������ �������� ������
    url(r'^close/([^/]+)/$', views.close_task),
    url(r'^unclose/([^/]+)/$', views.unclose_task),
    # ������������� ���������� ������
    url(r'^confirm/([^/]+)/$', views.confirm_task),
# ������������� ������    
    # �������� ������������� ������
    url(r'^new_regular_ticket/$', views.new_regular_ticket),
    # �������������� ������������� ������
    url(r'^edit_regular/([^/]+)/$', views.edit_regular_task),
    # ������� ��� ��������� ������������� ������
    url(r'^regular_task_done/([^/]+)/$', views.regular_task_done),
# ����� ��� ���� �����    
    url(r'^task/([^/]+)/(\d+)/$', views.task),
    # ��������� ����������� ������������� ������
    # �������� ������������� ������
    url(r'^deleted_tasks/$', views.deleted_tasks),
    url(r'^delete/([^/]+)/(\d+)/$', views.delete_task),
    url(r'^completle_delete/([^/]+)/(\d+)/$', views.completle_delete_task),
    url(r'^completle_delete_all/$', views.completle_delete_all),
    url(r'^undelete/([^/]+)/(\d+)/$', views.undelete_task),
    url(r'^add_children_task/([^/]+)/(\d+)/$', views.add_children_task),
    # http://192.168.1.157:8080/move_to_call/47 - ��������� ��������� �� "������"
    url(r'^move_to_call/([^/]+)/(\d+)/$', views.move_to_call),
    # http://192.168.1.157:8080/set_reminder/47 - ��������� ����������� ��� ������
    url(r'^set_reminder/([^/]+)/(\d+)/$', views.set_reminder), 
# ��� ��������������:
    url(r'^users/', views.get_all_logged_in_users),
    url(r'^tasks/to/([^/]+)/$', views.to),
    
    url(r'^accounts/$', login),
    url(r'^accounts/login/$', login),
    url(r'^accounts/register/$', views.register),
    url(r'^accounts/logout/$', logout),
    url(r'^accounts/profile/$', views.profile),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    # �������� 
    url(r'^$', views.tasks),

)
if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
