from rest_framework import generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Equipo, Jugador, Partido
from .serializers import EquipoSerializer, JugadorSerializer, PartidoSerializer
from django.http import HttpResponse, Http404
import requests



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
        return qs


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def fixture_grupos(request):
    partidos = Partido.objects.select_related('equipo_local', 'equipo_visitante').order_by('grupo', 'jornada', 'fecha_hora')

    resultado = {}
    for partido in partidos:
        g = partido.grupo
        j = str(partido.jornada)
        resultado.setdefault(g, {}).setdefault(j, [])
        resultado[g][j].append(PartidoSerializer(partido).data)

    return Response(resultado)

def proxy_foto_jugador(request, id_externo):
    url = f"https://content.actionnetwork.com/v1/photos/players/{id_externo}"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=5)
        
        if response.status_code == 200:
            return HttpResponse(response.content, content_type="image/png")
        
        url_alt = f"https://www.thesportsdb.com/images/media/player/render/{id_externo}.png"
        response_alt = requests.get(url_alt, timeout=3)
        if response_alt.status_code == 200:
            return HttpResponse(response_alt.content, content_type="image/png")

        raise Http404
    except Exception:
        raise Http404

class PartidoDetailView(generics.RetrieveAPIView):
    queryset = Partido.objects.select_related('equipo_local', 'equipo_visitante')
    serializer_class = PartidoSerializer
    permission_classes = [permissions.IsAuthenticated]

