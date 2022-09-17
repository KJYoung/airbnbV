from django.db import models
from . import managers

# Create your models here.
class AbstractTimeStampedModel(models.Model):
    """Time Stamped Core Model"""

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = managers.CustomModelManager()

    class Meta:
        abstract = True
