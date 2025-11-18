from django.contrib import admin
from .models import *

class title(admin.ModelAdmin):
    list_display = ('utilisateur','nom')
    
admin.site.register(Work)
admin.site.register(Genre)
admin.site.register(Notation)
admin.site.register(Librairie)
admin.site.site_title = "Plateforme DB"
admin.site.site_header = "Auteur DB"
admin.site.index_title = "Gestion des auteurs"
admin.site.register(Contact)
admin.site.register(Editeur,title)
admin.site.register(Bdtheque)
admin.site.register(Auteur)



