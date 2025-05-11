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
    ("Algérie", "Algérie"), ("Angola", "Angola"), ("Bénin", "Bénin"), ("Botswana", "Botswana"), 
    ("Burkina Faso", "Burkina Faso"), ("Burundi", "Burundi"), ("Cameroun", "Cameroun"), 
    ("Cap-Vert", "Cap-Vert"), ("République Centrafricaine", "République Centrafricaine"), 
    ("Tchad", "Tchad"), ("Comores", "Comores"), ("Congo-Brazzaville", "Congo-Brazzaville"), 
    ("Congo-Kinshasa", "Congo-Kinshasa"), ("Djibouti", "Djibouti"), ("Égypte", "Égypte"), 
    ("Guinée Équatoriale", "Guinée Équatoriale"), ("Érythrée", "Érythrée"), ("Eswatini", "Eswatini"), 
    ("Éthiopie", "Éthiopie"), ("Gabon", "Gabon"), ("Gambie", "Gambie"), ("Ghana", "Ghana"), 
    ("Guinée", "Guinée"), ("Guinée-Bissau", "Guinée-Bissau"), ("Côte d'Ivoire", "Côte d'Ivoire"), 
    ("Kenya", "Kenya"), ("Lesotho", "Lesotho"), ("Libéria", "Libéria"), ("Libye", "Libye"), 
    ("Madagascar", "Madagascar"), ("Malawi", "Malawi"), ("Mali", "Mali"), ("Mauritanie", "Mauritanie"), 
    ("Maurice", "Maurice"), ("Maroc", "Maroc"), ("Mozambique", "Mozambique"), ("Namibie", "Namibie"), 
    ("Niger", "Niger"), ("Nigéria", "Nigéria"), ("Rwanda", "Rwanda"), ("Sao Tomé-et-Principe", "Sao Tomé-et-Principe"), 
    ("Sénégal", "Sénégal"), ("Seychelles", "Seychelles"), ("Sierra Leone", "Sierra Leone"), 
    ("Somalie", "Somalie"), ("Afrique du Sud", "Afrique du Sud"), ("Soudan du Sud", "Soudan du Sud"), 
    ("Soudan", "Soudan"), ("Tanzanie", "Tanzanie"), ("Togo", "Togo"), ("Tunisie", "Tunisie"), 
    ("Ouganda", "Ouganda"), ("Zambie", "Zambie"), ("Zimbabwe", "Zimbabwe")
]


    role = models.CharField(max_length=120, choices=Role_choice,default='lecteur')
   
    bio = models.TextField()
    email = models.EmailField(unique=True)
    profil_picture = models.ImageField(upload_to='media/',blank=True,null=True)
    genres = models.ManyToManyField("gestion_content.Genre", related_name="auteurs", blank=True, null=True)
   
    # password_confirme = models.CharField(max_length=50)
    token = models.CharField(max_length=120)
    pays = models.CharField(max_length=100, choices=PAYS_AFRICAINS, default="Cameroun",null=True)
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
    date_fin_evenement = models.DateField(null=True, blank=True)
    lieu_evenement = models.CharField(max_length=255, null=True, blank=True)
    date_publication = models.DateField(auto_now=True)
    heure_evenement = models.TimeField(null=True, blank=True)

class ParticipationEvenement(models.Model):
    evenement = models.ForeignKey(Evenement,on_delete=models.CASCADE)
    prenom = models.CharField(max_length=100)
    nom = models.CharField(max_length=100)
    email = models.EmailField()
    telephone = models.CharField(max_length=20)
    date_participation = models.DateTimeField(blank=True,null=True)

    def __str__(self):
        return f"{self.prenom} {self.nom}"


   

