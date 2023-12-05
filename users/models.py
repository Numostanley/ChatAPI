import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    email = models.EmailField(unique=True)

    REQUIRED_FIELDS = ["email"]

    class Meta:
        ordering = ("-date_joined",)

    def __str__(self):
        return self.username
