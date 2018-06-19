import os
from configurations import Configuration

class AuthenticationMixin():

    LOGIN_REDIRECT_URL = '/profile/login_redirect/'
    # LOGOUT_REDIRECT_URL = '/music_library_app/index'
    LOGIN_URL = '/authentication_users/login'

class Base(AuthenticationMixin, Configuration):

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    SECRET_KEY = '#@55zbxrgcs(bu0__6i2fv=mf^#cm&6uy=wk@v'

    DEBUG = True

    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'django_extensions',
        'music_project',
        'library_api',
        'music_library_app',
        'authentication_users',
        'django_filters',
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
    ]

    ROOT_URLCONF = 'music_project.urls'

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

    WSGI_APPLICATION = 'music_project.wsgi.application'



    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
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


    REST_FRAMEWORK = {

        'DEFAULT_PERMISSION_CLASSES': (
            'rest_framework.permissions.IsAuthenticated',
        ),

        'DEFAULT_FILTER_BACKENDS':  (
            'django_filters.rest_framework.DjangoFilterBackend',
             ),
    }

    STATIC_ROOT = os.path.join(BASE_DIR, "static/")

    LANGUAGE_CODE = 'en-us'

    TIME_ZONE = 'UTC'

    USE_I18N = True

    USE_TZ = True

    STATIC_URL = '/static/'

    ALLOWED_HOSTS = ['127.0.0.1', '138.68.145.206']

class Dev(Base):
    INTERNAL_IPS = ('127.0.0.1',)
    DEBUG = True

class Prod(Base):
    DEBUG = False
