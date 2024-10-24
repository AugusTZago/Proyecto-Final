from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import CreateView, ListView, DetailView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages

from apps.contacto.forms import ContactoForm
from apps.contacto.models import Contacto
# Create your views here.
class ContactoUsuario(CreateView):
    model = Contacto
    from_class = ContactoForm
    success_url = reverse_lazy('index')
    template_name = 'contacto/contacto.html'
    def form_valid(self, form):
        messages.success(self.request, 'Mensaje enviado correctamente')
        return super().form_valid(form)
    
class ListarContactosView(UserPassesTestMixin, LoginRequiredMixin, ListView):
    model = Contacto
    template_name = 'contacto/lista-contacto.html'
    context_object_name = 'contactos'

    def test_func(self):
        if (self.request.user.is_miembro or self.request.user.is_superuser):
            return True
        else:
            return False
        
    def get_queryset(self):
        return Contacto.objects.all()
        
class DetalleContactoView(UserPassesTestMixin, LoginRequiredMixin, DetailView):
    model = Contacto
    template_name = 'contacto/detalle-contacto.html'
    context_object_name = 'contacto'

    def test_func(self):
        if (self.request.user.is_miembro or self.request.user.is_superuser):
            return True
        else:
            return False
        
class BorrarContactoView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    model = Contacto
    template_name = 'contacto/borrar-contacto.html'
    success_url = reverse_lazy('contacto:verContactos')

    def test_func(self):
        if (self.request.user.is_miembro or self.request.user.is_superuser):
            return True
        else:
            return False


    def get_success_url(self):
        messages.success(self.request, "contacto borrado exitosamente")
        return super().get_success_url()

