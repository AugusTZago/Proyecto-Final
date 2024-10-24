from django.urls import path
from .views import BorrarContactoView, ContactoUsuario, DetalleContactoView, ListarContactosView

app_name = 'contacto'

urlpatterns = [
    path('contacto/', ContactoUsuario.as_view(), name='contacto'),
    path('contacto/ver/', ListarContactosView.as_view(), name='verContactos'),
    path('contacto/<int:pk>/ver/', DetalleContactoView.as_view, name='detalle'),
    path('contacto/<int:pk>/borrar/', BorrarContactoView.as_view, name='borrar')
]