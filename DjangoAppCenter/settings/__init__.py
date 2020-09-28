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

from DjangoAppCenter.settings.adminui import *
from DjangoAppCenter.settings.docker import DOCKER_FILE_TEMPLATE
from DjangoAppCenter.settings.email import *
from DjangoAppCenter.settings.log import LOGGING
from DjangoAppCenter.settings.options import BASE_DIR, DEFAULT_OPTIONS, OPTIONS, PROFILE_NAME

# custom_settings = OPTIONS.get('custom_settings', None)  # 暂时没用到


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '8v9)1@nj4g+*i56y4c5bf8-ug#!$mj*(#p^o!yw%gr9$5+2+g^'

# SECURITY WARNING: don't run with debug turned on in production!
APP_CENTER_ENVIRON = os.environ.get("APP_CENTER_ENVIRON", "DEBUG")
DEBUG = APP_CENTER_ENVIRON == "DEBUG"

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
    'guardian',
    'rest_framework',
    'django_filters',
    'DjangoAppCenter.packages',
    *OPTIONS.get('apps', [])
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    *OPTIONS.get('middlewares', [])
]
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',  # default
    'guardian.backends.ObjectPermissionBackend',
)
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

DATABASES = OPTIONS.get('databases', None)

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

STATIC_URL = OPTIONS.get('static_url') if OPTIONS.get('static_url') else '/static/'
STATIC_ROOT = OPTIONS.get('static_root') if OPTIONS.get('static_root') else os.path.join(os.getcwd(), 'statics')

MEDIA_URL = OPTIONS.get('media_url') if OPTIONS.get('media_url') else '/media/'
MEDIA_ROOT = OPTIONS.get('media_root') if OPTIONS.get('media_root') else os.path.join(os.getcwd(), 'uploads')

REST_FRAMEWORK = OPTIONS.get('rest_framework', {})

admin.AdminSite.site_title = OPTIONS.get('admin_site_title', 'DjangoAppCenter')
admin.AdminSite.site_header = OPTIONS.get(
    'admin_site_header', 'DjangoAppCenter')
