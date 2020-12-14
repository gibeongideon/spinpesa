"""
Django settings for spinpesa project.

Generated by 'django-admin startproject' using Django 3.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
from decouple import config

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_DIR = os.path.dirname(BASE_DIR)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))



# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'i#r2p5_12xnuojmk)@$$ix78r^b=f__@vf*tw4nv665-yo14)j'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'users',
    'rest_framework',
    'rest_framework.authtoken',
    'channels',# resolve  apps which need run server commands# move to top
    'core',
    'account',
    'gwheel',
    # 'django_celery_results',
    # 'django_celery_beat'#no
    'spinchannel',
    'chat',
    'mpesa_api',
    'cash_trans',
    'app',
    'authentication',
      
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


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
    # 'DEFAULT_PERMISSION_CLASSES': [
    #    'rest_framework.permissions.IsAuthenticated',
    # ],
}

ROOT_URLCONF = 'spinpesa.urls'

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

WSGI_APPLICATION = 'spinpesa.wsgi.application'
ASGI_APPLICATION = 'spinpesa.asgi.application' 


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': config('DB_NAME'),
#         'USER': config('DB_USER'),
#         'PASSWORD': config('DB_PASSWORD'),
#         'HOST': config('DB_HOST'),
#         'PORT': config('DB_PORT'),  # Set to empty string for default.
#     }
# }

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'
# Celery
# CELERY_BROKER_URL = 'amqp://guest:guest@rabbitmq:5672//'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
        'logfile': {
            'level':'DEBUG',
            'class':'logging.FileHandler',
            'filename': BASE_DIR + "/../logfile",
        },
    },
    'root': {
        'level': 'INFO',
        'handlers': ['console', 'logfile']
    },
}



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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Nairobi'

USE_I18N = True

USE_L10N = True

USE_TZ = True



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
# STATIC_ROOT = os.path.abspath(os.path.join(PROJECT_DIR, 'static'))
# MEDIA_URL = '/media/'
# MEDIA_ROOT = os.path.abspath(os.path.join(PROJECT_DIR, 'media'))
# MEDIA_UPLOAD_FOLDER = '%Y_%m_%d/'
# TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")  # ROOT dir for templates


JET_SIDE_MENU_COMPACT = True

# CELERY_RESULT_BACKEND='django_db'
# BROKER_URL = 'amqp://guest:guest@localhost:5672/'
CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
# CELERY_TIMEZONE = 'Africa/Nairobi'
# CELERY_RESULT_BACKEND = 'django-db'


from celery.schedules import crontab

CELERY_BEAT_SCHEDULE = {

    'create_spin_wheel_market': { 
         'task': 'gwheel.tasks.create_spinwheel', 
         'schedule': crontab(minute= [0,5,10,15,20,25,30,35,40,45,50,55]),
        },          
}


CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [('localhost', 6379)],
        },
    }
}





# Safaricom Configs

# B2C (Bulk Payment) Configs
# see https://developer.safaricom.co.ke/test_credentials
# https://developer.safaricom.co.ke/b2c/apis/post/paymentrequest

#Consumer Key
MPESA_B2C_ACCESS_KEY = config('MPESA_B2C_ACCESS_KEY', default='')
#Consumer Secret
MPESA_B2C_CONSUMER_SECRET = config('MPESA_B2C_CONSUMER_SECRET', default='')
# This is the encryption of the scurity Credentials I used the Developer site to encrypt it.
B2C_SECURITY_TOKEN =  config('B2C_SECURITY_TOKEN', default='')
#InitiatorName
B2C_INITIATOR_NAME = config('B2C_INITIATOR_NAME', default='')
# CommandID
B2C_COMMAND_ID = config('B2C_COMMAND_ID', default='')
#PartyA
B2C_SHORTCODE = config('B2C_SHORTCODE', default='')
# this is the url where Mpesa  will post in case of a time out. Replace http://mpesa.ngrok.io/  with your url ow here this app is running
B2C_QUEUE_TIMEOUT_URL = config('B2C_QUEUE_TIMEOUT_URL', default='')
# this is the url where Mpesa will post the result. Replace http://mpesa.ngrok.io/  with your url ow here this app is running
B2C_RESULT_URL = config('B2C_RESULT_URL', default='')
# this is the url where we post the B2C request to Mpesa. Replace this with the url you get from safaricom after you have passed the UATS
MPESA_URL = config('MPESA_URL', default='')

# C2B (Paybill) Configs
# See https://developer.safaricom.co.ke/c2b/apis/post/registerurl

#Consumer Secret
MPESA_C2B_ACCESS_KEY = config('MPESA_C2B_ACCESS_KEY', default='')
# Consumer Key
MPESA_C2B_CONSUMER_SECRET = config('MPESA_C2B_CONSUMER_SECRET', default='')
# Url for registering your paybill replace it the url you get from safaricom after you have passed the UATS
C2B_REGISTER_URL = config('C2B_REGISTER_URL', default='')
#ValidationURL
# replace http://mpesa.ngrok.io/ with your url ow here this app is running
C2B_VALIDATE_URL = config('C2B_VALIDATE_URL', default='')
#ConfirmationURL
# replace http://mpesa.ngrok.io/ with your url ow here this app is running
C2B_CONFIRMATION_URL = config('C2B_CONFIRMATION_URL', default='')
#ShortCode (Paybill)
C2B_SHORT_CODE = config('C2B_SHORT_CODE', default='')
#ResponseType
C2B_RESPONSE_TYPE = config('C2B_RESPONSE_TYPE', default='')

# C2B (STK PUSH) Configs
# https://developer.safaricom.co.ke/lipa-na-m-pesa-online/apis/post/stkpush/v1/processrequest

#replace http://mpesa.ngrok.io/ with your url ow here this app is running
C2B_ONLINE_CHECKOUT_CALLBACK_URL = config('C2B_ONLINE_CHECKOUT_CALLBACK_URL', default='')
# The Pass Key provided by Safaricom when you pass UAT's
# See https://developer.safaricom.co.ke/test_credentials
C2B_ONLINE_PASSKEY = config('C2B_ONLINE_PASSKEY', default='')
# Your Short code
C2B_ONLINE_SHORT_CODE = config('C2B_ONLINE_SHORT_CODE', default='')
# your paybill or till number
C2B_ONLINE_PARTY_B = config('C2B_ONLINE_PARTY_B', default='')
# number of seconds from the expiry we consider the token expired the token expires after an hour
# so if the token is 600 sec (10 minutes) to expiry we consider the token expired.
# TOKEN_THRESHOLD = config('TOKEN_THRESHOLD', default=600, cast=int) ## invalid literal for int() with base 10: "config('TOKEN_THRESHOLD')"
