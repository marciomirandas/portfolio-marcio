from django.test import TestCase
from django.contrib.auth.models import User
from model_mommy import mommy
from django.urls import reverse
from django.contrib.messages import get_messages
import datetime

from tarefas.models import Tarefa
from tarefas.views import apagar_tarefa, nova_tarefa
from tarefas.forms import TarefaModelForm


class TarefasTest(TestCase):

    def setUp(self):
        self.usuario = mommy.make(User)
        self.tarefa1 = mommy.make(Tarefa, usuario=self.usuario)


    def test_tarefas_post(self):
        self.client.force_login(self.usuario)

        resposta = self.client.post(reverse('tarefas'), {'pesquisa': self.tarefa1.nome, 'opcao': self.tarefa1.status})

        self.assertEqual(resposta.status_code, 200)

        self.assertContains(resposta, self.tarefa1.nome)


class NovaTarefaTest(TestCase):

    def setUp(self):
        self.usuario = mommy.make(User)
        self.form_data = {
            'nome': 'valor1',
            'descricao': 'valor2',
            'vencimento': '2023-12-29',
            'status': 'iniciada'
        }

    def test_nova_tarefa_post_sucesso(self):
        self.client.force_login(self.usuario)

        resposta = self.client.post(reverse('nova-tarefa'), data=self.form_data)
        
        self.assertEqual(resposta.status_code, 302)
        self.assertEqual(Tarefa.objects.count(), 1)

        mensagens = [m.message for m in get_messages(resposta.wsgi_request)]
        self.assertIn('Tarefa criada com sucesso!', mensagens)

        nova_tarefa = Tarefa.objects.first()
        self.assertEqual(nova_tarefa.usuario, self.usuario)

        self.assertRedirects(resposta, reverse('tarefas'))


    def test_nova_tarefa_post_erro(self):
        self.client.force_login(self.usuario)

        formulario_invalido = {'campo1': 'valor1'}
        resposta = self.client.post(reverse('nova-tarefa'), data=formulario_invalido)

        mensagem = [m.message for m in get_messages(resposta.wsgi_request)]
        self.assertIn('Erro ao criar a tarefa!', mensagem)

        self.assertIsInstance(resposta.context['form'], TarefaModelForm)
    

    def test_nova_tarefa_get(self):
        self.client.force_login(self.usuario)

        resposta = self.client.get(reverse('nova-tarefa'))
        self.assertEqual(resposta.status_code, 200)
        self.assertIsInstance(resposta.context['form'], TarefaModelForm)
        self.assertTemplateUsed(resposta, 'tarefas/nova_tarefa.html')  


class EditarTarefaTest(TestCase):

    def setUp(self):
        self.usuario = mommy.make(User)
        self.tarefa = mommy.make(Tarefa, usuario=self.usuario)
        self.form_data = {
            'nome': 'valor1',
            'descricao': 'valor2',
            'vencimento': '2023-12-29',
            'status': 'iniciada'
        }


    def test_acesso_nao_permitido(self):
        outro_usuario = mommy.make(User)
        self.client.force_login(outro_usuario)

        resposta = self.client.get(reverse('editar-tarefa', args=[self.tarefa.id]))

        messagens = [m.message for m in get_messages(resposta.wsgi_request)]
        self.assertIn('Acesso não permitido!', messagens)

        self.assertRedirects(resposta, reverse('tarefas'))


    def test_editar_tarefa_post_sucesso(self):
        self.client.force_login(self.usuario)

        resposta = self.client.post(reverse('editar-tarefa', args=[self.tarefa.id]), data=self.form_data)
        
        self.assertEqual(resposta.status_code, 302)
        self.tarefa.refresh_from_db()
        self.assertEqual(self.tarefa.nome, 'valor1')
        self.assertEqual(self.tarefa.descricao, 'valor2')
        self.assertEqual(self.tarefa.vencimento, datetime.date(2023, 12, 29))
        self.assertEqual(self.tarefa.status, 'iniciada')

        messagens = [m.message for m in get_messages(resposta.wsgi_request)]
        self.assertIn('Tarefa editada com sucesso!', messagens)

        self.assertRedirects(resposta, reverse('tarefas'))

    
    def test_nova_tarefa_post_erro(self):
        self.client.force_login(self.usuario)

        formulario_invalido = {'campo1': 'valor1'}
        resposta = self.client.post(reverse('editar-tarefa', args=[self.tarefa.id]), data=formulario_invalido)

        mensagem = [m.message for m in get_messages(resposta.wsgi_request)]
        self.assertIn('Erro ao editar a tarefa!', mensagem)

        self.assertIsInstance(resposta.context['form'], TarefaModelForm)


    def test_editar_tarefa_get(self):
        self.client.force_login(self.usuario)

        resposta = self.client.get(reverse('editar-tarefa', args=[self.tarefa.id]))
        self.assertEqual(resposta.status_code, 200)
        self.assertIsInstance(resposta.context['form'], TarefaModelForm)
        self.assertTemplateUsed(resposta, 'tarefas/editar_tarefa.html')  
        


class VerTarefaTest(TestCase):

    def setUp(self):
        self.usuario = mommy.make(User)
        self.tarefa = mommy.make(Tarefa, usuario=self.usuario)


    def test_ver_tarefa(self):
        self.client.force_login(self.usuario)

        resposta = self.client.get(reverse('ver-tarefa', args=[self.tarefa.id]))

        self.assertEqual(resposta.status_code, 200)

        self.assertEqual(resposta.context['tarefa'], self.tarefa)

        self.assertTemplateUsed(resposta, 'tarefas/ver_tarefa.html')


    def test_acesso_nao_permitido(self):
        outro_usuario = mommy.make(User)
        self.client.force_login(outro_usuario)

        resposta = self.client.get(reverse('ver-tarefa', args=[self.tarefa.id]))

        messagens = [m.message for m in get_messages(resposta.wsgi_request)]
        self.assertIn('Acesso não permitido!', messagens)

        self.assertRedirects(resposta, reverse('tarefas'))


class ApagarTarefaTest(TestCase):

    def setUp(self):
        self.usuario = mommy.make(User)
        self.tarefa = mommy.make(Tarefa, usuario=self.usuario)


    def test_acesso_nao_permitido(self):
        outro_usuario = mommy.make(User)
        self.client.force_login(outro_usuario)

        resposta = self.client.get(reverse('apagar-tarefa', args=[self.tarefa.id]))

        messagens = [m.message for m in get_messages(resposta.wsgi_request)]
        self.assertIn('Acesso não permitido!', messagens)

        self.assertRedirects(resposta, reverse('tarefas'))


    def test_apagar_tarefa(self):
        self.client.force_login(self.usuario)

        resposta = self.client.get(reverse('apagar-tarefa', args=[self.tarefa.id]))

        messagens = [m.message for m in get_messages(resposta.wsgi_request)]
        self.assertIn('Tarefa apagada com sucesso!', messagens)

        self.assertRedirects(resposta, reverse('tarefas'))

        with self.assertRaises(Tarefa.DoesNotExist):
            Tarefa.objects.get(id=self.tarefa.id)