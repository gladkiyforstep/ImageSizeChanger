"""
ASGI config for image_changer project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this is_file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'image_changer.settings')

application = get_asgi_application()
