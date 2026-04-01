# serializers.py
from rest_framework import serializers
from .models import Equipo, Jugador, Partido


class EquipoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipo
        fields = '__all__'


class JugadorSerializer(serializers.ModelSerializer):
    equipo_nombre = serializers.CharField(source='equipo.nombre', read_only=True)
    equipo_codigo = serializers.CharField(source='equipo.codigo_fifa', read_only=True)

    class Meta:
        model = Jugador
        fields = ('id', 'nombre', 'equipo', 'equipo_nombre', 'equipo_codigo',
                  'posicion', 'numero_camiseta', 'foto', 'edad', 'es_sub21')


class PartidoSerializer(serializers.ModelSerializer):
    equipo_local = EquipoSerializer(read_only=True)
    equipo_visitante = EquipoSerializer(read_only=True)
    bloqueado = serializers.BooleanField(read_only=True)

    class Meta:
        model = Partido
        fields = ('id', 'equipo_local', 'equipo_visitante', 'fecha_hora',
                  'jornada', 'grupo', 'estadio', 'ciudad',
                  'goles_local', 'goles_visitante', 'estado', 'bloqueado')
