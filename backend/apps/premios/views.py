from rest_framework import generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import PronosticoPremio, premios_bloqueados
from .serializers import PronosticoPremioSerializer
from apps.fixture.models import Jugador
from apps.fixture.serializers import JugadorSerializer

class PronosticoPremioView(generics.RetrieveUpdateAPIView):
    serializer_class = PronosticoPremioSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        obj, _ = PronosticoPremio.objects.get_or_create(usuario=self.request.user)
        return obj


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def candidatos_premios(request):
    jugadores = Jugador.objects.select_related('equipo')
    return Response({
        'bota_de_oro': JugadorSerializer(jugadores, many=True).data,
        'guante_de_oro': JugadorSerializer(jugadores.filter(posicion='POR'), many=True).data,
        'balon_de_oro': JugadorSerializer(jugadores, many=True).data,
        'mejor_joven': JugadorSerializer(jugadores.filter(edad__lte=21), many=True).data,
    })
