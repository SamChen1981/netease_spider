# -*- coding: utf-8 -*-
"""
Django settings for netease_spider project.

Generated by 'django-admin startproject' using Django 1.11.4.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""
from __future__ import absolute_import

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


SECRET_KEY = ')6*zp_#_l7ao@zi%t&-qj9$jhr8@@i4seg*f0)6@z4^7y(r6qj'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'goods',
    'netease',
    'spider',
    'djcelery'
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'netease_spider.urls'

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

WSGI_APPLICATION = 'netease_spider.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'unix_socket': '/var/run/mysqld/mysqld.sock',
        'CHARSET': 'UTF8',
        'TEST_CHARSET': 'UTF8',
    },
    "slave": {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'unix_socket': '/var/run/mysqld/mysqld.sock',
        'CHARSET': 'UTF8',
        'TEST_CHARSET': 'UTF8',
    }
}

# 配置读写分离
DATABASE_ROUTERS = ['netease_spider.db_router.PrimaryReplicaRouter']

REDIS = {
    'default': {
        'db': 3,
        'unix_socket_path': '/tmp/redis.sock',
    },
}

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'unix:/tmp/redis.sock:1',
        # 'KEY_PREFIX': '_',
        'VERSION': 2,
        'OPTIONS': {
            # 'PARSER_CLASS': 'redis.connection.HiredisParser',
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
    },
    'local': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'local',
        'TIMEOUT': 3600 * 24 * 8,
        'MAX_ENTRIES': 1000,
    },
    'staticfiles': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'staticfiles',
        'TIMEOUT': 3600 * 24 * 8,
        'MAX_ENTRIES': 1000,
    },
}

TIME_ZONE = 'Asia/Shanghai'

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


MEDIA_URL = '/media/'
MEDIA_ROOT = '/data/netease/'


STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'


try:
    from netease_spider.local_settings import *
except ImportError:
    pass

if DEBUG:
    MSG_PREFIX = u'测试:'
else:
    MSG_PREFIX = ''

from datetime import timedelta
from celery.schedules import crontab

CELERYBEAT_SCHEDULE = {
    # 定时同步数据
    'sync_category': {
        'task': 'goods.tasks.sync_category',
        'schedule': crontab(hour=0, minute=34),
    },
    'sync_goods': {
        'task': 'goods.tasks.sync_goods',
        'schedule': crontab(hour=1, minute=32),
    },
    # 每隔5小时从代理网站中爬取代理
    'sync_proxy': {
        'task': 'spider.tasks.sync_proxy',
        'schedule': timedelta(hours=5),
    },
    # 每隔一小时 检查代理库中的代理状态
    'check_proxy': {
        'task': 'spider.tasks.sync_check_proxy',
        'schedule': timedelta(hours=1),
      },
}

CELERYBEAT_SCHEDULE_FILENAME = "./var/celerybeat-schedule.log"