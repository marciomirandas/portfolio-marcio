from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Base(models.Model):
    data_criacao = models.DateTimeField('Data de Criação', auto_now_add=True)
    data_modificao = models.DateTimeField('Data de Modificação', auto_now=True)
    ativo = models.BooleanField('Ativo', default=True)


class Tarefa(Base):
    STATUS = [
        ('pendente', 'Pendente'),
        ('iniciada', 'Iniciada'),
        ('concluida', 'Concluída'),
    ]

    nome = models.CharField('Nome', max_length=255)
    descricao = models.TextField('Descrição')
    vencimento = models.DateField('Data de Vencimento')
    status = models.CharField('Status', max_length=50, choices=STATUS)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Usuário', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Tarefa'
        verbose_name_plural = 'Tarefas'

    def __str__(self):
        return self.nome
