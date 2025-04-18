# Generated by Django 5.1.6 on 2025-02-10 17:55

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_content', '0001_initial'),
        ('gestion_utilisateur', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Auteur',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pays', models.CharField(blank=True, max_length=100, null=True)),
                ('social_links', models.JSONField(blank=True, default=dict)),
                ('genres', models.ManyToManyField(blank=True, to='gestion_content.genre')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='auteur', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BlogPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='blog_posts', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
