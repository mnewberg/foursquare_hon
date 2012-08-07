

# Django settings for twilio project.

DEBUG = False
TEMPLATE_DEBUG = True

ADMINS = ()

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME':'four_staging',                      # Or path to database file if using sqlite3.
        'USER': 'root',                      # Not used with sqlite3.
        'PASSWORD': 'swagoo',                  # Not used with sqlite3.
        'HOST': '108.171.160.105',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

SESSION_EXPIRE_AT_BROWSER_CLOSE=True

SESSION_ENGINE='django.contrib.sessions.backends.db'

SESSION_SAVE_EVERY_REQUEST=True

CLIENT_ID='4KS2JZ3U4GYSHOL1NQ3DCEH5ZXC3R5PVEVAAQAQCA5Z5RRRS'

CLIENT_SECRET='TOXCCMYSGVPM2OAVPR3RIDUM0WFMKVJ4VUFNFSI00QSZF4IH'

CALLBACK_URL='http://playdo.pe/loc/'

SENTRY_DSN='http://9b5bc04b51714ec09d37667b71b4dfa6:5281b6ccb4134b4ab98a992378f41d51@50.57.186.209:9000/2'

#TWILIO
ACCOUNT_SID = "AC5b9299999c233e8af8296346a93e74a1"

AUTH_TOKEN = "b6052ac1980c3986c7497bb8fcc9746e"

#KLOUT
KLOUT = 'cpej5es6neebsajjwqkv2yf2'

#SENDGRID
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = 'thenewb'
EMAIL_HOST_PASSWORD = '471send'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

#TWITTER
CONSUMER_KEY='JmkU5KyHIU8WIeyQK46lw'
CONSUMER_SECRET='O9plHA3btKtOIEcUPzimp5NIsWaekEyzB7FgkioSs8'
ACCESS_TOKEN='487096854-0V2XIflNO5mu6CZYVXVPIk59wXdURQa5XRRck4sC'
ACCESS_TOKEN_SECRET='E6vetPVM95pXMY94ZXnuoNRc3qLvVi3filmdTst273Y'


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
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = '/var/www/four_staging/foursquare/'

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = '/static/'

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
SECRET_KEY = '-b##*$&%1$44+r7f(q!55i36kbsyj8&j_@dc2!upleouprh*!$'

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
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
	"/var/www/four_staging/foursquare/templates"
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)


TEMPLATE_CONTEXT_PROCESSORS = (
   'django.core.context_processors.auth',
   'django.core.context_processors.debug',
   'django.core.context_processors.i18n',
   'django.core.context_processors.media',
   'django.core.context_processors.request',
   'mobileadmin.context_processors.user_agent',
)


INSTALLED_APPS = (
    #'mobileadmin',
    'raven.contrib.django',
    'sentry',
    'django_cron',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'gallery',
    'sms',
    # Uncomment the next line to enable the admin:
     'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
)


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "sentry": {
            "class": "sentry.client.handlers.SentryHandler",
            "level": "ERROR",
        }
    },
    "loggers": {
        "django.request": {
            "handlers": ["sentry"],
            "level": "ERROR",
            "propagate": True
        }
    },
}







