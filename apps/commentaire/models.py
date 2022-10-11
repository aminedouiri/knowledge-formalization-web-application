from django.db import models
from django.contrib.auth.models import User
from apps.connaissance.models import Connaissance
from datetime import datetime

# Create your models here.

class Commentaire(models.Model):
    created_at = models.DateTimeField(default = datetime.now, blank="True")
    created_for = models.CharField(max_length=255)
    contenu =models.CharField(max_length=255)
    created_by = models.CharField(max_length=255, default="null")

    class Meta:
        ordering = ['-created_at']

