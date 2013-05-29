# -*- coding:utf-8 -*-
# coding=<utf8>

from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render_to_response
import datetime
from todoes.models import Note, Resource, File, Person, Task, ProblemByWorker, ProblemByUser, Categories, RegularTask, Activity
from todoes.forms import NewTicketForm, NoteToTicketAddForm, UserCreationFormMY, TicketClosingForm, TicketConfirmingForm, TicketEditForm,TicketSearchForm, NewRegularTicketForm, EditRegularTicketForm, File_and_NoteToTicketAddForm
from django.contrib.auth.decorators import login_required
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.template import RequestContext
from itertools import chain

from djlib.cron_utils import decronize, crontab_to_russian, generate_next_reminder
from djlib.text_utils import htmlize
from djlib.acl_utils import acl
from djlib.user_tracking import set_last_activity_model, get_last_activities
from djlib.mail_utils import send_email_alternative

from user_settings import server_ip, admins, admins_mail
from user_settings import assets_url_not_to_track as url_not_to_track
from user_settings import assets_url_one_record as url_one_record
