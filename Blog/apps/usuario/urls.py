from django.urls import  path
from django.contrib.auth.decorators import permission_required
from apps.usuario.views import LoginUsuario, LogoutUsuario, UpdateUsuarioView, registrarUsuario, VerPerfilUsuario


app_name = 'usuario'

urlpatterns = [
    path('usuario/registro/', registrarUsuario.as_view(), name = 'registro'),
    path('usuario/login/', LoginUsuario.as_view(), name='login'),
    path('usuario/logout/', LogoutUsuario.as_view(), name='logout'),
    path('usuario/<int:pk>/actualizar/', UpdateUsuarioView.as_view(), name="actualizar"),
    path('usuario/<int:pk>/ver_perfil/', VerPerfilUsuario.as_view(), name="perfil"),
    
]