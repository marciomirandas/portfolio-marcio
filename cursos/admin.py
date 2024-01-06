from django.contrib import admin

from .models import *


@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ('id', 'titulo', 'url', 'criado', 'atualizado', 'ativo')


@admin.register(Avaliacao)
class AvaliacaoAdmin(admin.ModelAdmin):
    list_display = ('curso', 'nome', 'email', 'avaliacao', 'criado', 'atualizado', 'ativo')