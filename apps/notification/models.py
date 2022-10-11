from django.db import models
from apps.connaissance.models import Connaissance
from datetime import datetime

# Create your models here.

class Notification(models.Model):
    pass
    '''
    created_at = models.DateTimeField(blank=True, null=True, default=datetime.now)
    contenu_notification = models.CharField(max_length=128)
    type_notification = [
        ('connaissance','connaissance'),
        ('commentaire','commentaire'),
    ]
    type_notification = models.CharField(max_length=128, choices = type_notification)
    '''





    

    