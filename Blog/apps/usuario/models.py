from django.db import models
from django.contrib.auth.models import Group, User, Permission
from django.contrib.auth.models import AbstractUser
from django.urls import reverse_lazy
from django.utils import timezone

# Create your models here.
class Usuario(AbstractUser):
    is_miembro = models.BooleanField(default=False)
    foto_perfil = models.ImageField(
        default="../static/default.png", 
        upload_to="usuario",
        )
    nacimiento = models.DateField(
        null=True,
        blank=True
    )
    groups = models.ManyToManyField(
        Group,
        related_name='usuario_groups',
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='usuario_permissions',
        blank=True,
    )
    
   
    def get_link_verperfil(self):
        return reverse_lazy('usuario:perfil', args=[ self.pk ])
    
    def get_edad(self):
        return int((timezone.now - self.nacimiento).days / 365.25)
    
    def __str__(self):
        return self.username