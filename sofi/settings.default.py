"""
Nombre del software: Sofi

Descripción: Sistema de gestión de eventos

Nombre del licenciante y año: Fundación CENDITEL (2018)

Autores: William Páez

La Fundación Centro Nacional de Desarrollo e Investigación en Tecnologías
Libres (CENDITEL), ente adscrito al Ministerio del Poder Popular para Educación
Universitaria, Ciencia y Tecnología (MPPEUCT), concede permiso para usar,
copiar, modificar y distribuir libremente y sin fines comerciales el
"Software - Registro de bienes de CENDITEL", sin garantía alguna, preservando
el reconocimiento moral de los autores y manteniendo los mismos principios para
las obras derivadas, de conformidad con los términos y condiciones de la
licencia de software de la Fundación CENDITEL.

El software es una creación intelectual necesaria para el desarrollo económico
y social de la nación, por tanto, esta licencia tiene la pretensión de
preservar la libertad de este conocimiento para que contribuya a la
consolidación de la soberanía nacional.

Cada vez que copie y distribuya el "Software - Registro de bienes de CENDITEL"
debe acompañarlo de una copia de la licencia. Para más información sobre los
términos y condiciones de la licencia visite la siguiente dirección
electrónica:
http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/
"""

"""
Django settings for sofi project.

Generated by 'django-admin startproject' using Django 2.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '(vb%72-*^2k)%7b&5li+968jxtf5@c$thm+)or56jg%atovfnx'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Identifica a los administradores del sistema
ADMINS = [
    ('William Páez', 'wpaez@cenditel.gob.ve'),
]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'captcha',
    'base',
    'user.apps.UserConfig',
    'event.apps.EventConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'sofi.urls'

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

WSGI_APPLICATION = 'sofi.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    # 'default': {
    #   'ENGINE': 'django.db.backends.sqlite3',
    #   'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    # }

    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'sofi',
        'USER': 'admin',
        'PASSWORD': '123',
        'HOST': 'localhost',
        'PORT': '5432',
        'ATOMIC_REQUESTS': True,
    }

    # 'default': {
    #    'ENGINE': 'django.db.backends.mysql',
    #    'NAME': 'sofi',
    #    'USER':'admin',
    #    'PASSWORD':'123',
    #    'HOST':'localhost',
    #    'PORT':'3306',
    #    'OPTIONS': {
    #        'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
    #    }
    # }
}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'es-ve'

TIME_ZONE = 'America/Caracas'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static/'),
    os.path.join(BASE_DIR, 'media/'),
)

LOGIN_URL = 'user:login'

LOGIN_REDIRECT_URL = 'base:home'

LOGOUT_REDIRECT_URL = 'user:login'

if DEBUG:
    # Configuración para entornos de desarrollo
    EMAIL_HOST_USER = 'email@email.com'
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    # Configuración para entornos de producción
    EMAIL_USE_TLS = True
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_PORT = 587
    EMAIL_HOST_USER = 'email@email.com'
    EMAIL_HOST_PASSWORD = 'password'
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# Configuración del CAPTCHA
# Ruta en donde se encuentra el diccionario de palabras a utilizar en la
# generación del captcha
CAPTCHA_WORDS_DICTIONARY = os.path.join(
    BASE_DIR, 'static/dictionaries/captcha-es.txt'
)

# Establece el tipo de captcha a generar. Se establece a la extraccion de
# palabras a partir de un diccionario
CAPTCHA_CHALLENGE_FUNCT = 'captcha.helpers.word_challenge'

# Longitud de carácteres a mostrar en la imagen del captcha
CAPTCHA_LENGTH = 6

# Longitud de carácteres máxima permitida para extraer del diccionario
CAPTCHA_DICTIONARY_MAX_LENGTH = 6

# Longitud de carácteres mínima permitida para extraer del diccionario
CAPTCHA_DICTIONARY_MIN_LENGTH = 4

# Color de fondo para la imagen del captcha
CAPTCHA_BACKGROUND_COLOR = '#DC4A22'

# Color de la fuente para la imagen del captcha
CAPTCHA_FOREGROUND_COLOR = '#FFF'

if DEBUG:
    # Elimina la imagen de ruido en el fondo del captcha cuando la aplicacion
    # se encuentra en modo desarrollo
    CAPTCHA_NOISE_FUNCTIONS = ('captcha.helpers.noise_null',)

    # Tiempo de expiración del captcha en entornos de desarrollo, representado
    # en minutos
    CAPTCHA_TIMEOUT = 1440  # 24 horas
