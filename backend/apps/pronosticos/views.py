from rest_framework import serializers, generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.urls import path
from django.db.models import Sum, Count, Q
from .models import Pronostico
from apps.fixture.models import Partido
from apps.fixture.serializers import PartidoSerializer
from apps.usuarios.models import Usuario, GrupoPrivado


# ───── Serializers ─────

class PronosticoSerializer(serializers.ModelSerializer):
    partido_detalle = PartidoSerializer(source='partido', read_only=True)
    bloqueado = serializers.SerializerMethodField()

    class Meta:
        model = Pronostico
        fields = (
            'id', 'partido', 'partido_detalle',
            'goles_local', 'goles_visitante',
            'puntos_obtenidos', 'bloqueado',
            'creado_en', 'modificado_en',
        )
        read_only_fields = ('id', 'puntos_obtenidos', 'creado_en', 'modificado_en')

    def get_bloqueado(self, obj):
        return obj.partido.bloqueado

    def validate(self, attrs):
        partido = attrs.get('partido') or self.instance.partido
        if partido.bloqueado:
            raise serializers.ValidationError(
                'El partido ya comenzó, no podés modificar el pronóstico.'
            )
        return attrs


# ───── Views ─────

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


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ranking_global(request):
    """Tabla de posiciones global ordenada por puntos totales"""
    usuarios = Usuario.objects.annotate(
        puntos_totales=Sum('pronosticos__puntos_obtenidos'),
        exactos=Count('pronosticos', filter=Q(pronosticos__puntos_obtenidos=3)),
        acertados=Count('pronosticos', filter=Q(pronosticos__puntos_obtenidos__gte=1)),
        jugados=Count('pronosticos', filter=Q(pronosticos__puntos_obtenidos__isnull=False)),
    ).order_by('-puntos_totales', '-exactos')

    data = [
        {
            'posicion': i + 1,
            'usuario': u.username,
            'avatar': u.avatar.url if u.avatar else None,
            'puntos_totales': u.puntos_totales or 0,
            'exactos': u.exactos,
            'acertados': u.acertados,
            'jugados': u.jugados,
        }
        for i, u in enumerate(usuarios)
    ]
    return Response(data)


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


# ───── URLs ─────

urlpatterns = [
    path('',                    PronosticoListCreateView.as_view()),
    path('<int:pk>/',           PronosticoUpdateView.as_view()),
    path('ranking/global/',     ranking_global),
    path('ranking/grupo/<int:grupo_id>/', ranking_grupo),
]
