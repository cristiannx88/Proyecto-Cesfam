from django import forms
from .models import Comunicado, Documento

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

