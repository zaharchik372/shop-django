import os
from datetime import timedelta
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'abcdefghijklmnopqrstuvwxyz0123456789'

DEBUG = True
ALLOWED_HOSTS = ['*']

SESSION_COOKIE_HTTPONLY = False

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'article.apps.ArticleConfig',
    'catalog.apps.CatalogConfig',
    'account.apps.AccountConfig',
    'cart.apps.CartConfig',
    'mptt',
    # 'debug_toolbar',
    'django.contrib.humanize',
    'axes'
]

INTERNAL_IPS = [
    '127.0.0.1',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'axes.middleware.AxesMiddleware',
]

AUTHENTICATION_BACKENDS = [
    'axes.backends.AxesBackend',
    'django.contrib.auth.backends.ModelBackend',
]

# Настройки django-axes
AXES_FAILURE_LIMIT = 5  # Количество попыток до блокировки
AXES_COOLOFF_TIME = 0.1  # Время блокировки в часах
AXES_LOCK_OUT_AT_FAILURE = True  # Блокировать при достижении лимита
AXES_RESET_ON_SUCCESS = True  # Сбрасывать счетчик при успешном входе

ROOT_URLCONF = 'config.urls'

TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'catalog.context_processors.catalog'
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

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

AUTH_USER_MODEL = 'account.User'

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True
DEFAULT_CHARSET = 'utf-8'

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Ensure the logs directory exists
# LOG_DIR = os.path.join(BASE_DIR, 'logs')
# if not os.path.exists(LOG_DIR):
#     os.makedirs(LOG_DIR)

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'formatters': {
#         'verbose': {
#             'format': '{levelname} {asctime} {module} {message}',
#             'style': '{',
#         },
#         'simple': {
#             'format': '{levelname} {message}',
#             'style': '{',
#         },
#     },
#     'handlers': {
#         'console': {
#             'class': 'logging.StreamHandler',
#             'formatter': 'simple',
#         },
#         'file': {
#             'class': 'logging.FileHandler',
#             'filename': os.path.join(LOG_DIR, 'django.log'),
#             'formatter': 'verbose',
#         },
#     },
#     'root': {
#         'handlers': ['console', 'file'],
#         'level': 'DEBUG',
#     },
#     'django': {
#         'handlers': ['console', 'file'],
#         'level': 'DEBUG',
#         'propagate': False,
#     },
# }

LOGIN_REDIRECT_URL = '/'

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# Добавление WhiteNoise для обслуживания медиа-файлов
WHITENOISE_ALLOW_ALL_ORIGINS = True


