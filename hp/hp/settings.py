# Django settings for hp project.

import os

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))


DEBUG = True
TEMPLATE_DEBUG = DEBUG
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

DB_NAME = 'hp'
DB_USER = 'hpadmin'
DB_PASSWORD = 'hpadmin'
DB_HOST = '192.168.3.7'
DB_PORT = '5432'

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': DB_NAME,        # Or path to database file if using sqlite3.
        'USER': DB_USER,                      # Not used with sqlite3.
        'PASSWORD': DB_PASSWORD,                  # Not used with sqlite3.
        'HOST': DB_HOST,                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': DB_PORT,                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

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
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media') # by Mohsin


XML_ROOT = os.path.join(PROJECT_ROOT, 'xml')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/' # by Mohsin


XML_URL = '/xml/' # by Mohsin

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
SECRET_KEY = '0@v_o46nh)$vws(z)*&_&kkf^9u@_brn!6^ru0k24r2400gv^t'

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
    #'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    #'middleware.middleware_user_authentication.UserAuthentication',
)

APPEND_SLASH=True

ROOT_URLCONF = 'hp.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    
    os.path.join(PROJECT_ROOT, 'templates'), # by Mohsin
    os.path.join(os.path.dirname(__file__), 'templates/html_snippets/forum_snippets').replace('\\','/'), #Fouzia#EDIT:Anil
    os.path.join(os.path.dirname(__file__), 'templates/html_snippets/news_snippets').replace('\\','/'), #Anil
    os.path.join(os.path.dirname(__file__), 'templates/user_templates').replace('\\','/'), #Anil
    os.path.join(os.path.dirname(__file__), 'templates/forum_templates').replace('\\','/'), #Anil
    os.path.join(os.path.dirname(__file__), 'templates/groupTemplates').replace('\\','/'), #Mohsin
    os.path.join(os.path.dirname(__file__), 'templates/admanagertemplates').replace('\\','/'), #Mohsin
    os.path.join(os.path.dirname(__file__), 'templates/phr_templates').replace('\\','/'), #Mohsin
    os.path.join(os.path.dirname(__file__), 'templates/news_templates').replace('\\','/'), #Anil
    os.path.join(os.path.dirname(__file__), 'templates/medicalcontent').replace('\\','/'), #Mohsin
    os.path.join(os.path.dirname(__file__), 'templates/dir_lis_templates').replace('\\','/'), #Anil    
)

INSTALLED_APPS = (
    #'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'hp',
    'hp.forum',
    'hp.news',
    'hp.groupmanager',
    'hp.admanager',
    'hp.user',
    'hp.patienthealthrecord',
    'hp.phr',
    #'directory_listing',
    #'ckeditor',
    # Uncomment the next line to enable the admin:
    # 'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
)

CKEDITOR_MEDIA_PREFIX = "/media/ckeditor/"

CKEDITOR_UPLOAD_PATH = os.path.join(MEDIA_ROOT, 'media/ckeditor/')

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Full',
        'height': 300,
        'width': 300,
    },
}

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

# by Mohsin
TEMPLATE_CONTEXT_PROCESSORS = (
    #'django.core.context_processors.debug',
    #'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
)

#Author:Added By Fouzia
#Description:For Email
TO_EMAIL = 'friazk@gmail.com'
FROM_EMAIL = 'store@nicl.com.pk'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'store@nicl.com.pk'
EMAIL_HOST_PASSWORD = 'store786'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
FORCE_SCRIPT_NAME=''

#DEFAULT_FROM_EMAIL = ''
#SERVER_EMAIL = ''
