from django.db import models
from django.urls import reverse
from gestion_utilisateur.models import *

# class Genre(models.Model):
#     name = models.CharField(max_length=100, unique=True)

    # def __str__(self):
    #     return self.name
    
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
    choix_influence = [
        ('Franco-Belge','Franco-Belge'),
        ('Comic-US','Comic-US'),
        ('manga','manga'),
        ('webton','webton'),
        ('fusion','fusion'),
        ('alternative','alternative')
    ]
    
    edition = models.CharField(max_length=50,choices=choix_edition,default='Physique')
    influence = models.CharField(max_length=50,choices=choix_influence,default='Comic-US')
    title = models.CharField(max_length=255)
    author = models.ForeignKey('gestion_utilisateur.Utilisateur', on_delete=models.CASCADE, related_name='works')  
    publication_date = models.DateField()
    cover_image = models.ImageField(upload_to='media/', blank=True, null=True)
    description = models.TextField()
    genres = models.CharField(max_length=50,choices=choix_genre,default='Comedie')
    planche1 = models.ImageField(upload_to='media/', blank=True, null=True)
    planche2 = models.ImageField(upload_to='media/', blank=True, null=True)
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

class Librairie(models.Model):
    nom = models.CharField(max_length=255)
    pays = models.CharField(max_length=100, choices=Utilisateur.PAYS_AFRICAINS)
    ville = models.CharField(max_length=150)
    enseigne = models.CharField(max_length=255, blank=True, null=True)
    photo = models.ImageField(upload_to="media/", blank=True, null=True)
    a_propos = models.TextField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    telephone = models.CharField(max_length=50, blank=True, null=True)
    adresse = models.CharField(max_length=255, blank=True, null=True)
    map_url = models.URLField(blank=True, null=True)
    heures_ouverture = models.TimeField(null=True)
    heure_fermeture = models.TimeField(null=True)
    latitude = models.DecimalField(
        max_digits=9, 
        decimal_places=6, 
        null=True, 
        blank=True,
        verbose_name="Latitude"
    )
    longitude = models.DecimalField(
        max_digits=9, 
        decimal_places=6, 
        null=True, 
        blank=True,
        verbose_name="Longitude"
    )
    

    site_web = models.URLField(blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    tiktok = models.URLField(blank=True, null=True)
    vedette = models.BooleanField(default=False)
    valide = models.BooleanField(default=False)

    def __str__(self):
        return self.nom
    
class Contact(models.Model):
    profil_choice = [
        ('Auteur/Dessinateur','Auteur/Dessinateur'),
        ('Journaliste','Journaliste'),
        ('Etudiant/Chercheur','Etudiant/Chercheur'),
        ('Grand-public','Grand-public')
    ]
    profile = models.CharField(max_length=50,choices=profil_choice,default='Journaliste')
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    societe= models.CharField(max_length=50)
    email = models.EmailField()
    objet = models.CharField(max_length=100)
    message = models.TextField()

    def __str__(self):
        return self.nom



    
    


# Model pour Editeur

from django.db import models
from django.utils.text import slugify
from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf import settings # Pour référencer le modèle Utilisateur personnalisé

# =========================================================================
# MODÈLE ÉDITEUR (Détails spécifiques au rôle)
# =========================================================================

class Editeur(models.Model):
    """
    Modèle représentant les informations détaillées d'une Maison d'Édition.
    Il est lié par OneToOne au compte Utilisateur ayant le rôle 'editeur'.
    """
    
    # RELATION À L'UTILISATEUR (Compte et authentification)
    # OnDelete=CASCADE signifie que si le compte utilisateur est supprimé, l'éditeur l'est aussi.
    utilisateur = models.OneToOneField(
        settings.AUTH_USER_MODEL, # Fait référence à votre classe Utilisateur(AbstractUser)
        on_delete=models.CASCADE,
        related_name='details_editeur',
        limit_choices_to={'role': 'editeur'}, # Limite la sélection aux utilisateurs ayant le rôle 'editeur'
        verbose_name="Compte Utilisateur de l'Éditeur"
    )
    
    # ------------------------------------
    # INFORMATIONS PRINCIPALES POUR L'AFFICHAGE PUBLIC
    # ------------------------------------
    nom = models.CharField(
        max_length=150, 
        unique=True, 
        verbose_name="Nom de la maison d'édition",
        help_text="Ex: Les Éditions Soleil Levant"
    )
    slug = models.SlugField(
        max_length=150, 
        unique=True, 
        blank=True,
        help_text="URL unique générée (ex: les-editions-soleil-levant)"
    )
    slogan = models.CharField(
        max_length=255, 
        blank=True, 
        null=True, 
        verbose_name="Slogan ou courte accroche"
    )
    description = models.TextField(
        blank=True, 
        null=True, 
        verbose_name="Histoire et vision détaillées"
    )

    # ------------------------------------
    # LOCALISATION ET HISTORIQUE
    # ------------------------------------
    # Le champ 'pays' est déjà géré par le modèle Utilisateur (Utilisateur.pays),
    # mais nous ajoutons l'adresse complète pour le siège.
    adresse_siege = models.CharField(
        max_length=255, 
        blank=True, 
        null=True, 
        verbose_name="Adresse du siège social"
    )
    annee_fondation = models.PositiveIntegerField(
        blank=True, 
        null=True, 
        verbose_name="Année de fondation",
        validators=[MinValueValidator(1500), MaxValueValidator(2100)],
    )

    # ------------------------------------
    # CONTACT & SOCIAUX
    # ------------------------------------
    email_contact = models.EmailField(
        max_length=100, 
        blank=True, 
        null=True,
        help_text="E-mail public de contact (si différent de l'e-mail du compte)"
    )
    site_web = models.URLField(
        max_length=200, 
        blank=True, 
        null=True, 
        verbose_name="Site Web"
    )
    facebook = models.URLField(
        max_length=200, 
        blank=True, 
        null=True
    )
    instagram = models.URLField(
        max_length=200, 
        blank=True, 
        null=True
    )
    siege = models.CharField(
        max_length=50,
        null=True
    )
    
    # ------------------------------------
    # MEDIA & CARTE
    # ------------------------------------
    logo = models.ImageField(
        upload_to='editeurs/logos/', 
        blank=True, 
        null=True, 
        verbose_name="Logo de l'éditeur"
    )
    latitude = models.DecimalField(
        max_digits=9, 
        decimal_places=6, 
        blank=True, 
        null=True,
        verbose_name="Latitude du siège"
    )
    longitude = models.DecimalField(
        max_digits=9, 
        decimal_places=6, 
        blank=True, 
        null=True,
        verbose_name="Longitude du siège"
    )
    nom_contact_1 = models.CharField(max_length=255, verbose_name="Nom/Prénom Contact Principal", null=True, blank=True)
    role_contact_1 = models.CharField(max_length=50, choices=[('Propriétaire','Propriétaire'), ('Employé','Employé')], null=True, blank=True)
    tel_contact_1 = models.CharField(max_length=50, null=True, blank=True)
    email_contact_1 = models.EmailField(null=True, blank=True)

    nom_contact_2 = models.CharField(max_length=255, verbose_name="Nom/Prénom Contact Secondaire", null=True, blank=True)
    role_contact_2 = models.CharField(max_length=50, choices=[('Propriétaire','Propriétaire'), ('Employé','Employé')], null=True, blank=True)
    tel_contact_2 = models.CharField(max_length=50, null=True, blank=True)
    email_contact_2 = models.EmailField(null=True, blank=True)

    class Meta:
        verbose_name = "Éditeur (Détail)"
        verbose_name_plural = "Éditeurs (Détails)"
        ordering = ['nom']

    def __str__(self):
        return self.nom

    def save(self, *args, **kwargs):
        """ Génère le slug à partir du nom avant l'enregistrement. """
        if not self.slug:
            self.slug = slugify(self.nom)
        super().save(*args, **kwargs)
        
    # Propriétés pour un accès facile
    @property
    def pays_siege(self):
        """ Accède au pays via le modèle Utilisateur lié """
        return self.utilisateur.get_pays_display()
    
    @property
    def ville_siege(self):
        """ Accède à la ville via le modèle Utilisateur lié """
        return self.utilisateur.ville_residence
    


class Auteur(models.Model):
    # Lien OneToOne vers l'Utilisateur
    utilisateur = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='details_auteur',
        limit_choices_to={'role': 'auteur'},
        verbose_name="Compte Utilisateur de l'Auteur"
    )
    
    # Ajoutez des champs spécifiques à l'auteur ici si nécessaire, sinon utilisez
    # les propriétés pour accéder à 'utilisateur'.
    
    class Meta:
        verbose_name = "Auteur (Détail)"
        verbose_name_plural = "Auteurs (Détails)"
        ordering = ['utilisateur__last_name', 'utilisateur__first_name']
        
    def __str__(self):
        return self.utilisateur.get_full_name() or self.utilisateur.username
        
    def get_absolute_url(self):
        # On pourrait utiliser le slug de l'utilisateur ou un champ généré si nécessaire
        return reverse('auteur_detail', kwargs={'pk': self.pk})

# ==============================================================================
# 3. Modèle Livre (Adapté à vos Editeur et Auteur/Utilisateur)
# ==============================================================================

class Genre(models.Model):
    nom = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    class Meta:
        verbose_name = "Genre"
        verbose_name_plural = "Genres"

    def __str__(self):
        return self.nom

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nom)
        super().save(*args, **kwargs)

class Bdtheque(models.Model):
    TITRES_CHOIX = [
        ('BD', 'Bande Dessinée'),
        ('Roman', 'Roman'),
        ('Nouvelle', 'Nouvelle'),
        ('Webtoon', 'Webtoon'),
        ('Essai', 'Essai'),
        ('Manga', 'Manga'),
    ]
    
    # Informations de base
    titre = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=200, blank=True)
    resumé = models.TextField(verbose_name="Résumé de l'œuvre")
    couverture = models.ImageField(upload_to='livres/couvertures/', blank=True, null=True)
    
    # Relations
    edition = models.ForeignKey(
        Editeur, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='livres_publies',
        verbose_name="Maison d'Édition enregistrée"
    )

    # 2. On ajoute ce champ pour le cas "Autre" (éditeur pas encore enregistré)
    autre_editeur_nom = models.CharField(
        max_length=255, 
        blank=True, 
        null=True, 
        verbose_name="Nom de l'éditeur (si non listé)"
    )

    # 3. Le champ de validation demandé par le client
    valide = models.BooleanField(
        default=False, 
        verbose_name="Est validé par l'admin"
    )
    # Clé étrangère vers l'Auteur (via le modèle Auteur que nous avons créé)
    auteur_principal = models.ForeignKey(Auteur, on_delete=models.SET_NULL, null=True, related_name='livres_principaux')
    auteurs_secondaires = models.ManyToManyField(Auteur, blank=True, related_name='livres_secondaires', verbose_name="Auteurs Additionnels")
    genres = models.ManyToManyField(Genre, blank=True, related_name='livres_associes')
    
    # Métadonnées
    type_oeuvre = models.CharField(max_length=50, choices=TITRES_CHOIX, default='BD', verbose_name="Type d'œuvre")
    date_publication = models.DateField(verbose_name="Date de publication")
    isbn = models.CharField(max_length=13, unique=True, blank=True, null=True, verbose_name="ISBN (13 chiffres)")
    
    class Meta:
        verbose_name = "Bdtheque"
        verbose_name_plural = "Bdtheque"
        ordering = ['-date_publication', 'titre']
        unique_together = ('edition', 'titre')

    def __str__(self):
        return f"{self.titre} ({self.edition.nom})"
        
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titre)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('livre_detail', kwargs={'slug': self.slug})
    


