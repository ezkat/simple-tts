from django.apps import AppConfig
from logging import getLogger
from sys import argv
import os

logger = getLogger()

class ConversionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'conversion'


    def ready(self):
        if not any(i in ('makemigrations', 'migrate', 'createsuperuser', 'shell') for i in argv):
            if os.environ.get('RUN_MAIN', None) == 'true':
                logger.info('Poller already running')
                return
            from .polling import Poll
            Poll()
