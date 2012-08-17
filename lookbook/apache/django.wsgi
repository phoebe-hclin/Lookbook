import os, sys

path = '/home/hainingwu/projects/look/improve_deploy/Lookbook/lookbook'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'lookbook.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()