# Generated by Django 4.0.6 on 2022-07-13 01:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('connaissance', '0003_alter_connaissance_date_creation'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='connaissance',
            options={'ordering': ['-date_creation']},
        ),
    ]
