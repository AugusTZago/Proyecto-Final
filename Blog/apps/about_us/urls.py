from django.contrib import admin
from django.urls import path, include
from apps.about_us.views import *
from Blog import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', index, name='index'),
    path('', index, name='home'),
    path('blog/', blog, name='blog'),
    path('contact/', contacto, name='contact'),
    path('acerca-de/', acerca_de, name='about')
]