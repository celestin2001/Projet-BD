from django import forms
from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin


class UtilisateurForm(forms.ModelForm):
    class Meta:
        model = Utilisateur
        fields = '__all__'

    class Media:
        js = ('gestion_utilisateur/static/gestion_utilisateur/js/hide_fields.js',)  # Charger le script JavaScript

class CustomUserAdmin(UserAdmin):
    form = UtilisateurForm

    fieldsets = (
        (None, {
            'fields': ('username', 'email', 'password','last_name', 'role', 'pays','profil_picture'),
        }),
        ('Informations supplémentaires', {
            'fields': ('annee_experience', 'bio', 'valid_auteur'),
            'classes': ('collapse',),  # Permet de replier la section si nécessaire
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username','last_name', 'email', 'password', 'role', 'pays'),
        }),
        ('Informations supplémentaires', {
            'fields': ('annee_experience', 'bio', 'valid_auteur'),
            'classes': ('collapse',),
        }),
    )

    search_fields = ('username','last_name', 'email', 'pays', 'role')

    class Media:
        js = ('gestion_utilisateur/static/gestion_utilisateur/js/hide_fields.js',)  # Inclure le script JS pour cacher les champs

admin.site.register(Utilisateur, CustomUserAdmin)
# admin.site.register(Auteur)
admin.site.register(BlogPost)
admin.site.register(Evenement)
admin.site.site_title = "Plateforme DB"
admin.site.site_header = "Auteur DB"
admin.site.index_title = "Gestion des auteurs"
# admin.site.register(ParticipationEvenement)

