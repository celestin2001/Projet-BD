# gestion_bd/celery.py
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Définir le module par défaut de settings pour Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Gestion_BD.settings')

# Créer une instance de Celery
app = Celery('Gestion_BD')

# Utiliser une configuration de Celery depuis les settings de Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Charger les tâches depuis tous les modules 'tasks' dans les applications Django
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
