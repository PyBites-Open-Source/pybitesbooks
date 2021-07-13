from decouple import config
import dj_database_url

from myreadinglist.settings import *  # noqa F403

STATICFILES_STORAGE = ''
TEST_DB = config('TEST_DATABASE_URL',
                 'sqlite:///test.db')
DATABASES = {
    'default': dj_database_url.config(
        default=TEST_DB
    )
}
