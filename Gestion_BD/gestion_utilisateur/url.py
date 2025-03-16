
from django.urls import path
from .views import *
urlpatterns = [
    
    path('signup',signup,name='signup'),
    path('signin',signin,name='signin'),
    path('deconnexion',deconnexion,name='deconnexion'),
     path('',Home,name='home'),
     path('evenement',Evenements,name='evenement'),
    path('event_detail/<int:my_id>/',detail_evenement,name='event_detail'),
    path('signin_auteur',signin_auteur,name="signin_auteur")
]