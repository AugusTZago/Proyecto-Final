from typing import Iterable
from django.db import models
from django.urls import reverse_lazy
from django.utils import timezone
from django.db.models import Count

from apps.usuario.models import Usuario

# Create your models here.

# POST
class Post(models.Model):
    titulo = models.CharField(max_length=40, null=False)
    subtitulo = models.CharField(max_length=40, null=False)
    creado = models.DateTimeField(default=timezone.now)
    modificado = models.DateTimeField(default=None, null=True)
    contenido = models.TextField()
    image = models.ImageField(upload_to='post/', default='../static/post/default.png')
    autor = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='creador')

    class Meta:
        ordering = ('-creado',)

    def save(self, *args, **kwargs):
        if self.id:
            self.modificado = timezone.now()
        else:
            self.creado = timezone.now()
        super(Post, self).save(*args, **kwargs)

    def get_absolute_url(self):
        from django.urls import reverse
        # agregar la direccion del post
        return reverse('post:post-details', kwargs={'id': self.pk})

    def get_posts_recientes():
        ultimos_cinco = Post.objects.order_by('-creado', '-id')[:5]
        return ultimos_cinco

    def get_posts_mas_comentados():
        mas_comentados = Post.objects.all() \
            .annotate(num_comentarios = Count('comentario')) \
            .order_by('-num_comentarios')[:5]
        return mas_comentados
    
    def get_comentario_url(self):
        return reverse_lazy('post:comentario', args=[self.pk])
    
    def get_respon_url(self):
        return reverse_lazy('post:respon', args=[self.pk])
    
    def get_url_completo(self):
        return reverse_lazy('post:post-details', args=[self.pk])
    
    def __str__(self) -> str:
        return str(self.titulo + ' ' + self.creado.strftime("%d-%m-%Y"))


# CATEGORIA
class Categoria(models.Model):
    nombre = models.CharField(max_length=40, help_text='Nombre de la categoría')
    is_active = models.BooleanField(default=True, verbose_name='activo')

    def __str__(self):
        return str(self.nombre)
