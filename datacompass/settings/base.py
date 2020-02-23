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
    'imagekit',
    'django_filters',
    # Custom apps
    'apps.users.apps.UsersConfig',
    'apps.organizations.apps.OrganizationsConfig',
    'apps.projects.apps.ProjectsConfig',
    'apps.surveys.apps.SurveysConfig',
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
        'PORT': env('DATABASE_PORT', default='5432')
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

# Crispy forms

CRISPY_TEMPLATE_PACK = 'bootstrap4'

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
