from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class User(AbstractUser):
    phone = models.CharField(max_length=10, unique=True)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.username