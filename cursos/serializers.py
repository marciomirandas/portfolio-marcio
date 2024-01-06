from rest_framework import serializers

from django.db.models import Avg

from .models import *


class AvaliacaoSerializer(serializers.ModelSerializer):
    class Meta:
        extra_kargs = {
            'email': {'write_only':True}
        }
        model = Avaliacao
        fields = (
            'id',
            'curso',
            'nome',
            'email',
            'comentario',
            'avaliacao',
            'criado',
            'ativo'
        )

        def validate_avaliacao(self, valor):
            if valor in range(1, 6):
                return valor
            raise serializers.ValidationError('Inserir um número inteiro entre 1 e 5 para a avaliação') 


class CursoSerializer(serializers.ModelSerializer):
    # Nested Relationship
    #avaliacoes = AvaliacaoSerializer(many=True, read_only=True)

    # Hiperlinked Related Field
    #avaliacoes = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='avaliacao-detail')

    # Primary Key Related Field
    #avaliacoes = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    media_avaliacoes = serializers.SerializerMethodField()


    class Meta:
        model = Curso
        fields = (
            'id',
            'titulo',
            'url',
            'criado',
            'ativo',
            'avaliacoes',
            'media_avaliacoes'
        )
    
    def get_media_avaliacoes(self, obj):
        media = obj.avaliacoes.aggregate(Avg('avaliacao')).get('avaliacao__avg')

        if media is None:
            return 0
        return round(media * 2) / 2
