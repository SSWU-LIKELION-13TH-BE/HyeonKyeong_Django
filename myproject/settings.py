"""
Django settings for myproject project.

Generated by 'django-admin startproject' using Django 5.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-l2bepe+=y@0!ucap$&(h^ie*#u3y@7!t(ixk%p&0*d0)y4k8hs'

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
    'bootstrap4',
    "user",
    'django.contrib.sites',

    #allauth 추가
    'allauth',
    'allauth.account', 
    'allauth.socialaccount', 
 
    #provider 추가 
    'allauth.socialaccount.providers.kakao', # 카카오로그인 추가
    'allauth.socialaccount.providers.naver', # 네이버 로그인 추가
]

SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

SOCIALACCOUNT_LOGIN_ON_GET = True
LOGIN_REDIRECT_URL = 'user:home'
ACCOUNT_LOGOUT_REDIRECT_URL = 'user:home'
ACCOUNT_LOGOUT_ON_GET = True

ROOT_URLCONF = 'myproject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'myproject.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'ko-kr'
TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'user.CustomUser'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

from myproject import conf
# Email 전송
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = conf.EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = conf.EMAIL_HOST_PASSWORD


DEFAULT_FROM_EMAIL = EMAIL_HOST_USER


MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

LOGIN_URL = '/user/login/'
ACCOUNT_AUTHENTICATED_REDIRECT_URL = '/user/home/' 


SOCIALACCOUNT_PROVIDERS ={
"kakao": {
    "APP": {
    "client_id": conf.KAKAO_CLIENT_ID,
    "secret": conf.KAKAO_CLIENT_SECRET,
    "key": ""
    },
    "SCOPE": [
        "profile_nickname"
    ],

    'AUTH_PARAMS': {'auth_type': 'login'},
    "access_type": "online",
    'prompt': 'select_account', #간편로그인을 지원해줌
    },


#네이버 설정
"naver": {
"APP": {
"client_id": conf.NAVER_CLIENT_ID,
"secret": conf.NAVER_CLIENT_SECRET,
"key": ""
},

"SCOPE": [
    "name",
    "Email"
],
"AUTH_PARAMS": {
    "access_type": "online",
    'prompt': 'select_account',#간편로그인을 지원해줌
}}}