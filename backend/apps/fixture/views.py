from rest_framework import generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Equipo, Jugador, Partido
from .serializers import EquipoSerializer, JugadorSerializer, PartidoSerializer


class EquipoListView(generics.ListAPIView):
    queryset = Equipo.objects.all()
    serializer_class = EquipoSerializer
    permission_classes = [permissions.IsAuthenticated]


class JugadorListView(generics.ListAPIView):
    serializer_class = JugadorSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = Jugador.objects.select_related('equipo')
        equipo_id = self.request.query_params.get('equipo')
        posicion = self.request.query_params.get('posicion')
        sub21 = self.request.query_params.get('sub21')
        if equipo_id:
            qs = qs.filter(equipo_id=equipo_id)
        if posicion:
            qs = qs.filter(posicion=posicion)
        if sub21 == '1':
            qs = qs.filter(edad__lte=21)
        return qs


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def fixture_grupos(request):
    """
    Devuelve todos los partidos de grupos organizados por grupo y jornada.
    Estructura: { "A": { "1": [...], "2": [...], "3": [...] }, "B": {...}, ... }
    """
    partidos = Partido.objects.select_related(
        'equipo_local', 'equipo_visitante'
    ).order_by('grupo', 'jornada', 'fecha_hora')

    resultado = {}
    for partido in partidos:
        g = partido.grupo
        j = str(partido.jornada)
        resultado.setdefault(g, {}).setdefault(j, [])
        resultado[g][j].append(PartidoSerializer(partido).data)

    return Response(resultado)


class PartidoDetailView(generics.RetrieveAPIView):
    queryset = Partido.objects.select_related('equipo_local', 'equipo_visitante')
    serializer_class = PartidoSerializer
    permission_classes = [permissions.IsAuthenticated]
