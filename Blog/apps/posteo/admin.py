from django.contrib import admin

# Register your models here.
from apps.posteo.models import Post, Categoria

admin.site.register(Post)
admin.site.register(Categoria)