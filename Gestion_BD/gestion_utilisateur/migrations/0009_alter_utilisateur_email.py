# Generated by Django 5.1.6 on 2025-03-05 23:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_utilisateur', '0008_alter_utilisateur_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='utilisateur',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]
