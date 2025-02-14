# Generated by Django 5.1.6 on 2025-02-13 05:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_utilisateur', '0002_auteur_blogpost'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='utilisateur',
            name='social_links',
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='blog_posts', to='gestion_utilisateur.auteur'),
        ),
    ]
