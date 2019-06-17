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
from urlparse import urljoin

from django_auth_ldap import config as ldap_config
import environ
import ldap
from pathlib2 import Path

from geonode.settings import *
from geonode_ldap.config import GeonodeNestedGroupOfNamesType

env = environ.Env(
    DEBUG=(bool, False)
)

# Defines the directory that contains the settings file as the LOCAL_ROOT
# It is used for relative settings elsewhere.
LOCAL_ROOT = str(Path(__file__).resolve().parent)

STATIC_ROOT = "{}/static_root".format(Path(LOCAL_ROOT).parent)
MEDIA_ROOT = "{}/uploaded".format(Path(LOCAL_ROOT).parent)

PROJECT_NAME = "igb"

DEBUG = env("DEBUG")

TEMPLATE_DEBUG = DEBUG

DATABASES = {
    "default": env.db_url("DJANGO_DATABASE_URL"),
    "datastore": env.db_url("GEONODE_DB_URL"),
}

GEOSERVER_LOCATION = env("GEOSERVER_LOCATION")
GEOSERVER_PUBLIC_LOCATION = env("GEOSERVER_LOCATION")

# FIXME: align local .env with the one on the test server
# these need to be revised
OGC_SERVER["default"].update({
    "LOCATION": GEOSERVER_LOCATION,
    "WEB_UI_LOCATION": GEOSERVER_LOCATION,
    "PUBLIC_LOCATION": GEOSERVER_PUBLIC_LOCATION,
    "DATASTORE": "datastore",
})

DEFAULT_MAP_CRS = "EPSG:3857"

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.filebased.FileBasedCache",
        "LOCATION": "/var/tmp/django_cache"
    }
}

ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS")

SITEURL = env("DJANGO_SITEURL")
# Changing the `SITEURL` variable has lots of side effects, so we need to
# adjust them too
LOGIN_URL = "{}account/login/".format(SITEURL)
LOGOUT_URL = "{}account/logout/".format(SITEURL)
ACCOUNT_LOGIN_REDIRECT_URL = SITEURL
ACCOUNT_LOGOUT_REDIRECT_URL = SITEURL
CATALOGUE["default"]["URL"] = urljoin(SITEURL, "catalogue/csw")
PYCSW["CONFIGURATION"]["metadata:main"]["provider_url"] = SITEURL
if USE_GEOSERVER:
    PUBLIC_GEOSERVER["source"]["attribution"] = "&copy; {}".format(SITEURL)
    LOCAL_GEOSERVER["source"]["attribution"] = "&copy; {}".format(SITEURL)

UPLOADER["BACKEND"] = "geonode.importer"

SITENAME = env("DJANGO_SITENAME", default="igb")

WSGI_APPLICATION = "{}.wsgi.application".format(PROJECT_NAME)

LANGUAGE_CODE = env("LANGUAGE_CODE", default="en")


if PROJECT_NAME not in INSTALLED_APPS:
    INSTALLED_APPS += (PROJECT_NAME,)

# Location of url mappings
# ROOT_URLCONF = os.getenv("ROOT_URLCONF", "{}.urls".format(PROJECT_NAME))
ROOT_URLCONF = "{}.urls".format(PROJECT_NAME)

# Additional directories which hold static files
STATICFILES_DIRS.append(
    os.path.join(LOCAL_ROOT, "static"),
)

# Location of locale files
LOCALE_PATHS = (
    os.path.join(LOCAL_ROOT, "locale"),
    ) + LOCALE_PATHS

TEMPLATES[0]["DIRS"].insert(0, os.path.join(LOCAL_ROOT, "templates"))
loaders = (
    TEMPLATES[0]["OPTIONS"].get("loaders") or
    [
        "django.template.loaders.filesystem.Loader",
        "django.template.loaders.app_directories.Loader"
    ]
)
# loaders.insert(0, "apptemplates.Loader")
TEMPLATES[0]["OPTIONS"]["loaders"] = loaders
TEMPLATES[0].pop("APP_DIRS", None)

UNOCONV_ENABLE = env("UNOCONV_ENABLE", cast=bool, default=True)

if UNOCONV_ENABLE:
    UNOCONV_EXECUTABLE = env("UNOCONV_EXECUTABLE", default="/usr/bin/unoconv")
    UNOCONV_TIMEOUT = env("UNOCONV_TIMEOUT", cast=int, default=30)  # seconds

INSTALLED_APPS += (
    "allauth.socialaccount.providers.linkedin_oauth2",
    "allauth.socialaccount.providers.facebook",
)

AUTHENTICATION_BACKENDS += (
    "geonode_ldap.backend.GeonodeLdapBackend",
)

LOGGING["loggers"].update({
    "igb": {
        "handlers": ["console"], "level": "DEBUG" if DEBUG else "ERROR"
    }
})

if DEBUG:
    INSTALLED_APPS += (
        "sslserver",
    )

AUTH_LDAP_SERVER_URI = env("LDAP_SERVER_URL")
AUTH_LDAP_BIND_DN = env("LDAP_BIND_DN")
AUTH_LDAP_BIND_PASSWORD = env("LDAP_BIND_PASSWORD")
AUTH_LDAP_USER_SEARCH = ldap_config.LDAPSearch(
    env("LDAP_USER_SEARCH_DN"),
    ldap.SCOPE_SUBTREE,
    env("LDAP_USER_SEARCH_FILTERSTR")
)
AUTH_LDAP_GROUP_SEARCH = ldap_config.LDAPSearch(
    env("LDAP_GROUP_SEARCH_DN"),
    ldap.SCOPE_SUBTREE,
)
AUTH_LDAP_GROUP_TYPE = GeonodeNestedGroupOfNamesType()
AUTH_LDAP_USER_ATTR_MAP = {
    "first_name": "cn",
    "last_name": "sn"
}
AUTH_LDAP_FIND_GROUP_PERMS = True
AUTH_LDAP_MIRROR_GROUPS_EXCEPT = [
    "test_group"
]

# these are not needed by django_auth_ldap - we use them to find and match
# GroupProfiles and GroupCategories
GEONODE_LDAP_GROUP_NAME_ATTRIBUTE = env(
    "LDAP_GROUP_NAME_ATTRIBUTE", default="cn")
GEONODE_LDAP_GROUP_PROFILE_FILTERSTR = env("LDAP_GROUP_PROFILE_FILTERSTR")
GEONODE_LDAP_GROUP_CATEGORY_FILTERSTR = env("LDAP_GROUP_CATEGORY_FILTERSTR")

CELERY_TASK_ALWAYS_EAGER = False  # use an async queue

# The below code is a workaround for not being able to run tests, apparently
# due to some migration conflict. If the IGRATION_MODULES environment variable
# is set to none, we set MIGRATION_MODULES to {<app>: None}
# and that skips checking migrations during DB creation
# Run tests with:
#
# MIGRATION_MODULES=NONE python manage.py test ...


class MigrationDisabler(object):

    def __contains__(self, item):
        return True

    def __getitem__(self, key):
        return None


MIGRATION_MODULES = (
    MigrationDisabler() if env("MIGRATION_MODULES", default="").lower() == "none" else
    env("MIGRATION_MODULES", default="") or {}
)

