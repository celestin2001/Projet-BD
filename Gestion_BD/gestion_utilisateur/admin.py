from django import forms
from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin




class EvenementList(admin.ModelAdmin):
    list_display = ['titre_evenement','date_evenement','date_fin_evenement','couleur_evenement']
    fields = (
        'titre_evenement', 
        'description', 
        'image', 
        # Le champ apparaît tel quel, comme un simple champ de texte
        'couleur_evenement', 
        'date_evenement', 
        'date_fin_evenement', 
        'heure_evenement', 
        'lieu_evenement'
    )
admin.site.register(Utilisateur)
admin.site.register(Social_link)
# admin.site.register(Auteur)
admin.site.register(BlogPost)
admin.site.register(Evenement,EvenementList)
admin.site.site_title = "Plateforme DB"
admin.site.site_header = "Auteur DB"
admin.site.index_title = "Gestion des auteurs"
# admin.site.register(ParticipationEvenement)

