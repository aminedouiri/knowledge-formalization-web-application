# Generated by Django 4.0.6 on 2022-09-07 18:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0003_userprofile_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='email',
        ),
    ]
