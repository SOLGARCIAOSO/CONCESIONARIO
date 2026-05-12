from django import forms
from .models import Rol, TipoDocumento

class UsuarioForm(forms.Form):
    nombre = forms.CharField(label='Nombre completo', max_length=100)
    tipo_documento = forms.ChoiceField(label='Tipo documento', choices=TipoDocumento.choices)
    numero_documento = forms.CharField(label='Número documento', max_length=20)
    telefono = forms.CharField(label='Teléfono', max_length=20, required=False)
    direccion = forms.CharField(label='Dirección', max_length=150, required=False)
    email = forms.EmailField(label='Correo electrónico')
    rol = forms.ModelChoiceField(queryset=Rol.objects.all(), label='Rol')
    contrasena = forms.CharField(label='Contraseña', widget=forms.PasswordInput())
    habilitado = forms.BooleanField(label='Habilitado', required=False)