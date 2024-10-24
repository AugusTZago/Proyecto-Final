from django.forms import EmailField, ModelForm
from django.core import validators

from apps.contacto.models import Contacto

class ContactoForm(ModelForm):
    email = EmailField(validators=[validators.EmailValidator(message='Ingrese un email válido')])

    class Meta:
        model= Contacto
        fields = ('nombre', 'email', 'asunto', 'mensaje')