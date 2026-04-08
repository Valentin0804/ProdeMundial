from rest_framework import serializers
from .models import PronosticoEliminatoria


class PronosticoElimSerializer(serializers.ModelSerializer):
    class Meta:
        model = PronosticoEliminatoria
        fields = (
            'id', 'partido', 'goles_local', 'goles_visitante',
            'pronostica_extra', 'pronostica_penales',
            'ganador_pronosticado', 'puntos_obtenidos',
        )
        read_only_fields = ('id', 'puntos_obtenidos')

    def validate(self, attrs):
        partido = attrs.get('partido') or self.instance.partido
        if partido.bloqueado:
            raise serializers.ValidationError(
                'El partido ya comenzó, no podés modificar el pronóstico.'
            )

        # Si pronostica penales, debe pronosticar extra también
        if attrs.get('pronostica_penales') and not attrs.get('pronostica_extra'):
            raise serializers.ValidationError(
                'Para pronosticar penales, primero debés marcar que va a extra time.'
            )

        # Validar que el ganador pronosticado sea uno de los dos equipos
        ganador = attrs.get('ganador_pronosticado')
        if ganador and partido.equipo_local and partido.equipo_visitante:
            if ganador not in [partido.equipo_local, partido.equipo_visitante]:
                raise serializers.ValidationError(
                    'El ganador debe ser uno de los dos equipos del partido.'
                )
        return attrs
