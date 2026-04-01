from django.urls import path
from rest_framework import generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import PronosticoPremio, premios_bloqueados
from apps.fixture.models import Jugador
from apps.fixture.serializers import JugadorSerializer


class PronosticoPremioSerializer:
    pass  # definido en models.py, importado desde allá


from .models import PronosticoPremioSerializer  # noqa


class PronosticoPremioView(generics.RetrieveUpdateAPIView):
    serializer_class = PronosticoPremioSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        obj, _ = PronosticoPremio.objects.get_or_create(usuario=self.request.user)
        return obj


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def candidatos_premios(request):
    return Response({
        'bota_de_oro':   JugadorSerializer(Jugador.objects.select_related('equipo'), many=True).data,
        'guante_de_oro': JugadorSerializer(Jugador.objects.filter(posicion='POR').select_related('equipo'), many=True).data,
        'balon_de_oro':  JugadorSerializer(Jugador.objects.select_related('equipo'), many=True).data,
        'mejor_joven':   JugadorSerializer(Jugador.objects.filter(edad__lte=21).select_related('equipo'), many=True).data,
    })


urlpatterns = [
    path('',            PronosticoPremioView.as_view()),
    path('candidatos/', candidatos_premios),
]
