# -*- coding:utf-8 -*-
# coding=<utf8>

"""
start_deploy_server(branch='', directory='',github='', project=''):
change_server_test_to_master(directory='', project='', github=''):
change_source_test_to_master(branch=''):
deploy_server(directory='', project=''):
new_branch(branch='') - создаёт новую ветку
switch_branch(branch='') - переключается на указанную ветку
commit_branch(branch='') - коммитит ветку
push_commit(branch='') - отправляет ветку на сервер репозитория
start_deploy_server(branch='', directory='',github='', project='') - устанавливает сервер с указанной веткой

./manage.py schemamigration southtut --auto

fab -f mjcc_task_deployment.py new_branch:branch=bug2

fab -f mjcc_task_deployment.py switch_branch:branch=bug2

fab -f mjcc_task_deployment.py commit_branch:branch=bug2

fab -f mjcc_task_deployment.py south_migrate:app=todoes,project=tasks

fab -f mjcc_task_deployment.py deploy_server:directory=tasks,project=tasks,type_of_server=test

fab -f mjcc_task_deployment.py start_deploy_server:branch=bug2,directory=tasks,project=tasks,type_of_server=test,github=https://github.com/Ishayahu/MJCC-tasks.git

fab -f mjcc_task_deployment.py change_source_test_to_master:branch=bug2
"""

from __future__ import with_statement
from fabric.api import *
from fabric.contrib.console import confirm
# Словарь паролей
env.passwords={'ishayahu@192.168.1.25':'aA111111','ishayahu@192.168.1.183':'aA111111'}
env.shell='/bin/csh -c'
# папка с fab файлом
deployment_folder = '/usr/home/ishayahu/docsrv/scripts/MJCC-tasks/'
# папка с исходниками в локальном git репозитории
source_folder = '/usr/home/ishayahu/docsrv/scripts/MJCC-tasks/'
# Сервера для выполнения задачи
servers= {'test':['ishayahu@192.168.1.183',],
          'deploy' : ['ishayahu@192.168.1.25',]
          }

servers_ip= {'test':['192.168.1.183',],
          'deploy' : ['192.168.1.25',]
          }
bd_ip= {'test':['192.168.1.136',],
          'deploy' : ['192.168.1.24',]
          }

def south_migrate(app,project):
    run('pwd')
    with cd(project):
        run('pwd')
        run('python manage.py schemamigration %s --auto' % app)
        ans = prompt('Продолжаем?', default='Д')
        if ans == 'Д':
            run('python manage.py migrate '+app)
        
def new_branch(branch=''):
    """
    Создаёт новую ветку branch
    """
    if not branch:
        print "Вы должны указать ветку, которую хотите создать"
        return
    local ('git branch %s' % branch)
    local ('git checkout %s' % branch)
    
def switch_branch(branch=''):
    """
    Переключается на ветку branch
    """
    if not branch:
        print "Вы должны указать ветку, на которую хотите переключиться"
        return
    local ('git checkout %s' % branch)


def make_and_send_settings(host='',port='5432',email_host='',email_port='',email_user='',email_password='',where_to_place='',srv_ip=''):
    """
    Создаёт файл settings.py локально, выгружает его каталог where_to_place. Для того, чтобы настройки и пароли не хранились на github
    host - IP сервера БД, сервер именно PostgreSQL
    port - номер порта
    email_host - smtp сервер для отправки уведомлений по мылу
    email_port - порт smtp сервера
    email_user - логин для smtp сервера
    email_password - пароль smtp сервера
    where_to_place - место, куда выгружать файл setting.py
    """
    # Шаблон файла настроек. SECRET_KEY вынесен в отдельню строку из-за знаков %, которые в данном случае будут интерпретироваться как места для замены операцией форматирования %
    # Сразу же подставляем туда значения
    template="""
# Django settings for tasks project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'tasks',                      # Or path to database file if using sqlite3.
        'USER': 'puser',                      # Not used with sqlite3.
        'PASSWORD': 'planrabot',                  # Not used with sqlite3.
        'HOST': '%s',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '%s',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
#TIME_ZONE = 'America/Chicago'
TIME_ZONE = 'Europe/Moscow'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = '/usr/home/ishayahu/tasks/todoes/files/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = 'http://%s:8080/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)
""" % (host,port,srv_ip) + """
# Make this unique, and don't share it with anybody.
SECRET_KEY = 'b%2gll0&rnk^8vw$+s=#05vc&%=b^n4fi1r24is=vsz4ajgggr'
"""  + """

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)
TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages")
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'tasks.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    "/usr/home/ishayahu/tasks/tasks/templates",
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.auth',
    
    # 'django.contrib.sites',
    'django.contrib.messages',
    # 'django.contrib.staticfiles',
    #'tasks.todoes', # Django 1.3
    'todoes', # Django 1.4
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'south',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

# For e-mails
# EMAIL_USE_TLS = True
# EMAIL_HOST = 'smtp.mail.ru'
# EMAIL_PORT = 465
# EMAIL_HOST_USER = 'meoc-it@mail.ru'
# EMAIL_HOST_PASSWORD = 'Elishevochka2371'

EMAIL_USE_TLS = True
EMAIL_HOST = "%s"
EMAIL_PORT = %s
EMAIL_HOST_USER = "%s"
EMAIL_HOST_PASSWORD = '%s'

SESSION_EXPIRE_AT_BROWSER_CLOSE = True

    """ % (email_host,email_port,email_user,email_password)
    # Создаём файл settings.py и записываем в него содержимое
    open('settings.py','w').write(template)
    # Переходим в папку, где лежит созданный файл (там, где запускается скрипт)
    with lcd(deployment_folder):
	# Проверяем локальную и удалённую папку
	local('pwd')
	run('pwd')
	run('cd '+where_to_place)
	run('pwd')
	# Выгружаем файл с настройками
	put('settings.py',where_to_place)
	# Удаляем локальный файл, ибо нафига
	local('rm settings.py')

def start_deploy_server(branch='', directory='',github='', project='',type_of_server='',e_mail='',e_psswd=''):
    """
    Задача, подготавливающая сервер к разворачиванию на нём бранча branch проекта (не приложения) project. Код из репозитория github будет выгружаться в каталог directory
    """
    # Создаём каталог, куда будут разворачиваться исходники
    env.hosts=servers[type_of_server][0]
    ans = prompt('Разворачиваем на хосте '+str(env.hosts), default='Д')
    if ans == 'Д':
        # надо проверить, есть ли папка, и если есть - удалить её
        run('rm -rdf %s' % directory)
        run('mkdir %s' % directory)
        # Проверяем, где находимся
        run('pwd')
        # Переходим в созданный каталог
        with cd(directory):
            # Инициализируем репозиторий
	    run('git init')
	    # Добавляем удалённый репозиторий github под имененм origin и настраиваем отслеживание на бранч branch
	    run('git remote add -t %s origin %s' % (branch, github))
	    # Получаем файлы
	    run('git fetch')
	    # Переключаемся с master на branch
	    run('git checkout %s' % branch)
	    # Переходим в каталог проекта и создаём там файл с настройками
	    with cd(project):
                srv_ip=servers_ip[type_of_server]
                bd_ip=bd_ip[type_of_server]
                if type_of_server=='deploy':
                    make_and_send_settings(host=bd_ip,port='5432',email_host='smtp.gmail.com',email_port='25',email_user=e_mail,email_password=e_psswd,where_to_place='~/tasks/tasks/',srv_ip=srv_ip)
                if type_of_server=='test':
                    make_and_send_settings(host=bd_ip,port='5432',email_host='smtp.gmail.com',email_port='25',email_user=e_mail,email_password=e_psswd,where_to_place='~/tasks/tasks/',srv_ip=srv_ip)
	    # Запускаем сервер для проверки
	    #run('python manage.py runserver 0.0.0.0:8080')
	
def deploy_server(directory='', project='',type_of_server='',e_mail='',e_psswd=''):
    """
    Обновляем код на тестовом сервере
    """
    # Переходим в каталог, где хранится код
    env.hosts=servers[type_of_server][0]
    ans = prompt('Разворачиваем на хосте '+str(env.hosts), default='Д')
    if ans == 'Д':
        print (directory, project)
        with cd(directory):
	    # Получаем обновления кода для отслеживаемой ветки
	    run('git pull')
	    # Переходим в каталог проекта и создаём файл с настройками
	    with cd(project):
                srv_ip=servers_ip[type_of_server]
                bd_ip=bd_ip[type_of_server]
                if type_of_server=='deploy':
                    make_and_send_settings(host=bd_ip,port='5432',email_host='smtp.gmail.com',email_port='25',email_user=e_mail,email_password=e_psswd,where_to_place='~/tasks/tasks/',srv_ip=srv_ip)
                if type_of_server=='test':
                    make_and_send_settings(host=bd_ip,port='5432',email_host='smtp.gmail.com',email_port='25',email_user=e_mail,email_password=e_psswd,where_to_place='~/tasks/tasks/',srv_ip=srv_ip)

def commit_branch(branch=''):
    """
    Подтвеждаем нужный вариант кода (бранч). При подтверждении всё добавляется и подтверждается автоматом. Если что-то не устравивает - решите сперва проблему вручную
    """
    # Переходим в каталог с локальным исходным кодом
    with lcd(source_folder):
	# Переключаемся на тестовый бранч
	local('git checkout %s' % branch)
	# Смотрим статус
	local('git status')
	# Продолжаем?
	ans = prompt('Продолжить?', default='Д')
	if ans == 'Д':
	    # Добавляем все файлы в коммит
	    local('git add .')
	    # Получаем сообщение для коммита
	    message = prompt('Введите сообщение для коммита')
	    # Коммитим
	    local("git commit -m '%s'" % message)
	    # Выгружаем на сервер
	    local("git push origin %s" % branch)
	    
def push_commit(branch=''):
    """
    Выгружаем на удалённый сервер нужный бранч без коммита
    """
    # Переходим в локальный каталог с исходным кодом
    with lcd(source_folder):
	# Переключаемся на нужный бранч
	local('git checkout %s' % branch)
	# Статус
	local('git status')
	# Всё ок?
	ans = prompt('Продолжить?', default='Д')
	if ans == 'Д':
	    # Выгружаем код
	    local("git push origin %s" % branch)
	    
def change_source_test_to_master(branch=''):
    """
    Сливаем тестовый бранч и мастер и выгружаем на сервер кода. То есть перемещаем метку мастер на тестовый код
    """
    # Переходим в каталог с локальным исходным кодом
    with lcd(source_folder):
	# Переключаемся на мастера
	local('git checkout master')
	# Сливаем тестовый код с мастером
	local('git merge %s' % branch)
	# Выгружаем код
	local('git push origin master')
	
def change_server_test_to_master(directory='', project='', github='',e_mail='',e_psswd=''):
    """
    Делаем из тестового сервера продакшн.
    """
    # Переходим в каталог с исходниками
    with cd(directory):
	# Удаляем текущее отслеживание
	run('git remote rm origin')
	# Добавляем отслеживание мастера
	run('git remote add -t master origin %s' % github)
	# Скачиваем код
	run('git pull')
	# Переключаемся на мастер для гарантии
	run('git checkout master')
	# Переходим в каталог проекта и создаём файл с настройками
	with cd(project):
            srv_ip=srv_ip=servers_ip['deploy']
            bd_ip=bd_ip['deploy']
            make_and_send_settings(host=bd_ip,port='5432',email_host='smtp.gmail.com',email_port='25',email_user=e_mail,email_password=e_psswd,where_to_place='~/tasks/tasks/',srv_ip=srv_ip)


	