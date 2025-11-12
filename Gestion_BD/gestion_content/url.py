

from django.urls import path
from .views import *

urlpatterns = [
  path('auteur',auteur,name='auteur'),
  path('detail/<int:auteur_id>/', detail_auteur, name='detail_auteur'),
  path('actualite',actualite,name='actualite'),
  path('texte',text_affichage, name='texte'),
  path('texte_mail',texte_mail, name='texte_mail'),
  path('profil_auteur',profil_auteur,name="profil_auteur"),
  path('apropos',apropos,name='apropos'),
  path('page404',custom_404_view,name="page404"),
  path('librairies',Librairies,name="Librairie"),
  path('librairie/<int:librairie_id>/',detail_librairie, name='detail_librairie'),
  path('editeur',editeur, name='editeur'),
  path('editeur/<int:id>/', editeur_detail_view, name='editeur_detail'),
  path('bdtheque',bdtheque , name='bdtheque'),
 
]
