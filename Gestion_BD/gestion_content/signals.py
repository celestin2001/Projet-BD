from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from django.utils.text import slugify

# Remplace 'ton_app' par le nom réel de tes dossiers d'applications
from gestion_utilisateur.models import Utilisateur
from .models import Work, Bdtheque, Auteur, Genre, Editeur

@receiver(post_save, sender=Work)
def sync_work_to_bdtheque(sender, instance, created, **kwargs):
    """
    Synchronise automatiquement un Work vers la Bdtheque dès qu'il est sauvegardé.
    Gère l'auteur, l'éditeur (enregistré ou manuel), les genres et le slug.
    """
    
    # 1. Récupération ou création de l'objet Auteur lié à l'utilisateur
    # Note : On part du principe que l'auteur est l'instance.author (ForeignKey vers Utilisateur)
    auteur_obj, _ = Auteur.objects.get_or_create(utilisateur=instance.author)
    
    # 2. Synchronisation (Création ou Mise à jour)
    # On utilise update_or_create pour ne pas avoir de doublons si on modifie le Work
    bd_item, created_bd = Bdtheque.objects.update_or_create(
        titre=instance.title,
        auteur_principal=auteur_obj,
        defaults={
            'resumé': instance.description,
            'couverture': instance.cover_image,
            'date_publication': instance.publication_date,
            'valide': instance.valid,
            'type_oeuvre': 'BD', # Tu peux changer cela si Work a un champ type
            
            # Liaison avec la Maison d'Édition (Objet Editeur)
            'edition': instance.editeur, 
            
            # Sauvegarde du nom manuel si l'éditeur n'est pas sur le site
            'autre_editeur_nom': instance.other_editor_name or '',
        }
    )

    # 3. Gestion du Genre (Conversion du choix CharField vers ManyToMany)
    if instance.genres:
        # On crée l'objet Genre en base s'il n'existe pas encore
        genre_obj, _ = Genre.objects.get_or_create(nom=instance.genres)
        bd_item.genres.add(genre_obj)

    # 4. Génération d'un Slug unique
    # On ne génère le slug que si c'est une création ou si le slug est vide
    if not bd_item.slug:
        base_slug = slugify(instance.title)
        unique_slug = base_slug
        num = 1
        # On vérifie dans la base Bdtheque si le slug existe déjà
        while Bdtheque.objects.filter(slug=unique_slug).exclude(id=bd_item.id).exists():
            unique_slug = f'{base_slug}-{num}'
            num += 1
        bd_item.slug = unique_slug
        # On sauvegarde une dernière fois pour le slug
        bd_item.save()

@receiver(post_delete, sender=Work)
def delete_work_from_bdtheque(sender, instance, **kwargs):
    """
    Supprime automatiquement l'entrée dans la Bdtheque 
    si le Work original est supprimé.
    """
    # On cherche la BD qui a le même titre et le même auteur
    # On utilise .delete() pour la supprimer proprement
    Bdtheque.objects.filter(
        titre=instance.title, 
        auteur_principal__utilisateur=instance.author
    ).delete()

@receiver(post_save, sender=Utilisateur)
def sync_utilisateur_to_auteur(sender, instance, created, **kwargs):
    # SI l'utilisateur a le rôle 'auteur' ET qu'il est coché 'valid' par l'admin
    if instance.is_auteur and instance.valid:
        # On crée son profil Auteur (get_or_create évite de créer des doublons)
        Auteur.objects.get_or_create(utilisateur=instance)
        print(f"Profil Auteur créé/vérifié pour {instance.username}")
    
    # SINON (s'il n'est plus auteur ou plus valide)
    else:
        # On cherche s'il a une fiche Auteur et on la supprime
        Auteur.objects.filter(utilisateur=instance).delete()
        print(f"Profil Auteur supprimé pour {instance.username}")