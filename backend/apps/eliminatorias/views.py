from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics, serializers, status
from django.urls import path
from .motor_llaves import generar_bracket_usuario
from .models import PartidoEliminatoria, PronosticoEliminatoria
from apps.fixture.models import Equipo


# ─── Serializers ─────────────────────────────────────────────────────────────

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


# ─── Views ───────────────────────────────────────────────────────────────────

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def bracket_usuario(request, usuario_id=None):
    """
    Devuelve el bracket completo generado desde los pronósticos del usuario.
    Si no se pasa usuario_id, usa el usuario autenticado.
    """
    from apps.usuarios.models import Usuario
    if usuario_id:
        try:
            usuario = Usuario.objects.get(pk=usuario_id)
        except Usuario.DoesNotExist:
            return Response({'error': 'Usuario no encontrado'}, status=404)
    else:
        usuario = request.user

    bracket = generar_bracket_usuario(usuario)
    return Response(bracket)


class PronosticoElimListCreateView(generics.ListCreateAPIView):
    serializer_class = PronosticoElimSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return PronosticoEliminatoria.objects.filter(
            usuario=self.request.user
        ).select_related('partido', 'ganador_pronosticado')

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)


class PronosticoElimUpdateView(generics.UpdateAPIView):
    serializer_class = PronosticoElimSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return PronosticoEliminatoria.objects.filter(usuario=self.request.user)


# ─── URLs ────────────────────────────────────────────────────────────────────

urlpatterns = [
    path('bracket/',                    bracket_usuario),
    path('bracket/<int:usuario_id>/',   bracket_usuario),
    path('pronosticos/',                PronosticoElimListCreateView.as_view()),
    path('pronosticos/<int:pk>/',       PronosticoElimUpdateView.as_view()),
]
