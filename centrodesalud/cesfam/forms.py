from django import forms
from .models import Comunicado

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
