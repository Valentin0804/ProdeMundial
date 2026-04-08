from rest_framework import serializers
from .models import PronosticoPremio, premios_bloqueados

class PronosticoPremioSerializer(serializers.ModelSerializer):
    bloqueado = serializers.SerializerMethodField()

    class Meta:
        model = PronosticoPremio
        fields = (
            'id', 'bota_de_oro', 'guante_de_oro', 'balon_de_oro', 'mejor_joven',
            'puntos_obtenidos', 'bloqueado', 'creado_en', 'modificado_en',
        )
        read_only_fields = ('id', 'puntos_obtenidos', 'creado_en', 'modificado_en')

    def get_bloqueado(self, obj):
        return premios_bloqueados()

    def validate(self, attrs):
        if premios_bloqueados():
            raise serializers.ValidationError(
                'El torneo ya comenzó, no podés modificar los pronósticos de premios.'
            )
        if self.instance and self.instance.bota_de_oro:
            raise serializers.ValidationError(
                'Ya tenés un pronóstico guardado, no podés modificarlo.'
            )
        return attrs

