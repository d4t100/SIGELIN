from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Equipos
from .qr import generar_qr_para_equipo

@receiver(post_save, sender=Equipos)
def crear_qr_al_guardar(sender, instance, created, **kwargs):
    if created:
        generar_qr_para_equipo(instance)
