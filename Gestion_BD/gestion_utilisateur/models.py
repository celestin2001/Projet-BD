from django.db import models
from django.contrib.auth.models import AbstractUser


class Utilisateur(AbstractUser):
    Role_choice = [
        ('auteur','auteur'),
        ('editeur','editeur'),
        ('libraire','libraire'),
        ('organisateur_Evènement','organisateur_Evènement'),  
        ('autre','autre'),
       
        
    ]
  
    
    PAYS_AFRICAINS = [
        ("dz", "Algérie"), ("ao", "Angola"), ("bj", "Bénin"), ("bw", "Botswana"),
        ("bf", "Burkina Faso"), ("bi", "Burundi"), ("cm", "Cameroun"),
        ("cv", "Cap-Vert"), ("cf", "République Centrafricaine"),
        ("td", "Tchad"), ("km", "Comores"), ("cg", "Congo-Brazzaville"),
        ("cd", "Congo-Kinshasa"), ("dj", "Djibouti"), ("eg", "Égypte"),
        ("gq", "Guinée Équatoriale"), ("er", "Érythrée"), ("sz", "Eswatini"),
        ("et", "Éthiopie"), ("ga", "Gabon"), ("gm", "Gambie"), ("gh", "Ghana"),
        ("gn", "Guinée"), ("gw", "Guinée-Bissau"), ("ci", "Côte d'Ivoire"),
        ("ke", "Kenya"), ("ls", "Lesotho"), ("lr", "Libéria"), ("ly", "Libye"),
        ("mg", "Madagascar"), ("mw", "Malawi"), ("ml", "Mali"), ("mr", "Mauritanie"),
        ("mu", "Maurice"), ("ma", "Maroc"), ("mz", "Mozambique"), ("na", "Namibie"),
        ("ne", "Niger"), ("ng", "Nigéria"), ("rw", "Rwanda"), ("st", "Sao Tomé-et-Principe"),
        ("sn", "Sénégal"), ("sc", "Seychelles"), ("sl", "Sierra Leone"),
        ("so", "Somalie"), ("za", "Afrique du Sud"), ("ss", "Soudan du Sud"),
        ("sd", "Soudan"), ("tz", "Tanzanie"), ("tg", "Togo"), ("tn", "Tunisie"),
        ("ug", "Ouganda"), ("zm", "Zambie"), ("zw", "Zimbabwe")
    ]


    role = models.CharField(max_length=120, choices=Role_choice,default='auteur')
   
    bio = models.TextField()
    email = models.EmailField(unique=True)
    profil_picture = models.ImageField(upload_to='media/',blank=True,null=True)
    genres = models.ManyToManyField("gestion_content.Genre", related_name="auteurs", blank=True, null=True)
   
    # password_confirme = models.CharField(max_length=50)
    # token = models.CharField(max_length=120,null=True)
    pays = models.CharField(max_length=100, choices=PAYS_AFRICAINS, default="Cameroun",null=True)
    valid = models.BooleanField(default=False)
    vedette = models.BooleanField(default=False)
    date_naissance = models.DateField(null=True, blank=True)
    telephone = models.CharField(max_length=20, null=True, blank=True)
    ville_residence = models.CharField(max_length=100, null=True, blank=True)

    USERNAME_FIELD = 'email'  #  l'email pour l'authentification
    REQUIRED_FIELDS = ['username']

    def nombre_oeuvres(self):
         return self.works.count()
    
    def get_drapeau(self):
        """Retourne l'URL du drapeau basé sur le code pays."""
        return f"https://flagcdn.com/w40/{self.pays.lower()}.png"

    def __str__(self):
        return f"{self.username}"

class Social_link(models.Model):
    lien = [
        ('Facebook','Facebook'),
        ('Instagram','Instagram'),
        ('TikTok','TikTok'),
        ('LinkedIn','LinkedIn'),
        ('Site-web','Site-web')
    ]
    user = models.ForeignKey(Utilisateur, on_delete=models.CASCADE,related_name="social_link")
    plateforme = models.CharField(max_length=120,choices=lien,null=True)
    url = models.URLField()

    def __str__(self):
        return self.url
   

# class Auteur(models.Model):
#     user = models.OneToOneField(Utilisateur, on_delete=models.CASCADE, related_name='auteur')
#     pays = models.CharField(max_length=100, blank=True, null=True)
#     genres = models.ManyToManyField('gestion_content.Genre', blank=True)  
#     social_links = models.JSONField(default=dict, blank=True,null=True)  # Dictionnaire pour les réseaux sociaux

#     def nombre_oeuvres(self):
#         return self.works.count()   # Récupère le nombre de posts de cet auteur

#     def __str__(self):
#         return self.user.username

class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(Utilisateur, on_delete=models.SET_NULL, null=True, related_name='blog_posts')
    created_at = models.DateTimeField(auto_now_add=True)
    media = models.ImageField(upload_to='media/',blank=True,null=True)
    url_actu = models.URLField(null=True,blank=True)
    valid = models.BooleanField(default=False)

    def __str__(self):
        return self.title

from colorfield.fields import ColorField
class Evenement(models.Model):
    titre_evenement = models.CharField(max_length=125)
    description = models.TextField()
    image = models.ImageField(upload_to='media/',blank=True,null=True)
    date_evenement = models.DateField()
    date_fin_evenement = models.DateField(null=True, blank=True)
    lieu_evenement = models.CharField(max_length=255, null=True, blank=True)
    date_publication = models.DateField(auto_now=True)
    heure_evenement = models.TimeField(null=True, blank=True)
    couleur_evenement = ColorField(
        default='#007bff', 
        verbose_name="Couleur de l'événement"
    )

class ParticipationEvenement(models.Model):
    evenement = models.ForeignKey(Evenement,on_delete=models.CASCADE)
    prenom = models.CharField(max_length=100)
    nom = models.CharField(max_length=100)
    email = models.EmailField()
    telephone = models.CharField(max_length=20)
    date_participation = models.DateTimeField(blank=True,null=True)

    def __str__(self):
        return f"{self.prenom} {self.nom}"




   

