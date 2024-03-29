"""
Django settings for DBproject project.

Generated by 'django-admin startproject' using Django 3.0.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGIN_URL = '/social-login/'


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '9o_^k5*v7r=)jo(uwe9$97fv^6@tahz%cr5irl)pz=qyw61i6('
SOCIAL_AUTH_KEY = '14919125201-k0a1g3lh67n962e1fhje5kvl5k5ktp24.apps.googleusercontent.com'
SOCIAL_AUTH_SECRET = 'w9C1yMBFBNAHHLLKp9uaiUZB'


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

LINE_CHANNEL_ACCESS_TOKEN = "qTom/4bZpS64f0qneaQYWTuq4gLmqstnnIq2vZOsN4KLhUnc/ShWOJ+yHd2e04N/OD0t52nHOsaYL9if/q+mPEXfxJHcijTFe7X13sdcgMtw08ZJ+FwyWO8vpVhCGqCpFjTlKlXmWnJbDAzjTiMfjgdB04t89/1O/w1cDnyilFU="
LINE_CHANNEL_SECRET = "14c9e6bf0b49a0119f0d6c05d3354bdd"

ALLOWED_HOSTS = [
    "dblinebot.herokuapp.com",
    "localhost",
    "127.0.0.1",
    "35.201.254.214",
    "compare.keybo.me"
]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "django.contrib.redirects",
    'COMPARE',
    'social_django',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',

    'mylinebot'
]
SOCIAL_AUTH_URL_NAMESPACE = 'social'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    "django.contrib.redirects.middleware.RedirectFallbackMiddleware",
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'DBproject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')], # <- 加入這個設置
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends', 
                'social_django.context_processors.login_redirect', 
            ],
        },
    },
]

WSGI_APPLICATION = 'DBproject.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.db'),
    }
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

TIME_ZONE = 'Asia/Taipei'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'COMPARE/templates/static'),
]





AUTHENTICATION_BACKENDS = (
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.github.GithubOAuth2',
    'django.contrib.auth.backends.ModelBackend',
) 
SOCIAL_AUTH_URL_NAMESPACE = 'social' 

SOCIAL_AUTH_GITHUB_KEY = '4b70d8d8ff98234c2b80'
SOCIAL_AUTH_GITHUB_SECRET = '750b8e6323745f59e7d95ff79bde80a3a54b08c4'
SOCIAL_AUTH_GITHUB_USE_OPENID_AS_USERNAME = True
SOCIAL_AUTH_GITHUB_SCOPE =['']

SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/oauth/callback' # 登陸成功之後的路由
SITE_ID = 1

LOGIN_REDIRECT_URL = '/'
