from django.forms import ModelForm, TextInput, FileInput, Textarea
from apps.posteo.models import Post, Categoria

class PostCreationForm(ModelForm):

    class Meta:
        model = Post
        widgets = {'titulo' : TextInput(attrs={'placeholder': 'Ingrese su titulo'}), 
                   'contenido': TextInput(attrs={'placeholder': 'Ingrese aqui el contenido'}),
                   'image' : FileInput(),
                   
                   }
        exclude = ['autor', 'creado', 'modificado']

class CategoriaForm(ModelForm):
    class Meta:
        model = Categoria
        exclude = ['pk']
        widgets = {'categoria': TextInput(attrs={'placeholder' : 'Ingrese su categoria', 'max_length' : 40}),}
        exclude = ['is_active']