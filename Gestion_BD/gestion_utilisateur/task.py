# # gestion_utilisateur/tasks.py

# from celery import shared_task
# from django.core.mail import send_mail
# from django.utils import timezone
# from datetime import timedelta
# from .models import Utilisateur
# from Gestion_BD.settings import EMAIL_HOST_USER
# from django.core.mail import EmailMessage

# @shared_task
# def send_approval_email(user_id):
#     user = Utilisateur.objects.get(id=user_id)
    
#     # Envoi de l'email initial pour dire que la demande est en attente
#     # send_mail(
#     #     'Nous avons reçu votre inscription',
#     #     'Merci pour votre inscription en tant qu\'auteur. Dans 48 heures, nous vous enverrons un email pour vous informer si vous êtes approuvé.',
#     #     EMAIL_HOST_USER,  # Email de l'expéditeur
#     #     [user.email],
#     #     fail_silently=False,
#     # )
#     suject ="Nous avons reçu votre inscription"
#     message = "Merci pour votre inscription en tant qu'auteur. Dans 48 heures, nous vous enverrons un email pour vous informer si vous êtes approuvé."
#     from_email = EMAIL_HOST_USER
#     to_email = [user.email]
#     email = EmailMessage(suject, message, from_email, to_email)
#     email.send()
    
#     # Envoi de l'email après 3 jours
#     approval_time = timezone.now() + timedelta(days=3)
    
#     # Cette tâche peut être planifiée dans Celery pour exécution après 3 jours
#     send_approval_status(user, approval_time)

# @shared_task
# def send_approval_status(user, approval_time):
#     # Vérifier si l'auteur a été validé dans 3 jours
#     if user.valid_auteur:
#         send_mail(
#             'Félicitations, vous êtes approuvé !',
#             'Félicitations, votre demande en tant qu\'auteur a été approuvée.',
#             EMAIL_HOST_USER,  # Email de l'expéditeur
#             [user.email],
#             fail_silently=False,
#         )
#     else:
#         send_mail(
#             'Désolé, votre demande a été rejetée.',
#             'Nous regrettons de vous informer que votre demande en tant qu\'auteur n\'a pas été approuvée.',
#             EMAIL_HOST_USER,  # Email de l'expéditeur
#             [user.email],
#             fail_silently=False,
#         )
