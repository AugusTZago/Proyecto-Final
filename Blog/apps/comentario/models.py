from typing import Iterable
from django.db import models
from django.utils import timezone

from apps.posteo.models import Post
from apps.usuario.models import Usuario

# Create your models here.

class Comentario(models.Model):
    autor = models.ForeignKey(Usuario,null=True, blank=True, verbose_name='Creador', on_delete=models.CASCADE)
    contenido = models.CharField(max_length=200, verbose_name='Texto', help_text='Ingrese su comentario', default='')
    comentario_padre = models.ForeignKey('self', on_delete=models.CASCADE, verbose_name="Comentario", null=True, blank=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank= True, verbose_name='Post')
    creado = models.DateTimeField(default=timezone.now, null=False)
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.contenido
    
    def save(self, *args, **kwargs):
        self.creado = timezone.now
        return super().save(*args, **kwargs)