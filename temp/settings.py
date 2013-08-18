# -*- coding: utf-8 -*-
# Django settings for lpdh_I project.

from unipath import Path
import os.path

PROJECT_DIR = Path(__file__).ancestor(2)

MEDIA_ROOT = PROJECT_DIR.child('media')
STATIC_ROOT = PROJECT_DIR.child('static')
STATICFILES_DIRS = (
    PROJECT_DIR.child('assets'),
)
TEMPLATE_DIRS = (
    PROJECT_DIR.child('templates'),
)

DEBUG = True
TEMPLATE_DEBUG = DEBUG

#BASE_PATH = os.path.dirname(__file__)
CURRENT_PATH = os.path.abspath(os.path.dirname(__file__).decode('utf-8'))
#print(BASE_PATH)
#print(CURRENT_PATH)
#PROJECT_DIR = Path(__file__).ancestor(2)

#MEDIA_ROOT = PROJECT_DIR.child('media')
#STATIC_ROOT = PROJECT_DIR.child('static')
#STATIC_ROOT = '/home/jose/devel/django-projects/Blogs/lpdh_I/static/'
#STATICFILES_DIRS = (
#    PROJECT_DIR.child('assets'),
#)
#TEMPLATE_DIRS = (
#    PROJECT_DIR.child('templates'),
#)

#print(PROJECT_DIR)
#print(MEDIA_ROOT)
#print(STATIC_ROOT)
#print(STATICFILES_DIRS)
#print(TEMPLATE_DIRS)

ADMINS = (
     (u'Jose Manuel Garcia Montes', 'jmgmontes@gmail.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'nacho_laprensadehoy',                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': 'nacho',
        'PASSWORD': 'g22XsZuQ',
        'HOST': '',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',                      # Set to empty string for default.
    }
}

# Settings para comprobar envio de boletines a traves de email
ARTICLES_FROM_EMAIL = {
    'protocol': 'IMAP4',
    'host': 'mail.wservices.ch',
    'port': 993,
    'keyfile': None,
    'certfile': None,
    'user': 'boletin@laprensadehoy.es',
    'password': '1961Michie',
    'ssl': True,
    #'autopost': True,
    'markup': 'h',
    'acknowledge': False,
    }

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

TIME_ZONE = 'Europe/Madrid'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'es-ES'

SITE_ID = 1

SESSION_COOKIE_DAYS = 90
SESSION_COOKIE_AGE = 60 * 60 * 24 * SESSION_COOKIE_DAYS

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
#MEDIA_ROOT = '/home/jose/devel/django-projects/Blogs/lpdh_I/media/'
MEDIA_URL = '/media/'

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
#STATIC_URL = '/static/'
#STATIC_ROOT = '/home/jose/devel/django-projects/Blogs/lpdh_I/static/'
STATIC_URL = '/static/'
#STATICFILES_DIRS = (
#    BASE_PATH+'/static',
#)


# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '!ryc0x^8l3-gcbr78gi4(5&vgs%@rn3zb)ny$^!(0osfe#g_z6'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'aldia.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'aldia.wsgi.application'

#TEMPLATE_DIRS = (
#    BASE_PATH+'/templates/',
#)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    #'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.flatpages',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'core',
    'unipath',
    #'south',
    'katche',
    'jarrett',
    'coltrane',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
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
SITE_DOMAIN = "http://laprensadehoy.es/"
IPAD_IS_MOBILE = False
LOGIN_URL = "/usuario/login/"
LOGOUT_URL = "/usuario/logout/"
LOGIN_REDIRECT_URL = '/usuario/profile/'
#LOGOUT_REDIRECT_URL = '/'
FORCE_SCRIPT_NAME = ''
