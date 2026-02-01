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
admin.site.register(Auteur)

@admin.register(Editeur)
class EditeurAdmin(admin.ModelAdmin):
    list_display = ('nom', 'nom_contact_1', 'email_contact_1', 'pays_siege')
    search_fields = ('nom', 'nom_contact_1')
    fieldsets = (
        ('Info Maison d\'édition', {'fields': ('utilisateur', 'nom', 'logo', 'description')}),
        ('Contact Principal', {'fields': ('nom_contact_1', 'role_contact_1', 'tel_contact_1', 'email_contact_1')}),
        ('Contact Secondaire', {'fields': ('nom_contact_2', 'role_contact_2', 'tel_contact_2', 'email_contact_2')}),
    )

@admin.register(Bdtheque)
class BdthequeAdmin(admin.ModelAdmin):
    list_display = ('titre', 'edition', 'autre_editeur_nom', 'valide', 'date_publication')
    list_filter = ('valide', 'type_oeuvre', 'edition')
    search_fields = ('titre', 'autre_editeur_nom')
    actions = ['valider_oeuvres']

    def valider_oeuvres(self, request, queryset):
        queryset.update(valide=True)
    valider_oeuvres.short_description = "Valider les œuvres sélectionnées"



