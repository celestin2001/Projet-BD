from django.db import models
from django.contrib.auth.models import AbstractUser
from  gestion_content.models import Genre,Work

class Utilisateur(AbstractUser):
    Role_choice = [
        ('auteur','auteur'),
        ('lecteur','lecteur'),
        ('administrateur','administrateur')
    ]
    role = models.CharField(max_length=120, choices=Role_choice,default='lecteur')
    bio = models.TextField()
    profil_picture = models.ImageField(upload_to='media/',blank=True,null=True)
   
    password_confirme = models.CharField(max_length=50)
    token = models.CharField(max_length=120)

   

class Auteur(models.Model):
    user = models.OneToOneField(Utilisateur, on_delete=models.CASCADE, related_name='auteur')
    pays = models.CharField(max_length=100, blank=True, null=True)
    genres = models.ManyToManyField('gestion_content.Genre', blank=True)  
    social_links = models.JSONField(default=dict, blank=True,null=True)  # Dictionnaire pour les réseaux sociaux

    def nombre_oeuvres(self):
        return self.works.count()   # Récupère le nombre de posts de cet auteur

    def __str__(self):
        return self.user.username

class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(Auteur, on_delete=models.SET_NULL, null=True, related_name='blog_posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title



   

