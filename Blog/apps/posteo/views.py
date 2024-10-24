from typing import Any
from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import UpdateView, DeleteView
from django.views.generic import CreateView, ListView
from django.contrib import messages
from django.db.models import Q
from django.urls import reverse_lazy


from apps.posteo.forms import PostCreationForm, CategoriaForm
from apps.comentario.models import Comentario
from apps.comentario.forms import ComentarioCreationForm

from .models import Post, Categoria




# Create your views here.
class PostView(View):
    def get(self, request, id):
        post = Post.objects.filter(is_active = True).get(id = id)
        posts = Post.objects.filter(is_active = True).order_by('-creado', '-id')[:5]
        comentarios = Comentario.objects.filter(is_active=True, post = post)
        categorias = Categoria.objects.all()
        cant_coment = comentarios.count()
        context = {'posts_banner' : posts,
                   'post': post,
                   'cent_coment' : cant_coment,
                   'comentarios' : comentarios,
                   'categorias' : categorias,
                   'form' : form
                   
                   }
        form = ComentarioCreationForm()
        return render(request, 'post/post-details.html', context)
    
class EditarPost(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class=PostCreationForm
    template_name = 'posteos/mod-post.html'
    success_url = reverse_lazy('post:posteos')
    
    def test_func(self):
        return self.request.user.is_miembro or self.request.user.is_superuser        
    
    def post(self, request, *args, **kwargs):
        messages.success(request, 'Post actualizado correctamente')
        return super().post(request, *args, **kwargs)
    
class CrearPost(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    form_class = PostCreationForm
    template_name = 'posteos/crear-post.html'
    
    def test_func(self):
        return self.request.user.is_miembro or self.request.user.is_superuser
        
    def form_valid(self, form):
        if form.is_valid:
            form.instance.autor = self.request.user
            messages.success(self.request, "Post creado exitosamente")
            return super().form_valid(form)
        else:
            messages.error(self.request, "Error en la validacion")
            return render(self.request, 'posteo/crear-post.html', {'form': form})
        
class PostListView(ListView):
    model = Post
    template_name= 'posteos/todos-post.html'
    cantidad_registros = 0

    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['categorias'] = Categoria.objects.all()
        context['registros'] = self.cantidad_registros
        return context
    
    def get_queryset(self):
        posts = Post.objects.filter(is_active=True).order_by('-creado')
        self.cantidad_registros = posts.count()
        return posts
    
class PostBusquedaView(ListView):
    model = Post
    template_name= 'posteos/todos-post.html'
    registros = 0
    ordering = '-creado'

    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['categorias'] = Categoria.objects.all()
        context['registros'] = self.cantidad_registros
        context['filter'] = self.request.GET.get('filter', '')
        context['orderby'] = self.request.GET.get('orderby', '-creado')
        return context
    
    def get_queryset(self):
        filter_val = self.request.GET.get('filter', '')
        order = self.request.GET.get('orderby')
        if not order:
            order = '-creado'
        if not filter_val:
            filter_val = ''
        new_context = Post.objects \
            .filter( \
            Q(titulo__icontains=filter_val) | Q(contenido__icontains=filter_val)) \
            .order_by(order)
        self.registros = new_context.count()
        
        return new_context
    
class BorrarPostView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    def test_func(self):
        if (self.request.user.is_miembro or self.request.user.is_superuser):
            return True
        else:
            return False
    
    model = Post
    template_name = 'posteos/borrar-post.html'
    success_url = reverse_lazy('posteos:post-details')
    
    def get_success_url(self):
        messages.success(self.request, "Post eliminado exitosamente")
        return super().get_success_url()

class CrearCategoria(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    form_class = CategoriaForm
    template_name = 'posteos/crear-categoria.html'

    def test_func(self):
        if (self.request.user.is_miembro or self.request.user.is_superuser):
            return True
        else:
            return False
     
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['next'] = self.request.GET.get('next')
        return context    
    
    def form_valid(self, form):
        if form.is_valid:
            messages.success(self.request, "Categoria agregada exitosamente")
            self.success_url = self.request.POST.get('next') 
            return super().form_valid(form)
        else:
            messages.error(self.request, "Error en la validacion")
            return render(self.request, 'posteos/crear-categoria.html', {'form': form}) 

class BorrarCategoriaView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    
    def test_func(self):
        if (self.request.user.is_miembro or self.request.user.is_superuser):
            return True
        else:
            return False
    
    model = Categoria
    template_name = 'posteos/borrar-categoria.html'
    
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['next'] = self.request.GET.get('next')
        return ctx
    
    def post(self, request: HttpRequest, *args, **kwargs):
        self.success_url = request.POST.get('next')
        return super().post(request, *args, **kwargs)
    
    def get_success_url(self):
        messages.success(self.request, "Categoria borrada exitosamente")
        return super().get_success_url()

class CategoriaListView(ListView):
    model = Post
    paginate_by = 4
    template_name = 'posteos/todos-post.html'
    cantidad_registros = 0
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['registros'] = self.cantidad_registros
        context['categorias'] = Categoria.objects.all()
        context['categoria'] = Categoria.objects.get(id=self.kwargs['pk'])
        return context

    def get_queryset(self):
        posteos = Post.objects.filter(is_active=True, categoria=Categoria.objects.get(id=self.kwargs['pk'])).order_by('-creado')
        self.cantidad_registros = posteos.count()
        return posteos