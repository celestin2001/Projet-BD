from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin):
    # Masquer les champs groupes et permissions lors de la création
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password','pays','annee_experience','role','bio','valid_auteur'),
        }),
    )
    fieldsets = (
        (None, {
            'fields': ('username', 'email', 'password', 'pays', 'annee_experience', 'role', 'bio', 'valid_auteur'),
        }),
    )
search_fields = ('username', 'email', 'pays', 'role')
admin.site.register(Utilisateur,CustomUserAdmin)
# admin.site.register(Auteur)
admin.site.register(BlogPost)
admin.site.register(Evenement)
