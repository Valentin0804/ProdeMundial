from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics, status
from django.urls import path
from .motor_llaves import generar_bracket_usuario
from .models import PartidoEliminatoria, PronosticoEliminatoria
from apps.fixture.models import Equipo
from .serializers import PronosticoElimSerializer

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
