from django.db.models import Sum, Count, Q
from django.db.models.functions import Coalesce
from django.shortcuts import get_object_or_404
from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.pronosticos.models import Partido, Pronostico 
from .models import GrupoPrivado, Miembro
from .serializers import ( RegistroSerializer, UsuarioSerializer, GrupoPrivadoSerializer, MiembroSerializer )

class RegistroView(generics.CreateAPIView):
    serializer_class = RegistroSerializer
    permission_classes = [permissions.AllowAny]


class PerfilView(generics.RetrieveUpdateAPIView):
    serializer_class = UsuarioSerializer

    def get_object(self):
        return self.request.user


class GrupoPrivadoListCreateView(generics.ListCreateAPIView):
    serializer_class = GrupoPrivadoSerializer
    permission_classes = [permissions.IsAuthenticated]
    ordering = ['-creado_en']

    def get_queryset(self):
        return GrupoPrivado.objects.filter(
            miembros__usuario=self.request.user
        ).distinct().order_by('-creado_en')
        
    def perform_create(self, serializer):
        grupo = serializer.save(admin=self.request.user)
        Miembro.objects.create(grupo=grupo, usuario=self.request.user)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unirse_grupo(request):
    try:
        codigo = request.data.get('codigo_invitacion', '').upper()
        grupo = GrupoPrivado.objects.get(codigo_invitacion=codigo)
        miembro, creado = Miembro.objects.get_or_create(grupo=grupo, usuario=request.user)
        
        if not creado:
            return Response({'error': 'Ya sos miembro de este grupo.'}, status=400)

        return Response(GrupoPrivadoSerializer(grupo).data, status=201)

    except GrupoPrivado.DoesNotExist:
        return Response({'error': 'Código inválido.'}, status=404)
    except Exception as e:
        return Response({'error': str(e)}, status=500)

class MiembrosGrupoView(generics.ListAPIView):
    serializer_class = MiembroSerializer

    def get_queryset(self):
        grupo_id = self.kwargs['grupo_id']
        return Miembro.objects.filter(grupo_id=grupo_id).select_related('usuario')


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def detalle_grupo_modal(request, grupo_id):

    try:
        grupo = get_object_or_404(GrupoPrivado, id=grupo_id)
        
        miembros = Miembro.objects.filter(grupo=grupo).annotate(
            puntos=Coalesce(Sum('usuario__pronosticos__puntos_obtenidos'), 0),
            exactos=Count('usuario__pronosticos', filter=Q(usuario__pronosticos__puntos_obtenidos=3))
        ).order_by('-puntos', '-exactos')

        data = {
            'nombre_grupo': grupo.nombre,
            'codigo_invitacion': grupo.codigo_invitacion,
            'soy_admin': (grupo.admin == request.user),
            'miembros': [{
                'id': m.usuario.id,
                'username': m.usuario.username,
                'puntos': m.puntos,
                'exactos': m.exactos,
                'es_creador': (m.usuario == grupo.admin)
            } for m in miembros]
        }
        return Response(data)
    except Exception as e:
        print(f"Error real: {e}")
        return Response({'error': str(e)}, status=500)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def eliminar_miembro(request, grupo_id, usuario_id):
    grupo = get_object_or_404(GrupoPrivado, id=grupo_id)
    if grupo.admin != request.user:
        return Response({'error': 'No sos el admin'}, status=403)
    
    if usuario_id == request.user.id:
        return Response({'error': 'No podés eliminarte a vos mismo, usá salir'}, status=400)

    Miembro.objects.filter(grupo=grupo, usuario_id=usuario_id).delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def salir_grupo(request, grupo_id):
    Miembro.objects.filter(grupo_id=grupo_id, usuario=request.user).delete()
    return Response(status=status.HTTP_204_NO_CONTENT)