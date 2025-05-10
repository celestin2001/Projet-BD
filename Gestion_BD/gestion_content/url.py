

from django.urls import path
from .views import *

urlpatterns = [
  path('auteur',Auteur,name='auteur'),
  path('detail/<int:auteur_id>/', detail_auteur, name='detail_auteur'),
  path('actualite',actualite,name='actualite'),
  path('texte',text_affichage, name='texte'),
  path('texte_mail',texte_mail, name='texte_mail'),
  path('profil_auteur',profil_auteur,name="profil_auteur"),
  path('apropos',apropos,name='apropos'),
]
