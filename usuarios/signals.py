from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import User
from rolepermissions.roles import assign_role


@receiver(post_save, sender=User)
def permissoes(sender, instance, created, **kwargs):
    if created:
        if instance.tipo == 'vendedor':
            assign_role(instance, 'vendedor')
        elif instance.tipo == 'comprador':
            assign_role(instance, 'comprador')
        