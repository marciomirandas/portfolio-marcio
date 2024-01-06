from django import forms
from .models import *

class MateriaModelForm(forms.ModelForm):
    class Meta:
        model = Materia
        fields = ['titulo', 'subtitulo', 'texto', 'imagem', 'slide', 'importante']