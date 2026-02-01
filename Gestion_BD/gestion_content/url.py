

from django.urls import path
from .views import *

urlpatterns = [
  path('auteur',auteur,name='auteur'),
  path('detail/<int:auteur_id>/', detail_auteur_editeur, name='detail_auteur'),
  path('actualite',actualite,name='actualite'),
  path('texte',text_affichage, name='texte'),
  path('texte_mail',texte_mail, name='texte_mail'),
  path('profil_auteur',profil_auteur,name="profil_auteur"),
  path('apropos',apropos,name='apropos'),
  path('page404',custom_404_view,name="page404"),
  path('librairies',Librairies,name="Librairie"),
  path('librairie/<int:librairie_id>/',detail_librairie, name='detail_librairie'),
  path('editeur',editeur, name='editeur'),
  # path('editeur2',editeurs, name='editeur2'),
  path('editeur/<int:id>/', editeur_detail_view, name='editeur_detail'),
  # path('editeur/<int:id>/', editeur_detail, name='editeur_detail'),
  path('bdtheque',bdtheque , name='bdtheque'),
  path('auteur/<str:username>/galerie/',auteur_galerie_view, name='auteur_galerie_oeuvres'),
  path('editeur_input',input_editeur,name="input_editeur"),
  path('ajouter_bd',ajouter_bd,name="ajouter_bd"),
  # path('livre/<slug:slug>/', livre_detail_view, name='livre_detail'),
  path('modifier_bd/<int:id>/', modifier_bd, name='modifier_bd'),
  path('supprimer_bd/<int:id>/', supprimer_bd, name='supprimer_bd'),
  path('modifier_profil_editeur',modifier_profil_editeur,name="modifier_profil_editeur")
]
