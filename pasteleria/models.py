from django.db import models
from django.contrib.auth.models import AbstractUser, User


# Create your models here.
class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.IntegerField()
    stock = models.IntegerField(default=0)

    def __str__(self):
        return self.nombre


class UserProfile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    ADMIN = 'admin'
    CLIENT = 'cliente'
    ROLE_CHOICES = [
        (ADMIN, 'Admin'),
        (CLIENT, 'Cliente'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=CLIENT)

    class Meta:
        db_table = 'custom_user'
