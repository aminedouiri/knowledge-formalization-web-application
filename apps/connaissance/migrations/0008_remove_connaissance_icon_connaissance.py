# Generated by Django 4.0.6 on 2022-09-12 22:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('connaissance', '0007_alter_connaissance_forme_connaissance_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='connaissance',
            name='icon_connaissance',
        ),
    ]