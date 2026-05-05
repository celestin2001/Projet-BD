from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import *


# ==========================
# FORMULAIRE CREATION USER
# ==========================
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = Utilisateur
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "is_auteur",
            "is_editeur",
            "is_libraire",
            "is_organisateur",
            "is_autre",
            "bio",
            "profil_picture",
            "pays",
            "date_naissance",
            "telephone",
            "ville_residence",
            "genres",
        )


# ==========================
# FORMULAIRE MODIFICATION USER
# ==========================
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = Utilisateur
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "is_auteur",
            "is_editeur",
            "is_libraire",
            "is_organisateur",
            "is_autre",
            "bio",
            "profil_picture",
            "pays",
            "valid",
            "vedette",
            "date_naissance",
            "telephone",
            "ville_residence",
            "genres",
        )


# ==========================
# ADMIN UTILISATEUR
# ==========================
class UtilisateurAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = Utilisateur

    list_display = ("username", "email", "first_name", "last_name", "is_auteur", "is_editeur", "is_staff")
    search_fields = ("username", "email", "first_name", "last_name")
    ordering = ("username",)

    # MODIFICATION
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Informations personnelles", {
            "fields": ("first_name", "last_name", "email")
        }),
        ("Permissions", {
            "fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")
        }),
        ("Dates importantes", {"fields": ("last_login", "date_joined")}),

        ("Informations supplémentaires", {
            "fields": (
                "is_auteur",
                "is_editeur",
                "is_libraire",
                "is_organisateur",
                "is_autre",
                "bio",
                "profil_picture",
                "pays",
                "valid",
                "vedette",
                "date_naissance",
                "telephone",
                "ville_residence",
                "genres",
            )
        }),
    )

    # CREATION
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "password1", "password2"),
        }),
        ("Informations personnelles", {
            "fields": ("email", "first_name", "last_name"),
        }),
        ("Informations supplémentaires", {
            "fields": (
                "is_auteur",
                "is_editeur",
                "is_libraire",
                "is_organisateur",
                "is_autre",
                "bio",
                "profil_picture",
                "pays",
                "date_naissance",
                "telephone",
                "ville_residence",
                "genres",
            )
        }),
    )


from django import forms
from django.forms.widgets import TextInput

class ColorInput(TextInput):
    input_type = 'color'

from colorfield.fields import ColorField

class EvenementAdminForm(forms.ModelForm):
    couleur_evenement = forms.CharField(
        widget=forms.TextInput(attrs={'type': 'color', 'style': 'height: 40px; width: 60px; padding: 0; cursor: pointer;'}),
        required=False,
        label="Couleur de l'événement"
    )
    class Meta:
        model = Evenement
        fields = '__all__'

# ==========================
# ADMIN EVENEMENT
# ==========================
class EvenementList(admin.ModelAdmin):
    form = EvenementAdminForm
    formfield_overrides = {
        ColorField: {'widget': forms.TextInput(attrs={'type': 'color', 'style': 'height: 40px; width: 60px; padding: 0; cursor: pointer;'})},
    }
    list_display = ['titre_evenement', 'date_evenement', 'date_fin_evenement', 'organisateur', 'valide', 'couleur_evenement']
    list_filter = ['valide', 'date_evenement', 'organisateur']
    fields = (
        'valide',
        'organisateur',
        'titre_evenement',
        'description',
        'image',
        'couleur_evenement',
        'date_evenement',
        'date_fin_evenement',
        'heure_evenement',
        'lieu_evenement'
    )

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == 'couleur_evenement':
            kwargs['widget'] = forms.TextInput(attrs={'type': 'color', 'style': 'height: 40px; width: 60px; padding: 0; cursor: pointer;'})
        return super().formfield_for_dbfield(db_field, request, **kwargs)


# ==========================
# ENREGISTREMENT
# ==========================
admin.site.register(Utilisateur, UtilisateurAdmin)  # ✅ IMPORTANT
admin.site.register(Social_link)
admin.site.register(BlogPost)
admin.site.register(Evenement, EvenementList)


# ==========================
# CONFIG ADMIN
# ==========================
admin.site.site_title = "Plateforme DB"
admin.site.site_header = "Auteur DB"
admin.site.index_title = "Gestion des auteurs"