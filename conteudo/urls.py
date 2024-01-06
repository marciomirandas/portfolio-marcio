from django.urls import path
from .views import *

urlpatterns = [
    path('', site, name='conteudo-site'),
    path('materia/<int:id>/', materia, name='materia'),
    path('adm/', adm_conteudo, name='adm-conteudo'),
    path('nova/', nova_materia, name='nova-materia'),
    path('editar/<int:id>/', editar_materia, name='editar-materia'),
    path('apagar/<int:id>/', apagar_materia, name='apagar-materia'),
]
