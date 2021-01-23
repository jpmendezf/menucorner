import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
SECRET_KEY = "4wkb*12q$$ih+kibcfjp--kumu99&z-4o0je6-jv_ed%ui4e4r"
DEBUG = True
ALLOWED_HOSTS = ['*']
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "debug_toolbar",
    "menu",
    "ckeditor",
    "ckeditor_uploader",
]
MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
ROOT_URLCONF = "menu.urls"
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]
WSGI_APPLICATION = "menu.wsgi.application"
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",},
]
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True
STATIC_URL = "/opt/bitnami/apache/htdocs/menucorner2/static/"
STATICFILES_DIRS = []
LOGIN_URL = "/login/"
LOGIN_REDIRECT_URL = "/menus/"
INTERNAL_IPS = ["127.0.0.1"]
DJANGO_WYSIWYG_FLAVOR = "ckeditor"
CKEDITOR_JQUERY_URL = 'https://ajax.googleapis.com/ajax/libs/jquery/2.2.4/jquery.min.js'
CKEDITOR_RESTRICT_BY_USER = True #Only who upload image see it
CKEDITOR_UPLOAD_PATH = 'uploads/'
CKEDITOR_BROWSE_SHOW_DIRS = True # Shows directory of image in the server
CKEDITOR_RESTRICT_BY_DATE = True # Arranges image in terms of date uploaded
CKEDITOR_IMAGE_BACKEND = "pillow"
STATIC_ROOT = '/opt/bitnami/apache/htdocs/menucorner2/static/'

EMAIL_BACKEND = "sendgrid_backend.SendgridBackend"


SENDGRID_API_KEY = os.getenv('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')

EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = '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' # this is exactly the value 'apikey'
EMAIL_HOST_PASSWORD = SENDGRID_API_KEY
DEFAULT_FROM_EMAIL  = 'pablo@team.cr'

EMAIL_PORT = 587
EMAIL_USE_TLS = True

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': None,
        'extraPlugins': 'codesnippet',
    },
}