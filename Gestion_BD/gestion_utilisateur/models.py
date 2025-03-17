from django.db import models
from django.contrib.auth.models import AbstractUser


class Utilisateur(AbstractUser):
    Role_choice = [
        ('auteur','auteur'),
        ('lecteur','lecteur')
        
    ]
    Annee_Experience = [
        ('0-2 ans','0-2 ans'),
        ('3-5 ans','3-5 ans'),
        ('5-10 ans','5-10 ans'),
        ('plus de 10 ans','plus de 10 ans')
    ]
    
    PAYS_AFRICAINS = [
    ("DZ", "Algérie"), ("AO", "Angola"), ("BJ", "Bénin"), ("BW", "Botswana"), ("BF", "Burkina Faso"),
    ("BI", "Burundi"), ("CM", "Cameroun"), ("CV", "Cap-Vert"), ("CF", "République Centrafricaine"),
    ("TD", "Tchad"), ("KM", "Comores"), ("CG", "Congo-Brazzaville"), ("CD", "Congo-Kinshasa"),
    ("DJ", "Djibouti"), ("EG", "Égypte"), ("GQ", "Guinée Équatoriale"), ("ER", "Érythrée"),
    ("SZ", "Eswatini"), ("ET", "Éthiopie"), ("GA", "Gabon"), ("GM", "Gambie"), ("GH", "Ghana"),
    ("GN", "Guinée"), ("GW", "Guinée-Bissau"), ("CI", "Côte d'Ivoire"), ("KE", "Kenya"),
    ("LS", "Lesotho"), ("LR", "Libéria"), ("LY", "Libye"), ("MG", "Madagascar"), ("MW", "Malawi"),
    ("ML", "Mali"), ("MR", "Mauritanie"), ("MU", "Maurice"), ("MA", "Maroc"), ("MZ", "Mozambique"),
    ("NA", "Namibie"), ("NE", "Niger"), ("NG", "Nigéria"), ("RW", "Rwanda"), ("ST", "Sao Tomé-et-Principe"),
    ("SN", "Sénégal"), ("SC", "Seychelles"), ("SL", "Sierra Leone"), ("SO", "Somalie"), ("ZA", "Afrique du Sud"),
    ("SS", "Soudan du Sud"), ("SD", "Soudan"), ("TZ", "Tanzanie"), ("TG", "Togo"), ("TN", "Tunisie"),
    ("UG", "Ouganda"), ("ZM", "Zambie"), ("ZW", "Zimbabwe")
]

    role = models.CharField(max_length=120, choices=Role_choice,default='lecteur')
    annee_experience = models.CharField(max_length=120, choices=Annee_Experience,blank=True, null=True)
    bio = models.TextField()
    email = models.EmailField(unique=True)
    profil_picture = models.ImageField(upload_to='media/',blank=True,null=True)
   
    # password_confirme = models.CharField(max_length=50)
    token = models.CharField(max_length=120)
    pays = models.CharField(max_length=100, choices=PAYS_AFRICAINS, default="CM",null=True)
    valid_auteur = models.BooleanField(default=False)

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
    user = models.ForeignKey(Utilisateur, on_delete=models.CASCADE,related_name="social_link")
    platform = models.CharField(max_length=120)
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
    valid = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Evenement(models.Model):
    titre_evenement = models.CharField(max_length=125)
    description = models.TextField()
    image = models.ImageField(upload_to='media/',blank=True,null=True)
    date_evenement = models.DateField()
    date_fin = models.DateField(null=True,blank=True)


   

