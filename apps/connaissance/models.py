from datetime import datetime
from xml.etree.ElementInclude import default_loader
from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
import re

# Create your models here.

class Connaissance(models.Model):
    choices = [
        ('tableau','tableau'),
        ('document','document'),
        ('image','image'),
    ]
    nom_connaissance = models.CharField(max_length=128)
    forme_connaissance = models.CharField(max_length=10, choices=choices)
    date_creation = models.DateTimeField(blank=True, null=True, default=datetime.now)
    status_vue = models.BooleanField(default=False, null=True)
    url_connaissance = models.CharField(max_length=128, default=True)

    def __str__(self):
        return self.nom_connaissance

    class Meta:
        ordering = ['-date_creation']

        

