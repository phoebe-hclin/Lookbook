import os
import sys

path = '/home/fibi0822/lookbook'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'lookbook.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()