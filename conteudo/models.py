import uuid
from django.db import models
from django.contrib.auth.models import User
from stdimage.models import StdImageField
from django.conf import settings


def get_file_path(_instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'
    return 'materias/' + str(filename)


class Base(models.Model):
    data_criacao = models.DateTimeField('Data de Criação', auto_now_add=True)
    data_modificao = models.DateTimeField('Data de Modificação', auto_now=True)
    ativo = models.BooleanField('Ativo', default=True)


class Materia(Base):
    titulo = models.CharField('Título', max_length=255)
    subtitulo = models.CharField('Subtítulo', max_length=255)
    texto = models.TextField('Texto')
    slide = models.BooleanField('Slide', default=False)
    importante = models.BooleanField('importante', default=False)
    imagem = StdImageField('Imagem', upload_to=get_file_path, variations={'thumb': {'width': 1366, 'height': 600, 'crop': True}})
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Usuário', on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = 'Matéria'
        verbose_name_plural = 'Matérias'

    def __str__(self):
        return self.titulo

