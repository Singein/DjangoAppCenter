"""
Django settings for DjangoAppCenter project.

Generated by 'django-admin startproject' using Django 3.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

from django.contrib import admin
from OSProfile import OSProfile

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


DEFAULT_OPTIONS = {
    'admin_site_title': 'DjangoAppCenter',
    'admin_site_header': 'DjangoAppCenter',
    'redirect': 'admin/',
    'apps': [],
    'middlewares': [],
    "routers": [],
    'databases': {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    },
    'rest_framework': {
        'DEFAULT_PERMISSION_CLASSES': [
            'rest_framework.permissions.IsAuthenticated',
        ],
        'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
        'PAGE_SIZE': 100,
        'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend']
    }
}


profile = OSProfile(appname="DjangoAppCenter",
                    profile="profile.json", options=DEFAULT_OPTIONS)
OPTIONS = profile.read_profile()

custom_settings = OPTIONS.get('custom_settings', None)  # 暂时没用到
apps = OPTIONS.get('apps', [])
middlewares = OPTIONS.get('middlewares', [])
databases = OPTIONS.get('databases', None)


site_title = OPTIONS.get('admin_site_title', 'DjangoAppCenter')
site_header = OPTIONS.get('admin_site_header', 'DjangoAppCenter')

admin.AdminSite.site_title = site_title
admin.AdminSite.site_header = site_header
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '8v9)1@nj4g+*i56y4c5bf8-ug#!$mj*(#p^o!yw%gr9$5+2+g^'

# SECURITY WARNING: don't run with debug turned on in production!
APP_CENTER_ENVIRON = os.environ.get("APP_CENTER_ENVIRON", "DEBUG")
DEBUG = APP_CENTER_ENVIRON == "DEBUG"

REST_FRAMEWORK = OPTIONS.get('rest_framework', {})

ALLOWED_HOSTS = ["*"]
# 跨域请求设置的基本参数
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True

# Application definition

INSTALLED_APPS = [
    'DjangoAppCenter.simpleui',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'django_filters'
] + apps

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
] + middlewares

ROOT_URLCONF = 'DjangoAppCenter.settings.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

DATABASE_ROUTERS = ['DjangoAppCenter.settings.dbrouters.Router']
WSGI_APPLICATION = 'DjangoAppCenter.settings.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = databases


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
