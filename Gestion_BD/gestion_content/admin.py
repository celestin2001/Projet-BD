from django.contrib import admin
from django import forms
from .models import *

class title(admin.ModelAdmin):
    list_display = ('utilisateur','nom')
    
class WorkImageInline(admin.TabularInline):
    model = WorkImage
    extra = 1


class PlancheInline(admin.TabularInline):
    model = Planche
    extra = 1


class TomeInline(admin.StackedInline):
    model = Tome
    extra = 1
    fields = ('numero', 'image')

@admin.register(Work)
class WorkAdmin(admin.ModelAdmin):
    class WorkAdminForm(forms.ModelForm):
        class Meta:
            model = Work
            fields = '__all__'
            labels = {
                'cover_image': 'Couverture (Tome 1)'
            }

    form = WorkAdminForm
    inlines = [WorkImageInline, TomeInline]
admin.site.register(Genre)
admin.site.register(Notation)
admin.site.register(Librairie)
admin.site.site_title = "Plateforme DB"
admin.site.site_header = "Auteur DB"
admin.site.index_title = "Gestion des auteurs"
admin.site.register(Contact)
admin.site.register(Auteur)

@admin.register(Tome)
class TomeAdmin(admin.ModelAdmin):
    list_display = ('work', 'numero')
    search_fields = ('work__title',)
    list_filter = ('work',)
    inlines = [PlancheInline]

@admin.register(Planche)
class PlancheAdmin(admin.ModelAdmin):
    list_display = ('tome', 'work_title', 'planche_label')
    search_fields = ('tome__work__title', 'tome__numero')
    list_filter = ('tome__work', 'tome__numero')

    def work_title(self, obj):
        return obj.tome.work.title
    work_title.short_description = 'Oeuvre'

    def planche_label(self, obj):
        return f'Tome {obj.tome.numero}'
    planche_label.short_description = 'Tome'

admin.site.register(Jours)

@admin.register(Editeur)
class EditeurAdmin(admin.ModelAdmin):
    list_display = ('nom', 'nom_contact_1', 'email_contact_1', 'pays_siege')
    search_fields = ('nom', 'nom_contact_1')
    fieldsets = (
        ('Info Maison d\'édition', {'fields': ('utilisateur', 'nom', 'logo', 'description')}),
        ('Contact Principal', {'fields': ('nom_contact_1', 'role_contact_1', 'tel_contact_1', 'email_contact_1')}),
        ('Contact Secondaire', {'fields': ('nom_contact_2', 'role_contact_2', 'tel_contact_2', 'email_contact_2')}),
    )

class BdthequeImageInline(admin.TabularInline):
    model = BdthequeImage
    extra = 1

@admin.register(Bdtheque)
class BdthequeAdmin(admin.ModelAdmin):
    list_display = ('titre', 'edition', 'autre_editeur_nom', 'valide', 'date_publication')
    list_filter = ('valide', 'type_oeuvre', 'edition')
    search_fields = ('titre', 'autre_editeur_nom')
    actions = ['valider_oeuvres']
    inlines = [BdthequeImageInline]

    def valider_oeuvres(self, request, queryset):
        queryset.update(valide=True)
    valider_oeuvres.short_description = "Valider les œuvres sélectionnées"





