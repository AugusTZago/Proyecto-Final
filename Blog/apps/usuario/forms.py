from django.forms import CharField, DateField, ModelForm, PasswordInput
from django.contrib.auth.decorators import login_required
from apps.usuario.models import Usuario


class UserCreationForm(ModelForm):
    password = CharField(
        label='Contraseña', 
        widget=PasswordInput(
            attrs={'placeholder': 'Contraseña'}
            ), 
        required=True)
    password2 = CharField(
        label='Reingrese Contraseña', 
        widget=PasswordInput(
            attrs={'placeholder': 'Reingrese su contraseña'}
            ), 
        required=True)
    nacimiento = DateField(
        label="Ingrese fecha de nacimiento"
    )
    
    def clean(self):
        cleaned_form = super().clean() 
        password = cleaned_form.get('password')
        password2 = cleaned_form.get('password2')
        if password != password2:
            self.add_error("password2", "Las contraseñas no coinciden")
        return cleaned_form
    
    class Meta:
        model = Usuario
        fields = ('username', 'first_name','last_name','foto_perfil','email','nacimiento', 'password')



class UserEditionForm(ModelForm):

    nacimiento = DateField(
        label="Ingrese fecha de nacimiento"
    )
    
    def clean(self):
        return super().clean() 
    
    class Meta:
        model = Usuario
        fields = ('first_name','last_name','foto_perfil','email','nacimiento')