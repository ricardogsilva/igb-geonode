# -*- coding: utf-8 -*-
#########################################################################
#
# Copyright (C) 2017 OSGeo
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
#########################################################################

import os

import environ
from pathlib2 import Path

from geonode.settings import *

env = environ.Env(
    DEBUG=(bool, False)
)

# Defines the directory that contains the settings file as the LOCAL_ROOT
# It is used for relative settings elsewhere.
LOCAL_ROOT = str(Path(__file__).resolve().parent)

PROJECT_NAME = 'igb'

DEBUG = env("DEBUG")

TEMPLATE_DEBUG = DEBUG

DATABASES = {
    "default": env.db_url("DJANGO_DATABASE_URL"),
    "datastore": env.db_url("GEONODE_DB_URL"),
}

ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS")

SITEURL = env("DJANGO_SITEURL")

SITENAME = env("DJANGO_SITENAME", default='igb')

WSGI_APPLICATION = "{}.wsgi.application".format(PROJECT_NAME)

LANGUAGE_CODE = env("LANGUAGE_CODE", default="en")

if PROJECT_NAME not in INSTALLED_APPS:
    INSTALLED_APPS += (PROJECT_NAME,)

# Location of url mappings
# ROOT_URLCONF = os.getenv('ROOT_URLCONF', '{}.urls'.format(PROJECT_NAME))
ROOT_URLCONF = '{}.urls'.format(PROJECT_NAME)

# Additional directories which hold static files
STATICFILES_DIRS.append(
    os.path.join(LOCAL_ROOT, "static"),
)

# Location of locale files
LOCALE_PATHS = (
    os.path.join(LOCAL_ROOT, 'locale'),
    ) + LOCALE_PATHS

TEMPLATES[0]['DIRS'].insert(0, os.path.join(LOCAL_ROOT, "templates"))
loaders = (
    TEMPLATES[0]['OPTIONS'].get('loaders') or
    [
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader'
    ]
)
# loaders.insert(0, 'apptemplates.Loader')
TEMPLATES[0]['OPTIONS']['loaders'] = loaders
TEMPLATES[0].pop('APP_DIRS', None)

UNOCONV_ENABLE = env("UNOCONV_ENABLE", cast=bool, default=True)

if UNOCONV_ENABLE:
    UNOCONV_EXECUTABLE = env("UNOCONV_EXECUTABLE", default="/usr/bin/unoconv")
    UNOCONV_TIMEOUT = env("UNOCONV_TIMEOUT", cast=int, default=30)  # seconds

INSTALLED_APPS += (
   'allauth.socialaccount.providers.linkedin_oauth2',
   'allauth.socialaccount.providers.facebook',
)

if DEBUG:
    INSTALLED_APPS += (
        "sslserver",
    )

