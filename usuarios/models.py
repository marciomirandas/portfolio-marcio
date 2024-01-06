from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    SELECIONAR_TIPO = (
        ('vendedor', 'Vendedor'),
        ('comprador', 'Comprador'),
    )
    tipo = models.CharField('Tipo', max_length=12, choices=SELECIONAR_TIPO)