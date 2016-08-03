"""
WSGI config for partyfood project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""

# import os

# from django.core.wsgi import get_wsgi_application

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "partyfood.settings")

# application = get_wsgi_application()

import os
import sys

## assuming your Django settings file is at '/home/my_username/projects/my_project/settings.py'

path = '/home/winstonww/partyfood/'
if path not in sys.path:
    sys.path.append(path)


os.environ['DJANGO_SETTINGS_MODULE'] = 'partyfood.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

