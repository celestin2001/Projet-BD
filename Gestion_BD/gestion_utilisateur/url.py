
from django.urls import path
from .views import *
urlpatterns = [
    
    path('signup',signup,name='signup'),
    path('signin',signin,name='signin'),
    path('deconnexion',deconnexion,name='deconnexion'),
     path('',Home,name='home'),
    path('detail_actu/<int:my_id>/',detail_actualite,name='detail_actualite'),
     path('evenement',Evenements,name='evenement'),
    path('event_detail/<int:my_id>/',detailEvenement,name='event_detail'),
    path('signin_auteur',signin_auteur,name="signin_auteur"),
    path('inscription_event/<int:my_id>/',inscription_evenement,name='inscription_event'),
]