

from django.urls import path
from .views import *

urlpatterns = [
  path('',home,name='home'),
  path('detail/<int:auteur_id>/', detail_auteur, name='detail_auteur'),
  
 
]
