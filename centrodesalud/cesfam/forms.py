from django import forms
from .models import Comunicado, Documento, Usuario, Rol, SolicitudPermiso
from django.contrib.auth.forms import UserCreationForm


class ComunicadoForm(forms.ModelForm):
    class Meta:
        model = Comunicado
        fields = ['titulo', 'contenido', 'tipo', 'destacado', 'archivo_adjunto']
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Título del comunicado'
            }),
            'contenido': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Comparte un anuncio rápido con tus colegas...'
            }),
            'tipo': forms.Select(attrs={
                'class': 'form-select w-auto'
            }),
            'destacado': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'archivo_adjunto': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
        }


class DocumentoForm(forms.ModelForm):
    class Meta:
        model = Documento
        fields = ['titulo', 'descripcion', 'tipo', 'ruta_archivo']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título del documento'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Descripción del documento'}),
            'tipo': forms.Select(attrs={'class': 'form-select w-auto'}),
            'ruta_archivo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


class RegistroForm(UserCreationForm):
    id_rol = forms.ModelChoiceField(
        queryset=Rol.objects.all(),
        label="Rol",
        required=True,
        empty_label="Seleccione un rol",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Usuario
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'rut',
            'telefono',
            'cargo',
            'departamento',
            'observaciones',
            'id_rol',  
            'password1',
            'password2'
        ]
        labels = {
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'rut': 'RUT',
            'telefono': 'Teléfono',
            'cargo': 'Cargo',
            'departamento': 'Departamento',
            'observaciones': 'Observaciones',
            'email': 'Correo electrónico',
            'id_rol': 'Rol del usuario',
        }
        widgets = {
            'observaciones': forms.Textarea(attrs={'rows': 3}),
        }


class SolicitudPermisoForm(forms.ModelForm):
    class Meta:
        model = SolicitudPermiso
        fields = ['tipo_permiso', 'fecha_inicio', 'fecha_fin', 'documento_respaldo']

        widgets = {
            'tipo_permiso': forms.Select(attrs={
                'class': 'form-select',
                'placeholder': 'Seleccione el tipo de permiso'
            }),
            'fecha_inicio': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'fecha_fin': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'documento_respaldo': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
        }

        labels = {
            'tipo_permiso': 'Tipo de Permiso',
            'fecha_inicio': 'Fecha de Inicio',
            'fecha_fin': 'Fecha de Fin',
            'documento_respaldo': 'Documento de Respaldo (opcional)',
        }