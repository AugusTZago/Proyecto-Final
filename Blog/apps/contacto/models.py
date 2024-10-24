from django.db import models
from django.utils import timezone
# Create your models here.

class Contacto(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    asunto = models.CharField(max_length=50)
    mensaje = models.TextField()
    fecha = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return self.nombre