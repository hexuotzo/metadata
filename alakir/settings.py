import os

import mimetypes

mimetypes.add_type("image/svg+xml", ".svg", True)
mimetypes.add_type("image/svg+xml", ".svgz", True)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '6h5ksb=sa3q&ydn2g^iimb7)8q6-z8c8gzxenl9j5hjo!%3i_6'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'adminlteui',
    # 'jet',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'metadata',
    # 'schedule',
    # 'dimdata',
    # 'userlabeldata',
    'projectrule',
    'treebeard',
    'usertags',
    'dimsource',
    'parkinglabel',
    'cloudserver'

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    #'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'alakir.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'alakir.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'metadata',
        'USER': 'admin',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': 3306 ,

    },
    'tags': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'label',
        'USER': 'admin',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': 3306,

    },
    'provide': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'data_provide',
        'USER': 'admin',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': 3306,

    }
}

DATABASE_ROUTERS = ['usertags.db_router.TagsdataRouter','dimsource.db_router.DimSourceRouter','parkinglabel.db_router.ParkingRouter']

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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

# jet
JET_SIDE_MENU_COMPACT = True
JET_DEFAULT_THEME = 'light-gray'
JET_THEMES = [
    {
        'theme': 'default',  # theme folder name
        'color': '#47bac1',  # color of the theme's button in user menu
        'title': 'Default'  # theme title
    },
    {
        'theme': 'green',
        'color': '#44b78b',
        'title': 'Green'
    },
    {
        'theme': 'light-green',
        'color': '#2faa60',
        'title': 'Light Green'
    },
    {
        'theme': 'light-violet',
        'color': '#a464c4',
        'title': 'Light Violet'
    },
    {
        'theme': 'light-blue',
        'color': '#5EADDE',
        'title': 'Light Blue'
    },
    {
        'theme': 'light-gray',
        'color': '#222',
        'title': 'Light Gray'
    }
]

APPEND_SLASH = True

STATIC_URL = '/static/'

LANGUAGE_CODE = 'zh-hans'

SITE_ID = 1

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATICFILES_DIRS = (
    ("css", os.path.join(STATIC_ROOT, 'css')),
    ("js", os.path.join(STATIC_ROOT, 'js')),
    ("img", os.path.join(STATIC_ROOT, 'img')),
    ("fonts", os.path.join(STATIC_ROOT, 'font')),
    ("adminlite_dist", os.path.join(STATIC_ROOT, 'adminlite_dist')),
    ("admin", os.path.join(STATIC_ROOT, 'admin')),
)

DEFAULT_CHARSET = 'utf-8'
DATETIME_FORMAT = 'Y-m-d H:i:s'
DATE_FORMAT = 'Y-m-d'

LOGIN_REDIRECT_URL  = '/admin/'

