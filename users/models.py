from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100, unique=True)

    # USERNAME_FIELD = "email"
    # REQUIRED_FIELDS = ["username"]
