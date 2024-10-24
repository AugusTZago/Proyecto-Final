from django.urls import path
from .views import PostBusquedaView, PostCreationForm, BorrarPostView, CrearCategoria, BorrarCategoriaView, PostListView, CrearPost, EditarPost, CategoriaListView
from apps.comentario.views import publicarComentario, publicarRespuestaComentario

app_name = 'post'

urlpatterns = [
    path('posteos/', PostListView.as_view(), name='posteos'),
    path('post/<int:id>/', PostListView.as_view(), name='mostrarPost'),
    path('post/crear/', CrearPost.as_view(), name='crear'),
    path('post/<int:pk>/editar/', EditarPost.as_view(), name='editar'),
    path('post/<int:pk>/borrar/', BorrarPostView.as_view(), name=('borrar')),
    path('post/<int:id>/comentar/', publicarComentario, name='comentar'),
    path('post/<int:id>/responder/', publicarRespuestaComentario, name='responder'),
    path('categoria/<int:pk>/', CategoriaListView.as_view(), name='categoria'),
    path('post/buscar/', PostBusquedaView.as_view(), name='buscar'),
    path('categoria/crear/', CrearCategoria.as_view(), name='crearCategoria'),
    path('categoria/<int:pk>/borrar/', BorrarCategoriaView.as_view(), name='borrarCategoria'),
]