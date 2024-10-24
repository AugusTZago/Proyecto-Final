from typing import Any, Dict
from django import http
from django.contrib.auth.forms import AuthenticationForm
from django.forms.models import BaseModelForm
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.http.response import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.utils.http import url_has_allowed_host_and_scheme

from apps.usuario.forms import UserCreationForm, UserEditionForm
from apps.usuario.models import Usuario
from apps.comentario.models import Comentario
from apps.posteo.models import Post

# Create your views here.
class registrarUsuario(CreateView):
    
    template_name = 'registro/register.html'
    form_class = UserCreationForm
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        ctx = super().get_context_data(**kwargs)
        ctx['next'] = self.request.GET.get('next', '')
        return ctx
    
    def form_valid(self, form):
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.password = make_password(form.cleaned_data["password"])
            usuario.save()
            usuario = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password'],
                                    )
            login(self.request, usuario)
            return super().form_valid(form) 
        else:
            self.form_invalid(form)

    def get_success_url(self) -> str:
        redirect_to = self.request.POST.get('next', '')
        messages.warning(self.request, redirect_to)
        url_is_safe = url_has_allowed_host_and_scheme(redirect_to, '*')
        if redirect_to and url_is_safe:
            messages.success(self.request, "¡Usuario creado correctamente!")
            return redirect_to



class LoginUsuario(UserPassesTestMixin,LoginView):
    template_name = 'registro/login.html'

    def test_func(self):
        if self.request.user.is_authenticated:
            return False
        else:
            return True
        
    def handle_no_permission(self):
        return redirect(reverse_lazy('index'))
    
    def form_valid(self, form):
        if form.is_valid():
            return super().form_valid(form)
        else:
            self.form_invalid(form)
    
    def form_invalid(self, form: AuthenticationForm):
        messages.warning(self.request, "¡Usuario o contraseña incorrectos, intente nuevamente!")
        return super().form_invalid(form)

    def get_success_url(self):
        redirect_to = self.request.POST.get('next', '')
        # if not redirect_to or not url_has_allowed_host_and_scheme(redirect_to, '*'):
        #     redirect_to = reverse_lazy('index')
        # return redirect_to
        url_is_safe = url_has_allowed_host_and_scheme(redirect_to, '*')
        if redirect_to != None and url_is_safe:
            messages.success(self.request, "¡Usuario logueado correctamente!")
            return redirect_to

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        next = self.request.GET.get('next','')
        context['next'] = next
        return context
  
  
  
class LogoutUsuario(LoginRequiredMixin, LogoutView):
    template_name = 'registro/logout.html'

    def handle_no_permission(self):
        return redirect(reverse_lazy('usuario:login'))
    
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any):
        messages.success(self.request, "¡Sesion cerrada correctamente!")
        return super().get(request, *args, **kwargs)



class UpdateUsuarioView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    
    template_name = "usuario/editar-perfil.html"
    model = Usuario
    form_class = UserEditionForm
    
    def test_func(self):
        if (self.request.user.is_miembro or self.request.user.is_superuser or self.request.user == self.get_object()):
            return True
        else:
            return False    
    
    def get_success_url(self) -> str:
        redirect_to = self.request.POST.get('next', '')
        url_is_safe = url_has_allowed_host_and_scheme(redirect_to, '*')
        if redirect_to != None and url_is_safe:
            messages.success(self.request, "¡Usuario actualizado correctamente!")
            return redirect_to
        
    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['usuario'] = self.get_object(self.queryset)
        next = self.request.GET.get('next','')
        context['next'] = next
        return context
    
    def form_valid(self, form):
        if form.is_valid():
            messages.success(self.request, "¡Usuario actualizado correctamente!")
            return super().form_valid(form)
        else:
            self.form_invalid(form)
      



class VerPerfilUsuario(DetailView):
    model = Usuario
    template_name = 'usuario/perfil.html'
    context_object_name = 'usuario'
    
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        posteos = Post.objects.filter(creado_por=kwargs['object'])
        comentarios = Comentario.objects.filter(creado_por=kwargs['object'])
        cant_comentarios = comentarios.count()
        cant_articulos = posteos.count()
        if cant_comentarios == 0:
            titulo_comentarios = 'Sin comentarios'
        elif cant_comentarios == 1:
            titulo_comentarios = 'Comentario'
        else:
            titulo_comentarios = str(cant_comentarios) + ' ' + 'Comentarios'
        if cant_articulos == 0:
            titulo_posteos = 'Sin posteos'
        elif cant_articulos == 1:
            titulo_posteos = 'Posteo'
        else:
            titulo_posteos = str(cant_comentarios) + ' ' + 'Posteos'
        ctx['titulo_posteos'] = titulo_posteos
        ctx['titulo_comentarios'] = titulo_comentarios
        ctx['comentarios'] = comentarios
        ctx['posteos'] = posteos
        return ctx