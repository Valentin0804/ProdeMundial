from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Sum, Count, Q, Max
from django.db.models.functions import Coalesce
import random
from datetime import date
from apps.fixture.models import Partido
from apps.usuarios.models import Usuario, GrupoPrivado
from .serializers import PronosticoSerializer
from .models import Pronostico


class PronosticoListCreateView(generics.ListCreateAPIView):
    serializer_class = PronosticoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Pronostico.objects.filter(
            usuario=self.request.user
        ).select_related('partido__equipo_local', 'partido__equipo_visitante')

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)


class PronosticoUpdateView(generics.UpdateAPIView):
    serializer_class = PronosticoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Pronostico.objects.filter(usuario=self.request.user)


def guardar_pronostico(request):
    user = request.user
    datos = request.data
    
    claves_premios = ['bota_de_oro', 'balon_de_oro', 'guante_de_oro', 'mejor_joven']
    
    pronostico, created = Pronostico.objects.get_or_create(user=user)
    
    if pronostico.premios_bloqueados:
        return Response({"error": "Los premios ya han sido enviados y están bloqueados."}, 
                        status=status.HTTP_403_FORBIDDEN)

    completos = all(getattr(pronostico, key) is not None for key in claves_premios)
    if completos:
        pronostico.premios_bloqueados = True
        pronostico.save()

    return Response({"message": "Guardado exitosamente", "bloqueado": pronostico.premios_bloqueados})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ranking_global(request):
    usuarios_qs = Usuario.objects.annotate(
        puntos_totales=Coalesce(Sum('pronosticos__puntos_obtenidos'), 0),
        exactos=Count('pronosticos', filter=Q(pronosticos__puntos_obtenidos=3)),
    )

    max_puntos = usuarios_qs.aggregate(Max('puntos_totales'))['puntos_totales__max'] or 0

    if max_puntos == 0:
        usuarios_list = list(usuarios_qs)
        random.seed(date.today().strftime("%Y%m%d"))
        random.shuffle(usuarios_list)
    else:
        usuarios_list = list(usuarios_qs.order_by('-puntos_totales', '-exactos', 'username'))

    full_ranking = []
    mi_posicion_data = None

    for i, u in enumerate(usuarios_list):
        user_data = {
            'posicion': i + 1,
            'usuario': u.username,
            'puntos_totales': u.puntos_totales,
            'exactos': u.exactos,
        }
        full_ranking.append(user_data)
        if u.id == request.user.id:
            mi_posicion_data = user_data

    return Response({
        'top_100': full_ranking[:100],
        'mi_posicion': mi_posicion_data,
        'torneo_empezado': max_puntos > 0
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ranking_grupo(request, grupo_id):
    """Tabla de posiciones de un grupo privado"""
    try:
        grupo = GrupoPrivado.objects.get(pk=grupo_id)
    except GrupoPrivado.DoesNotExist:
        return Response({'error': 'Grupo no encontrado'}, status=404)

    miembros_ids = grupo.miembros.values_list('usuario_id', flat=True)
    usuarios = Usuario.objects.filter(id__in=miembros_ids).annotate(
        puntos_totales=Sum('pronosticos__puntos_obtenidos'),
        exactos=Count('pronosticos', filter=Q(pronosticos__puntos_obtenidos=3)),
    ).order_by('-puntos_totales', '-exactos')

    data = [
        {
            'posicion': i + 1,
            'usuario': u.username,
            'puntos_totales': u.puntos_totales or 0,
            'exactos': u.exactos,
        }
        for i, u in enumerate(usuarios)
    ]
    return Response(data)
