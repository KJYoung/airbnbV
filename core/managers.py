from django.db import models
from django.contrib.auth import models as UserModel


class CustomModelManager(models.Manager):
    def get_or_none(self, *args, **kwargs):
        try:
            return self.get(*args, **kwargs)
        except self.model.DoesNotExist:
            return None


class CustomUserManager(CustomModelManager, UserModel.UserManager):
    pass
