from .base import *
import dj_database_url

DEBUG = False

SECRET_KEY = os.environ.get('SECRET_KEY')


DATABASES = {}
DATABASES['default'] = dj_database_url.config(conn_max_age=600)

ALLOWED_HOSTS = ['.herokuapp.com']
