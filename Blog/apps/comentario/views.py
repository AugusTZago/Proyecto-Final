from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import UpdateView, DeleteView

from apps.comentario.forms import ComentarioCreationForm
from apps.comentario.models import Comentario
from apps.posteo.models import Post

# Create your views here.
def publicarComentario(request, id):
    if request.method == "POST":
        form = ComentarioCreationForm(data = request.POST)
        form.instance.autor = request.user
        post = Post.objects.get(id=id)
        form.instance.post = post
        if form.is_valid():
            form.save()
        else:
            return redirect('posteo:post-detail', id)
    return redirect('posteo:post-detail', id)

def publicarRespuestaComentario(request, id):
    if request.method == "POST": 
        comentario_id = request.POST.get('comentario')
        comentario = Comentario.objects.get(id=comentario_id)
        contenido = request.POST.get('contenido')
        usuario = request.user
        nuevo_comentario = Comentario()
        nuevo_comentario.comentario = comentario
        nuevo_comentario.autor = usuario
        nuevo_comentario.contenido = contenido
        nuevo_comentario.save()
    return redirect('posteo:post-detail', id)

class borrarComentario(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comentario
    template_name = 'comentario/borrar-comentario.html'
    success_url = ''

    def test_func(self):
        if (self.request.user.is_miembro or self.request.user.is_superuser):
            return True
        else:
            return False
        
    def get_success_url(self) -> str:
        self.success_url = self.request.GET.get('next')
        messages.success(self.request, "Comentario borrado exitosamente")
        return super().get_success_url()
    
class EditarComentario(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comentario
    form_class = ComentarioCreationForm
    template_name = 'comentario/editar-comentario.html'
    success_url = ''
    
    def test_func(self):
        if (self.request.user.is_miembro or self.request.user.is_superuser):
            return True
        else:
            return False    

    def post(self, request, *args, **kwargs):
        self.success_url = request.GET.get('next')
        messages.success(request, "Post actualizado correctamente")
        return super().post(request, *args, **kwargs)