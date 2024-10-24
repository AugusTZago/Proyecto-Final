from django.forms import ModelForm, TextInput, CharField
from apps.posteo.models import Post, Categoria

from apps.comentario.models import Comentario
class ComentarioCreationForm(ModelForm):
    contenido = CharField(label= 'Ingrese su comentario',min_length=10, max_length=255, 
        widget=TextInput(attrs={'placeholder': 'Ingrese su comentario, maximo de 255 caracteres.'}))
    class Meta:
        model = Comentario
        fields = ('contenido',)

