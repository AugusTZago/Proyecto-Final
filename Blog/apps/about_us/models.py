from django.db import models

# Create your models here.
class Nosotros(models.Model):
    nombre = models.CharField(max_length=50)
    edad = models.IntegerField(max_length=2)
    