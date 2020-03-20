"""
Django settings for datacompass project.

Generated by 'django-admin startproject' using Django 3.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/

For more information django-environ which is used to read environment variables settings, see
https://django-environ.readthedocs.io/en/latest/
"""
from email.utils import getaddresses
from pathlib import Path

import environ

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = Path(__file__).parents[2]

env = environ.Env()

env.read_env(str(BASE_DIR / '.env'))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('DJANGO_SECRET_KEY', default='!$!c7jx@rx%u$fp+79)$$fjfhzjv5bot(o(s0ap&vbkslhoz_f')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DJANGO_DEBUG", False)

ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=[])

INTERNAL_IPS = env.list('INTERNAL_IPS', default=['127.0.0.1'])

# Application definition

INSTALLED_APPS = [
    # Django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    # Third party apps
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'django_countries',
    'phonenumber_field',
    'mptt',
    'crispy_forms',
    'widget_tweaks',
    'imagekit',
    'django_filters',
    'active_link',
    'django_select2',
    'froala_editor',
    'bootstrap_pagination',
    # Custom apps
    'core',
    'apps.users.apps.UsersConfig',
    'apps.organizations.apps.OrganizationsConfig',
    'apps.projects.apps.ProjectsConfig',
    'apps.surveys.apps.SurveysConfig',
    'apps.respondents.apps.RespondentsConfig',
    'apps.responses.apps.ResponsesConfig',
    # Debug toolbar
    'debug_toolbar',
]

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'datacompass.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            str(BASE_DIR / 'templates')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
                'datacompass.context_processors.site',
            ],
        },
    },
]

WSGI_APPLICATION = 'datacompass.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': env('DATABASE_ENGINE', default='django.db.backends.postgresql'),
        'NAME': env('DATABASE_NAME', default='datacompass'),
        'USER': env('DATABASE_USER', default='datacompass'),
        'PASSWORD': env('DATABASE_PASSWORD', default='datacompass'),
        'HOST': env('DATABASE_HOST', default='127.0.0.1'),
        'PORT': env('DATABASE_PORT', default='5432'),
        'CONN_MAX_AGE': env.int('DATABASE_CONN_MAX_AGE', default=0),
        'ATOMIC_REQUESTS': env.bool('DATABASE_ATOMIC_REQUESTS', default=True)
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_USER_MODEL = 'users.User'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
)

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
]

ACCOUNT_AUTHENTICATION_METHOD = env('ACCOUNT_AUTHENTICATION_METHOD', default='email')

ACCOUNT_EMAIL_REQUIRED = env.bool('ACCOUNT_EMAIL_REQUIRED', default=True)

ACCOUNT_USERNAME_REQUIRED = env.bool('ACCOUNT_USERNAME_REQUIRED', default=False)

ACCOUNT_EMAIL_VERIFICATION = env('ACCOUNT_EMAIL_VERIFICATION', default='none')

LOGIN_REDIRECT_URL = env('LOGIN_REDIRECT_URL', default='users:profile-detail')

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = env('LANGUAGE_CODE', default='en-us')

TIME_ZONE = env('TIME_ZONE', default='UTC')

USE_I18N = True

USE_L10N = True

USE_TZ = True

LANGUAGES = [
    ('en', 'English'),
    ('sw', 'Swahili'),
]

DEFAULT_LANGUAGES = ['en']


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATICFILES_DIRS = env.list('STATICFILES_DIRS', default=[
    str(BASE_DIR / 'static'),
    str(BASE_DIR / 'assets/bundles')]
)

STATIC_URL = env('STATIC_URL', default='/static/')

STATIC_ROOT = env('STATIC_ROOT', default=str(BASE_DIR / 'static_root'))

MEDIA_URL = env('MEDIA_URL', default='/media/')

MEDIA_ROOT = env('MEDIA_ROOT', default=str(BASE_DIR / 'media_root'))

DEFAULT_FILE_STORAGE = env('DEFAULT_FILE_STORAGE', default='django.core.files.storage.FileSystemStorage')

STATICFILES_STORAGE = env('STATICFILES_STORAGE',
                          default='django.contrib.staticfiles.storage.StaticFilesStorage')

# Crispy forms

CRISPY_TEMPLATE_PACK = 'bootstrap4'

# Active link
ACTIVE_LINK_CSS_CLASS = 'active'

ACTIVE_LINK_STRICT = True

# Select2
SELECT2_JS = ''

SELECT2_CSS = ''


# Site

SITE_ID = env.int('SITE_ID', default=1)

SITE_NAME = env('SITE_NAME', default='Data Compass')


# Admin site

ADMIN_SITE_NAME = env('ADMIN_SITE_HEADER', default=SITE_NAME)

ADMIN_SITE_HEADER = env('ADMIN_SITE_HEADER', default=SITE_NAME)

ADMIN_INDEX_TITLE = env('ADMIN_INDEX_TITLE', default='Administration')


# Email

EMAIL_USE_TLS = env.bool('EMAIL_USE_TLS', default=True)

EMAIL_BACKEND = env('EMAIL_BACKEND', default='django.core.mail.backends.smtp.EmailBackend')

EMAIL_HOST = env('EMAIL_HOST', default='localhost')

EMAIL_PORT = env.int('EMAIL_PORT', default=25)

EMAIL_HOST_USER = env('EMAIL_HOST_USER', default='')

EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD', default='')

DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL', default='')

SERVER_EMAIL = env('SERVER_EMAIL', default='')

ADMINS = getaddresses([env('ADMINS', default='')])


# Session

SESSION_COOKIE_AGE = env.int('SESSION_COOKIE_AGE', default=1209600)

SESSION_EXPIRE_AT_BROWSER_CLOSE = env.bool('SESSION_EXPIRE_AT_BROWSER_CLOSE', default=False)

SESSION_COOKIE_SECURE = env.bool('SESSION_COOKIE_SECURE', default=False)


# SSL

if env('SECURE_PROXY_SSL_HEADER', default=None):
    SECURE_PROXY_SSL_HEADER = env('SECURE_PROXY_SSL_HEADER').split()[:2]

SECURE_SSL_REDIRECT = env.bool('SECURE_SSL_REDIRECT', default=False)

CSRF_COOKIE_SECURE = env.bool('CSRF_COOKIE_SECURE', default=False)

SECURE_REFERRER_POLICY = env('SECURE_REFERRER_POLICY', default='origin-when-cross-origin')

SECURE_HSTS_SECONDS = env.int('SECURE_HSTS_SECONDS', default=0)

SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool('SECURE_HSTS_INCLUDE_SUBDOMAINS', default=False)

SECURE_HSTS_PRELOAD = env.bool('SECURE_HSTS_PRELOAD', default=False)


# Logging

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'formatters': {
        'django.server': {
            '()': 'django.utils.log.ServerFormatter',
            'format': '[%(server_time)s] %(message)s',
        }
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
        },
        'console_debug_false': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'logging.StreamHandler',
        },
        'django.server': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'django.server',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'console_debug_false', 'mail_admins'],
            'level': 'INFO',
        },
        'django.server': {
            'handlers': ['django.server'],
            'level': 'INFO',
            'propagate': False,
        }
    }
}

# Surveys

SURVEYS_DEFAULT_DATASET_FREQUENCIES = env.list('SURVEYS_DEFAULT_DATASET_FREQUENCIES', default=[
    'Every day',
    'A few days a week',
    'A few times a month',
    'A few times a year',
])

SURVEYS_DEFAULT_DATASET_ACCESS = env.list('SURVEYS_DEFAULT_DATASET_ACCESS', default=[
    'Only I or a few people can access',
    'All staff can access',
    'Everybody can access',
])

# Azure

AZURE_ACCOUNT_NAME = env('AZURE_ACCOUNT_NAME', default=None)

AZURE_ACCOUNT_KEY = env('AZURE_ACCOUNT_KEY', default=None)

AZURE_CONTAINER = env('AZURE_CONTAINER', default=None)

AZURE_STATIC_CONTAINER = env('AZURE_STATIC_CONTAINER', default=None)

AZURE_MEDIA_CONTAINER = env('AZURE_MEDIA_CONTAINER', default=None)

AZURE_URL_EXPIRATION_SECS = env('AZURE_URL_EXPIRATION_SECS', default=None)

AZURE_LOCATION = env('AZURE_LOCATION', default='')

AZURE_STATIC_LOCATION = env('AZURE_STATIC_LOCATION', default='static')

AZURE_MEDIA_LOCATION = env('AZURE_MEDIA_LOCATION', default='media')

AZURE_CUSTOM_DOMAIN = env('AZURE_CUSTOM_DOMAIN', default=None)

# Google Analytics

GOOGLE_ANALYTICS_TRACKING_ID = env('GOOGLE_ANALYTICS_TRACKING_ID', default='')
