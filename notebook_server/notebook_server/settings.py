"""
Django settings for notebook_server project.

Generated by 'django-admin startproject' using Django 1.10.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '*k_1+2!r+)zb%_j$g5-qx2ymt()-hjk-58=6rypl9@_h&pbqvq'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['192.168.1.133']


# Application definition

INSTALLED_APPS = [
    'rest_framework',
    'rest_framework_social_oauth2',
    'oauth2_provider',
    'file_storage.apps.FileStorageConfig',
    'polls.apps.PollsConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'social_django',
    'notebook',
    'private_storage',
    'file_storage_oidc_auth',
]

PRIVATE_STORAGE_ROOT = '/media/'
PRIVATE_STORAGE_AUTH_FUNCTION = 'private_storage.permissions.allow_staff'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


#LOGIN_URL = '/login/'
#LOGIN_REDIRECT_URL = '/members/'
#LOGIN_ERROR_URL = '/login-error/'


#TEMPLATE_CONTEXT_PROCESSORS = (
#  "social_auth.context_processors.social_auth_by_type_backends"
#)


#SOCIAL_AUTH_DEFAULT_USERNAME = 'new_social_auth_user'
#SOCIAL_AUTH_UID_LENGTH = 16
#SOCIAL_AUTH_ASSOCIATION_HANDLE_LENGTH = 16
#SOCIAL_AUTH_NONCE_SERVER_URL_LENGTH = 16
#SOCIAL_AUTH_ASSOCIATION_SERVER_URL_LENGTH = 16
#SOCIAL_AUTH_ASSOCIATION_HANDLE_LENGTH = 16

#SOCIAL_AUTH_ENABLED_BACKENDS = ('google')

#GOOGLE_OAUTH2_CLIENT_ID = 'fdghdfghdfhgdfgh'
#GOOGLE_OAUTH2_CLIENT_SECRET = 'dfghdfghdfghfdghfdgh'

ROOT_URLCONF = 'notebook_server.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
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

WSGI_APPLICATION = 'notebook_server.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

AUTHENTICATION_BACKENDS = (
    'social_core.backends.open_id.OpenIdAuth',
    'social_core.backends.google.GoogleOpenId',
    'social_core.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend',
    'rest_framework_social_oauth2.backends.DjangoOAuth2'
)

#REST_FRAMEWORK = {
#    'DEFAULT_AUTHENTICATION_CLASSES': (
#        'oauth2_provider.ext.rest_framework.OAuth2Authentication',
#    ),
#}


FILE_STORAGE_OIDC_AUTH = {
    # Specify OpenID Connect endpoint. Configuration will be
    # automatically done based on the discovery document found
    # at <endpoint>/.well-known/openid-configuration
    'OIDC_ENDPOINT': 'https://accounts.google.com',

    # Accepted audiences the ID Tokens can be issued to
    'OIDC_AUDIENCES': ('390145535673-tlmf7h68q5mm4pkis097borj474qcirl.apps.googleusercontent.com','390145535673-de84dii1uprj03n02vmkg32m76sp2aap.apps.googleusercontent.com'),

    # (Optional) Function that resolves id_token into user.
    # This function receives a request and an id_token dict and expects to
    # return a User object. The default implementation tries to find the user
    # based on username (natural key) taken from the 'sub'-claim of the
    # id_token.
    'OIDC_RESOLVE_USER_FUNCTION': 'file_storage_oidc_auth.authentication.get_user_by_id',

    # (Optional) Number of seconds in the past valid tokens can be
    # issued (default 600)
    'OIDC_LEEWAY': 6000,

    # (Optional) Time before signing keys will be refreshed (default 24 hrs)
    'OIDC_JWKS_EXPIRATION_TIME': 24 * 60 * 60,

    # (Optional) Time before bearer token validity is verified again (default 10 minutes)
    'OIDC_BEARER_TOKEN_EXPIRATION_TIME': 10 * 60,

    # (Optional) Token prefix in JWT authorization header (default 'JWT')
    'JWT_AUTH_HEADER_PREFIX': 'JWT',

    # (Optional) Token prefix in Bearer authorization header (default 'Bearer')
    'BEARER_AUTH_HEADER_PREFIX': 'Bearer',
}

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
       'oauth2_provider.ext.rest_framework.OAuth2Authentication',
       'rest_framework_social_oauth2.authentication.SocialAuthentication',
        'file_storage_oidc_auth.authentication.JSONWebTokenAuthentication',
     #   'oidc_auth.authentication.BearerTokenAuthentication',
    ),
}

#SOCIAL_AUTH_STORAGE = 'social_django_mongoengine.models.DjangoStorage'
#SOCIAL_AUTH_STORAGE = 'django.db.backends.sqlite3'


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

#SOCIAL_AUTH_USER_MODEL = 'django.contrib.auth.models.User'
#SOCIAL_AUTH_SECRET_KEY = 'sdfsfsf'

#CSRF_COOKIE_SECURE = False


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
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'
