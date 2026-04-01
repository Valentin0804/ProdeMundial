from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import GrupoPrivado, Miembro
from .serializers import (
    RegistroSerializer, UsuarioSerializer,
    GrupoPrivadoSerializer, MiembroSerializer,
)


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
def unirse_grupo(request):
    codigo = request.data.get('codigo_invitacion', '').upper()
    try:
        grupo = GrupoPrivado.objects.get(codigo_invitacion=codigo)
    except GrupoPrivado.DoesNotExist:
        return Response(
            {'error': 'Código inválido.'}, status=status.HTTP_404_NOT_FOUND
        )

    miembro, creado = Miembro.objects.get_or_create(
        grupo=grupo, usuario=request.user
    )
    if not creado:
        return Response({'error': 'Ya sos miembro de este grupo.'}, status=400)

    return Response(GrupoPrivadoSerializer(grupo).data, status=201)


class MiembrosGrupoView(generics.ListAPIView):
    serializer_class = MiembroSerializer

    def get_queryset(self):
        grupo_id = self.kwargs['grupo_id']
        return Miembro.objects.filter(grupo_id=grupo_id).select_related('usuario')
