"""
WSGI config for djdownloader project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application

sys.path.append('/var/www/web_dev/djdownloader')
os.environ["DJANGO_SETTINGS_MODULE"] = "djdownloader.settings"
#os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djdownloader.settings')

application = get_wsgi_application()
