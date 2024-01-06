from django.test import TestCase
from model_mommy import mommy

class TarefaTestCase(TestCase):
    
    def setUp(self):
        self.tarefa = mommy.make('Tarefa')

    def test_str(self):
        self.assertEquals(str(self.tarefa), self.tarefa.nome)