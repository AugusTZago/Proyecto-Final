from django.contrib import admin
from django.urls import path, include
from apps.about_us.views import *
from Blog import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('index.html', index, name='index'),
    path('', index, name='home'),
    path('blog.html', blog, name='blog'),
    path('contact.html', contacto, name='contact'),
    path('about.html', acerca_de, name='about')
]