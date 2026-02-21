from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify

from gestion_utilisateur.models import Utilisateur
from .models import Work, Bdtheque, Auteur, Genre

@receiver(post_save, sender=Work)
def sync_work_to_bdtheque(sender, instance, created, **kwargs):
    # 1. Récupérer ou créer l'Auteur lié à l'Utilisateur
    # On utilise 'utilisateur' car c'est le nom du champ dans ton modèle Auteur
    auteur_obj, created_auteur = Auteur.objects.get_or_create(utilisateur=instance.author)
    
    # 2. Synchronisation de l'entrée Bdtheque
    # On utilise update_or_create pour mettre à jour si le titre existe déjà pour cet auteur
    bd_item, created_bd = Bdtheque.objects.update_or_create(
        titre=instance.title,
        auteur_principal=auteur_obj,
        defaults={
            'resumé': instance.description,
            'couverture': instance.cover_image,
            'date_publication': instance.publication_date,
            'valide': instance.valid,
            'type_oeuvre': 'BD', # Valeur par défaut
        }
    )

    # 3. Gestion du Genre (Conversion CharField -> ManyToMany)
    if instance.genres:
        # On récupère ou crée le modèle Genre basé sur le texte du choix dans Work
        genre_obj, _ = Genre.objects.get_or_create(nom=instance.genres)
        bd_item.genres.add(genre_obj)

    # 4. Forcer la génération du slug si c'est une création
    if not bd_item.slug:
        bd_item.slug = slugify(instance.title)
        # On vérifie l'unicité du slug
        unique_slug = bd_item.slug
        num = 1
        while Bdtheque.objects.filter(slug=unique_slug).exclude(id=bd_item.id).exists():
            unique_slug = f'{bd_item.slug}-{num}'
            num += 1
        bd_item.slug = unique_slug
        bd_item.save()


@receiver(post_save, sender=Utilisateur)
def sync_utilisateur_to_auteur(sender, instance, created, **kwargs):
    """
    Crée ou met à jour un profil Auteur si l'utilisateur a le rôle 'auteur'
    et que son compte est validé.
    """
    if instance.role == 'auteur' and instance.valid:
        # On utilise update_or_create pour être sûr de ne pas avoir de doublons
        # et mettre à jour si nécessaire.
        Auteur.objects.get_or_create(
            utilisateur=instance,
            defaults={} # Tu peux ajouter des champs par défaut ici si ton modèle Auteur évolue
        )
    elif instance.role == 'auteur' and not instance.valid:
        # Optionnel : si l'admin invalide l'utilisateur, 
        # on peut décider de supprimer le profil auteur ou simplement le laisser.
        pass