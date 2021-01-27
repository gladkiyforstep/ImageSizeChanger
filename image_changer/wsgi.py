"""
WSGI config for image_changer project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this is_file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'image_changer.settings')

application = get_wsgi_application()
