from django.contrib import admin
from .models import *

admin.site.register(Utilisateur)
admin.site.register(Auteur)
admin.site.register(BlogPost)
