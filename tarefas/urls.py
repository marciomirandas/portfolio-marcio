from django.urls import path
from .views import *

urlpatterns = [
    path('', tarefas, name='tarefas'),
    path('nova/', nova_tarefa, name='nova-tarefa'),
    path('ver/<int:id>/', ver_tarefa, name='ver-tarefa'),
    path('editar/<int:id>/', editar_tarefa, name='editar-tarefa'),
    path('apagar/<int:id>/', apagar_tarefa, name='apagar-tarefa')
]
