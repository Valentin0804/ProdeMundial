from django.db import models
from django.utils import timezone
from apps.usuarios.models import Usuario
from apps.fixture.models import Equipo, FASES, ESTADOS


class PartidoEliminatoria(models.Model):
    """
    Partido de fase eliminatoria.
    Puede ser real (admin lo crea) o virtual (generado desde pronósticos del usuario).
    """
    fase = models.CharField(max_length=10, choices=FASES[1:])
    orden = models.PositiveSmallIntegerField(default=0)  # Para ordenar dentro de la fase
    equipo_local = models.ForeignKey(
        Equipo, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='elim_local'
    )
    equipo_visitante = models.ForeignKey(
        Equipo, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='elim_visitante'
    )
    fecha_hora = models.DateTimeField(null=True, blank=True)
    estadio = models.CharField(max_length=100, blank=True)

    # Resultado real
    goles_local = models.PositiveSmallIntegerField(null=True, blank=True)
    goles_visitante = models.PositiveSmallIntegerField(null=True, blank=True)
    fue_a_extra = models.BooleanField(default=False)
    fue_a_penales = models.BooleanField(default=False)
    ganador = models.ForeignKey(
        Equipo, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='elim_ganadas'
    )
    estado = models.CharField(max_length=12, choices=ESTADOS, default='PENDIENTE')

    class Meta:
        ordering = ['fase', 'orden']
        verbose_name = 'Partido eliminatoria'
        verbose_name_plural = 'Partidos eliminatorias'

    def __str__(self):
        local = self.equipo_local.codigo_fifa if self.equipo_local else '?'
        visit = self.equipo_visitante.codigo_fifa if self.equipo_visitante else '?'
        return f'{self.fase} {self.orden}: {local} vs {visit}'

    @property
    def bloqueado(self):
        if not self.fecha_hora:
            return False
        return timezone.now() >= self.fecha_hora - timezone.timedelta(minutes=5)


class PronosticoEliminatoria(models.Model):
    usuario = models.ForeignKey(
        Usuario, on_delete=models.CASCADE, related_name='pronosticos_elim'
    )
    partido = models.ForeignKey(
        PartidoEliminatoria, on_delete=models.CASCADE, related_name='pronosticos'
    )
    goles_local = models.PositiveSmallIntegerField()
    goles_visitante = models.PositiveSmallIntegerField()
    pronostica_extra = models.BooleanField(default=False)
    pronostica_penales = models.BooleanField(default=False)
    ganador_pronosticado = models.ForeignKey(
        Equipo, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='pronosticos_ganador'
    )
    puntos_obtenidos = models.PositiveSmallIntegerField(null=True, blank=True)

    class Meta:
        unique_together = ('usuario', 'partido')

    def calcular_puntos(self):
        p = self.partido
        if p.ganador is None:
            return None

        puntos = 0
        rl, rv = p.goles_local, p.goles_visitante
        pl, pv = self.goles_local, self.goles_visitante

        # Resultado exacto en 90 min → 3 pts
        if rl == pl and rv == pv:
            puntos += 3
        # Solo el ganador correcto → 1 pt
        elif self.ganador_pronosticado == p.ganador:
            puntos += 1

        # Bonus por acertar extra time → +1 pt
        if self.pronostica_extra == p.fue_a_extra:
            puntos += 1

        # Bonus por acertar penales → +1 pt (solo si acertó el extra)
        if p.fue_a_extra and self.pronostica_penales == p.fue_a_penales:
            puntos += 1

        return puntos
