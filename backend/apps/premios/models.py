from django.db import models
from django.urls import path
from rest_framework import serializers, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from apps.usuarios.models import Usuario
from apps.fixture.models import Jugador, Partido
from django.utils import timezone


# ─── Models ──────────────────────────────────────────────────────────────────

class ResultadoPremios(models.Model):
    """Resultado real de los premios (lo carga el admin al final del torneo)"""
    bota_de_oro = models.ForeignKey(
        Jugador, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='bota_real'
    )
    guante_de_oro = models.ForeignKey(
        Jugador, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='guante_real'
    )
    balon_de_oro = models.ForeignKey(
        Jugador, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='balon_real'
    )
    mejor_joven = models.ForeignKey(
        Jugador, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='joven_real'
    )
    publicado = models.BooleanField(default=False)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Resultado premios'
        verbose_name_plural = 'Resultado premios'

    def __str__(self):
        return f'Premios del torneo (publicado: {self.publicado})'


class PronosticoPremio(models.Model):
    """Pronóstico de premios individuales por usuario"""
    usuario = models.OneToOneField(
        Usuario, on_delete=models.CASCADE, related_name='pronostico_premios'
    )
    bota_de_oro = models.ForeignKey(
        Jugador, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='pronosticos_bota'
    )
    guante_de_oro = models.ForeignKey(
        Jugador, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='pronosticos_guante'
    )
    balon_de_oro = models.ForeignKey(
        Jugador, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='pronosticos_balon'
    )
    mejor_joven = models.ForeignKey(
        Jugador, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='pronosticos_joven'
    )
    puntos_obtenidos = models.PositiveSmallIntegerField(null=True, blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    modificado_en = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Pronóstico de premios'
        verbose_name_plural = 'Pronósticos de premios'

    def __str__(self):
        return f'Premios de {self.usuario.username}'

    def calcular_puntos(self, resultado):
        """
        Calcula puntos según el ResultadoPremios oficial.
        Bota/Guante/Balón → 4 pts c/u
        Mejor Joven → 3 pts
        """
        if not resultado or not resultado.publicado:
            return None
        puntos = 0
        if self.bota_de_oro and self.bota_de_oro == resultado.bota_de_oro:
            puntos += 4
        if self.guante_de_oro and self.guante_de_oro == resultado.guante_de_oro:
            puntos += 4
        if self.balon_de_oro and self.balon_de_oro == resultado.balon_de_oro:
            puntos += 4
        if self.mejor_joven and self.mejor_joven == resultado.mejor_joven:
            puntos += 3
        return puntos


# ─── Helpers ─────────────────────────────────────────────────────────────────

def premios_bloqueados():
    """Los premios se bloquean al inicio del primer partido del torneo."""
    primer_partido = Partido.objects.order_by('fecha_hora').first()
    if not primer_partido:
        return False
    return timezone.now() >= primer_partido.fecha_hora - timezone.timedelta(minutes=5)


# ─── Serializers ─────────────────────────────────────────────────────────────

class PronosticoPremioSerializer(serializers.ModelSerializer):
    bloqueado = serializers.SerializerMethodField()

    class Meta:
        model = PronosticoPremio
        fields = (
            'id', 'bota_de_oro', 'guante_de_oro', 'balon_de_oro', 'mejor_joven',
            'puntos_obtenidos', 'bloqueado', 'creado_en', 'modificado_en',
        )
        read_only_fields = ('id', 'puntos_obtenidos', 'creado_en', 'modificado_en')

    def get_bloqueado(self, obj):
        return premios_bloqueados()

    def validate(self, attrs):
        if premios_bloqueados():
            raise serializers.ValidationError(
                'El torneo ya comenzó, no podés modificar los pronósticos de premios.'
            )
        # Validar que mejor_joven sea realmente sub-21
        mejor_joven = attrs.get('mejor_joven')
        if mejor_joven and not mejor_joven.es_sub21:
            raise serializers.ValidationError(
                {'mejor_joven': 'El jugador seleccionado no es sub-21.'}
            )
        return attrs


# ─── Views ───────────────────────────────────────────────────────────────────

class PronosticoPremioView(generics.RetrieveUpdateAPIView):
    serializer_class = PronosticoPremioSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        obj, _ = PronosticoPremio.objects.get_or_create(usuario=self.request.user)
        return obj


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def candidatos_premios(request):
    """
    Devuelve los jugadores candidatos para cada premio.
    - Bota de Oro y Balón de Oro: todos los jugadores
    - Guante de Oro: solo porteros
    - Mejor Joven: solo sub-21
    """
    from apps.fixture.serializers import JugadorSerializer
    from apps.fixture.models import Jugador

    return Response({
        'bota_de_oro': JugadorSerializer(
            Jugador.objects.select_related('equipo'), many=True
        ).data,
        'guante_de_oro': JugadorSerializer(
            Jugador.objects.filter(posicion='POR').select_related('equipo'), many=True
        ).data,
        'balon_de_oro': JugadorSerializer(
            Jugador.objects.select_related('equipo'), many=True
        ).data,
        'mejor_joven': JugadorSerializer(
            Jugador.objects.filter(edad__lte=21).select_related('equipo'), many=True
        ).data,
    })


# ─── URLs ────────────────────────────────────────────────────────────────────

urlpatterns = [
    path('',            PronosticoPremioView.as_view()),
    path('candidatos/', candidatos_premios),
]
