from pathlib import Path
import os
import django_heroku

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '99kbj66#8drc=o=m%0*m^2%^*l7c29bkvqfa6po8k8_$vogqka'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['contactguys.herokuapp.com', '127.0.0.1']


# Application definition

INSTALLED_APPS = [
    'contact',
    'api',
    'rest_framework',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'gdstorage',
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

ROOT_URLCONF = 'vk.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
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

WSGI_APPLICATION = 'vk.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.postgresql',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_ROOT = os.path.join(BASE_DIR, "media/")
MEDIA_URL = '/media/'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}

json_google = {
  "type": "service_account",
  "project_id": "solid-heaven-312719",
  "private_key_id": "7cdbd890488a23f11d42e8db58b076592cec24fc",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQC48mIlqlSZQMDn\np/OTcJqkqB/ypRR4iPP1VjO/ZqvE5Gu10aLjnu+MW60MV2OHPiYyAbSeVC43a2AQ\nAgqsfJJDYaqjX30Gx0luiF7SCvxetUnI94W1nwjK1PRLZWtscW4dXa66sfgEv0Wj\n5QabXXqATH0en444yi8hX67/5KR0AQ8NpSgDzynuIUvwkzmlC4YdZJpljmPgMxDl\nm05WQ78T0vJuVljHelSxRJmsJJCgK26o5a657H6lawIaKZx0Mo17yakzMWoJu948\nWCZWv+ReSZGbfnQqnowiCTDxM6xybSxOgbXd/YeH1UWZCCH6WZijplNnl7Cvmzy3\nsLFl25EzAgMBAAECggEAUd5FkPvBwCc4XTNs8KbHZbzgi4YEtkiViVQTyxW1Uo50\nmYMHcnAQBRct1ok2jw71VGyJ2g5UeQbIer2UoP7xte8dXH1v+FiuSkYGhz8CsR/Z\n3iKnpxqTh0nWLCvkbhgWENy/9HfEXMGYn7DJiGvMRs/VEQG7MKtbSpAzBKZfH9P4\nYV2jg/nIphkb+Wb/SNYIdXq+KO3+pOgaqRuRXm1gZ3XYc5t5Y46Gs6WCz8FHoW7w\nrUsSxJlwpgaZRvuFkB5zlu9n/Gf1yZlmtnCL8NEnwffoDppjHAYkrfY8QaUGghpD\nvkHmcO1xkr7j6k8z1c8F6D9D7X+l+o36XHmVgSUO6QKBgQDyi+8YWbUtScComXBW\n4nPoX79YRrwddoD2NDXX0iIUEbhNH9D9KGO8vBWw2nZCD40CK6GtpjM6nateFwLM\naxgIFEXBE7JjWNe8opifjYnrPt8tGdUEhxrAXnBvy4TOc7TKDrSE4rtEUya974IY\nfu9yRuCY4V7C+v7/t3GN8YanaQKBgQDDNI4Q0KXx7iounZqMGyfLmL164buxWiUb\niKgR1ZQXSPGwJv4jKsiVbHKKOmLJ7HHgldpD8T2UtSMKVJW5287Ql/TwZcYs7TID\nODf8I2rVwgRMcBjvT5DwJocXLWAd8Jgq09M0ElBGkPMtiFM/OhkGe11x4AuRI+iH\nwdhufHecOwKBgQCkXlqI2PpkF5AdceZkqxA7kO9+JmmDWfSpZNZ8TOZVTXDlq0MY\n3M9CbwAQGux7dkhsCR+HK5OaDJG+sL9vwr/Fcd+Xqf6BPwrsxg/CSMwHhVL/IHtw\nlxJ0/UsbKAP3WQhSykZhq7mW4vblTrOOYC9q9Udts4Vhg3Fd4HZu6BgFyQKBgAaY\n9SA+XQ1zNjvDGeEYXdz0uZq4nGZfHJf0o3GO3WV4EqsYdkhr/sGGG8zuMj6O3j5v\n8iOPuLwY7yk/OJxCgJfuOtoRJoSIM8OGF+ZOsCKvXwPSWhVkhAqJ0tEGuJPqeMoh\nxKai49GuvnlQfTfK1+OvMbZSkzGBnC9SbuU1EbnXAoGBANFKJd9S60zKVGYJT6DT\ntFNju4QQXFanrHYdfIrsixaw2kqW5x6HMrMo9xC72nx0gAfmqFNbDlAXUbpQNtYw\n3ndGIN6EJ9qP0sXbfwIQzJgQ5UdIHBX4EtG6xXCXq6snNFxQPPofzElE40pplT3A\n1USK5MuP2lK8TkLq6qJCKWtk\n-----END PRIVATE KEY-----\n",
  "client_email": "contact-service@solid-heaven-312719.iam.gserviceaccount.com",
  "client_id": "100730099495830905588",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/contact-service%40solid-heaven-312719.iam.gserviceaccount.com"
}

# Google Drive Storage Settings
GOOGLE_DRIVE_STORAGE_JSON_KEY_FILE = 'googledrive.json'

# heroku
django_heroku.settings(locals())
