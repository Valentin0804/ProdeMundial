from rest_framework import serializers
from .models import Pronostico
from apps.fixture.serializers import PartidoSerializer

class PronosticoSerializer(serializers.ModelSerializer):
    partido_detalle = PartidoSerializer(source='partido', read_only=True)
    bloqueado = serializers.SerializerMethodField()

    class Meta:
        model = Pronostico
        fields = (
            'id', 'partido', 'partido_detalle',
            'goles_local', 'goles_visitante',
            'puntos_obtenidos', 'bloqueado',
            'creado_en', 'modificado_en',
        )
        read_only_fields = ('id', 'puntos_obtenidos', 'creado_en', 'modificado_en')

    def get_bloqueado(self, obj):
        return obj.partido.bloqueado

    def validate(self, attrs):
        partido = attrs.get('partido') or getattr(self.instance, 'partido', None)
        if partido.bloqueado:
            raise serializers.ValidationError(
                'El partido ya comenzó, no podés modificar el pronóstico.'
            )
        return attrs

