from __future__ import absolute_import, unicode_literals

# Faire en sorte que Celery soit chargé avec l'application Django
from .celery import app as celery_app

__all__ = ('celery_app',)