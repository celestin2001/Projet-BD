"""
WSGI config for Gestion_BD project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os
import sys

sys.path.insert(0, 'E:/projet_BD/Gestion_BD')
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Gestion_BD.settings')

application = get_wsgi_application()
