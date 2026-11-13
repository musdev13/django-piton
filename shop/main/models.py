from django.db import models


class User(models.Model):
    username = models.CharField(max_length=150, unique=True)
    last_name = models.CharField(max_length=150, blank=True)
    first_name = models.CharField(max_length=150, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    password_hash = models.CharField(max_length=128)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    refresh_token = models.CharField(max_length=255, null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name} <{self.email}>'
