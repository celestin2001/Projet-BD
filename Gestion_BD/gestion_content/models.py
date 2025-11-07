from django.db import models
from gestion_utilisateur.models import *

class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    
class Work(models.Model):
    choix_edition = [
        ('Numerique','Numerique'),
        ('Physique','Physique'),
        ('Physique_&_Numerique','Physique_&_Numerique')
    ]
    choix_genre = [
        ('Comedie','Comedie'),
        ('Aventure','Aventure'),
        ('Fantastique','Fantastique'),
        ('Histoire','Histoire'),
        ('Humour','Humour'),
        ('Science-fiction','Science-fiction'),
        ('Jeunesse','Jeunesse'),
        ('Suspense','Suspense'),
        ('Western','Western'),
        ('Romance','Romance'),
        ('Polar','Polar'),
        ('Tranche_de_vie','Tranche_de_vie')
    ]
    
    edition = models.CharField(max_length=50,choices=choix_edition,default='Physique')
    title = models.CharField(max_length=255)
    author = models.ForeignKey('gestion_utilisateur.Utilisateur', on_delete=models.CASCADE, related_name='works')  
    publication_date = models.DateField()
    cover_image = models.ImageField(upload_to='media/', blank=True, null=True)
    description = models.TextField()
    genres = models.CharField(max_length=50,choices=choix_genre,default='Comedie')
    valid = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Notation(models.Model):
    user = models.ForeignKey('gestion_utilisateur.Utilisateur', on_delete=models.CASCADE, related_name='notation')  # ✅ Ici aussi
    work = models.ForeignKey(Work, on_delete=models.CASCADE, related_name='notation')
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # Note entre 1 et 5
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def notation_auteur(self):
        
        return sum(self.rating)

    def __str__(self):
        return f"{self.user.username} - {self.work.title} - {self.rating}"
    
    



#    class Genre(models.Model):
#     name = models.CharField(max_length=100, unique=True)

#     def __str__(self):
#         return self.name
    


