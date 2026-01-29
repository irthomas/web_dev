"""
WSGI config for djhello project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os
import sys
from django.core.wsgi import get_wsgi_application

sys.path.append('/var/www/web_dev/djhello')
os.environ["DJANGO_SETTINGS_MODULE"] = "djhello.settings"

application = get_wsgi_application()

