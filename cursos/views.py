from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework import permissions

from .models import Curso, Avaliacao
from .serializers import CursoSerializer, AvaliacaoSerializer
from .permissions import IsSuperUser


"""
API V1
"""

class CursoViewSet(viewsets.ModelViewSet):
    # Só permite excluir um registro se for superuser
    permission_classes = (IsSuperUser, )

    queryset = Curso.objects.all()
    serializer_class = CursoSerializer

    @action(detail=True, methods=['get'])
    def avaliacoes(self, request, pk=None):

        # Paginação
        self.pagination_class.page_size = 1
        avaliacoes = Avaliacao.objects.filter(curso_id=pk)
        page = self.paginate_queryset(avaliacoes)

        if page is not None:
            serializer = AvaliacaoSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = AvaliacaoSerializer(avaliacoes, many=True)
        return Response(serializer.data)
    

# Uma forma de não permitir a utilização de todos os métodos disponíveis
class AvaliacaoViewSet(
        mixins.ListModelMixin,
        mixins.CreateModelMixin,
        mixins.RetrieveModelMixin,
        mixins.UpdateModelMixin,
        #mixins.DestroyModelMixin,
        viewsets.GenericViewSet
        ):
    
    # Só permite acessar essa view se tiver permissão
    permission_classes = (permissions.DjangoModelPermissions, )

    queryset = Avaliacao.objects.all()
    serializer_class = AvaliacaoSerializer