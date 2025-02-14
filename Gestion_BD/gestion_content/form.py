from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Avg
from gestion_utilisateur.models import Auteur, Utilisateur
from gestion_content.models import Work, Notation
from django.contrib.auth.decorators import login_required
from django import forms

# Formulaire pour gérer les notations et commentaires
class NotationForm(forms.ModelForm):
    class Meta:
        model = Notation
        fields = ['work', 'rating', 'comment']
        widgets = {
            'rating': forms.Select(choices=[(i, i) for i in range(1, 6)]),
            'comment': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Votre commentaire...'}),
        }


