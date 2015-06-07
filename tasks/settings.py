
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
        'HOST': '172.22.0.123',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '5432',                      # Set to empty string for default. Not used with sqlite3.
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

LANGUAGE_CODE = 'ru'
# LANGUAGE_CODE = 'en-us'
gettext = lambda s: s

LANGUAGES = (
    ('ru', gettext('Russian')),
    ('en', gettext('English')),
)


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
MEDIA_URL = 'http://172.22.0.124:8080/media/'

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

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'b%2gll0&rnk^8vw$+s=#05vc&%=b^n4fi1r24is=vsz4ajgggr'


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
    'assets', # assets bd
    'logs', # Logging
    'user_settings', # Settings
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

    # 'filters': {
        # 'require_debug_false': {
            # '()': 'django.utils.log.RequireDebugFalse'
        # }
    # },

    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'

        },
        # 'console':{
            # 'level':'DEBUG',
            # 'filters': ['require_debug_false'],
            # 'class':'logging.StreamHandler',
        # },

    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },

        # 'django.db.backends' : {
            # 'handlers': ['console'],
            # 'level': 'DEBUG',
            # 'propagate': True,
        # }
    }
}

# For e-mails
# EMAIL_USE_TLS = True
# EMAIL_HOST = 'smtp.mail.ru'
# EMAIL_PORT = 465
# EMAIL_HOST_USER = 'meoc-it@mail.ru'
# EMAIL_HOST_PASSWORD = 'Elishevochka2371'

EMAIL_USE_TLS = True
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 25

EMAIL_HOST_USER = "mjcc.sms@gmail.com"
EMAIL_HOST_PASSWORD = 'JnghfdrfCvcVRJWXXX'


SESSION_EXPIRE_AT_BROWSER_CLOSE = True

    
