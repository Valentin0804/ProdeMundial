from django.db import models
from apps.usuarios.models import Usuario
from apps.fixture.models import Jugador, Partido
from django.utils import timezone


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

