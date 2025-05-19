# users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    profile_image = models.URLField(blank=True, null=True)
    language = models.CharField(max_length=10, choices=[("ko", "Korean"), ("en", "English")], default="ko")
    registered_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email