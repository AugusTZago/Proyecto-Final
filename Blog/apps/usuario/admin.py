from django.contrib import admin

# Register your models here.
from apps.usuario.models import Usuario

admin.site.register(Usuario)