from django import forms
from .models import *

class TarefaModelForm(forms.ModelForm):
    class Meta:
        model = Tarefa
        fields = ['nome', 'descricao', 'vencimento', 'status']

        widgets = {
                'nome': forms.TextInput(attrs={'class': 'form-control'}),
                'descricao': forms.Textarea(attrs={'class': 'form-control'}),
                'vencimento': forms.DateInput(format=('%Y-%m-%d'),attrs={'class': 'form-control', 'type': 'date'}),
                'status': forms.Select(attrs={'class': 'form-select'}),
        }