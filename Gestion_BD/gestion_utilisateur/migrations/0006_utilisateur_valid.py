# Generated by Django 5.1.6 on 2025-03-02 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_utilisateur', '0005_utilisateur_annee_experience_utilisateur_genres_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='utilisateur',
            name='valid',
            field=models.BooleanField(default=False),
        ),
    ]
