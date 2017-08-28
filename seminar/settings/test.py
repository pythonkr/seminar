
from .base import *

# https://docs.travis-ci.com/user/database-setup/#PostgreSQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'seminar_test',
        'USER': 'postgres',
        'HOST': 'localhost',
        'PORT': '',
    }
}
