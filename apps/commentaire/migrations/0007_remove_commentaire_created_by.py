# Generated by Django 4.0.6 on 2022-07-11 22:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('commentaire', '0006_alter_commentaire_created_by'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='commentaire',
            name='created_by',
        ),
    ]
