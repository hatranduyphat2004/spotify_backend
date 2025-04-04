"""
Django settings for backend project.

Generated by 'django-admin startproject' using Django 4.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
from datetime import timedelta


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-s8^u1j%7m_m3w&(e)439lpp-t20o+yj^2ztp!&53%v40i)0xu0'

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

    'api',
    'corsheaders',
    'rest_framework_simplejwt',
    'rest_framework',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = 'backend.urls'

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

WSGI_APPLICATION = 'backend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.mysql',  # Sử dụng MySQL
    #     'NAME': 'spotify',  # Thay bằng tên database của bạn
    #     'USER': 'root',  # Tài khoản MySQL
    #     'PASSWORD': '',  # Mật khẩu MySQL
    #     'HOST': 'localhost',  # Nếu dùng máy chủ từ xa, thay bằng IP
    #     'PORT': '2434',  # Cổng của P
    #     # 'PORT': '',  # Cổng theo máy
    #     'OPTIONS': {
    #         'charset': 'utf8mb4',  # Hỗ trợ Unicode đầy đủ
    #     },
    # }

    #Luan
     'default': {
        'ENGINE': 'django.db.backends.mysql',  # Sử dụng MySQL
        'NAME': 'spotify',  # Thay bằng tên database của bạn
        'USER': 'root',  # Tài khoản MySQL
        'PASSWORD': '1234',  # Mật khẩu MySQL
        'HOST': '127.0.0.1',  # Nếu dùng máy chủ từ xa, thay bằng IP
        'PORT': '3306',  # Cổng của MySQL
        'OPTIONS': {
            'charset': 'utf8mb4',  # Hỗ trợ Unicode đầy đủ
        },
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ]
}

# JWT
SIMPLE_JWT = {
    'USER_ID_FIELD': 'id',  # ✅ Chỉ định đúng trường khóa chính
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),  # Thời gian sống của Access Token
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),     # Thời gian sống của Refresh Token
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "AUTH_HEADER_TYPES": ("Bearer",),  # Header bắt đầu bằng "Bearer <token>"
}
CORS_ALLOW_ALL_ORIGINS = True  # Chấp nhận tất cả domain
CORS_ALLOW_CREDENTIALS = True


MEDIA_URL = '/media/'  # URL để truy cập file uploads
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')  # Thư mục lưu trữ file uploads

# In settings.py
AUTH_USER_MODEL = 'api.User'
AUTHENTICATION_BACKENDS = ['django.contrib.auth.backends.ModelBackend']
