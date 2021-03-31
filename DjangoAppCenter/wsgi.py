"""
WSGI config for DjangoAppCenter project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

from DjangoAppCenter.utils import get_python_version

os.system("%s -m DjangoAppCenter prod collectstatic --noinput" % get_python_version())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoAppCenter.settings')
application = get_wsgi_application()
