from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-0m)9)s92=mg!j&_qdcx8)c*!o$bbfj(^+7%_mh5-)ia63j)ev!'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
# CART_SESSION_ID = 'cart'

ALLOWED_HOSTS = ["127.0.0.1", 'localhost', 'shopmoderno.ru']
INTERNAL_IPS = ["127.0.0.1"]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sites',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'moderno.apps.ModernoConfig',
    'users.apps.UsersConfig',
    'cart.apps.CartConfig',
    'like.apps.LikeConfig',
    'debug_toolbar',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'users.middleware.RedirectIfAuthenticatedMiddleware',
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

ROOT_URLCONF = 'shopmoderno.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'moderno.context_processors.get_info_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'shopmoderno.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
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

LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
# STATICFILES_DIRS = [
#     BASE_DIR / 'static',
# ]
MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_URL = '/media/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_REDIRECT_URL = 'moderno:home'
LOGOUT_REDIRECT_URL = 'users:login'
LOGIN_URL = 'users:login'

CSRF_TRUSTED_ORIGINS = ['http://127.0.0.1']

# AUTHENTICATION_BACKENDS = [
#     # 'social_core.backends.github.GithubOAuth2',
#     # 'social_core.backends.vk.VKOAuth2',
#     'django.contrib.auth.backends.ModelBackend',
#     'users.authentication.EmailAuthBackend',
# ]

# DEFAULT_USER_IMAGE = MEDIA_URL + 'users/default.png'
# DEFAULT_PRODUCT_IMAGE = MEDIA_URL + 'images/default.jpg'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

EMAIL_HOST_USER = 'kalaytanov93@gmail.com'
EMAIL_HOST_PASSWORD = 'iylgsbrhxnuarrxr'

# EMAIL_HOST = "smtp.yandex.ru"
# EMAIL_PORT = 465
# EMAIL_HOST_USER = "kalaitanov93@yandex.ru"
# EMAIL_HOST_PASSWORD = "bnufhkwcripaunvu"
# EMAIL_USE_SSL = True

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
SERVER_EMAIL = EMAIL_HOST_USER
EMAIL_ADMIN = EMAIL_HOST_USER

AUTH_USER_MODEL = 'users.User'
SITE_ID = 1