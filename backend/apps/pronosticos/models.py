from django.db import models
from apps.usuarios.models import Usuario
from apps.fixture.models import Partido


class Pronostico(models.Model):
    """Pronóstico de un partido de fase de grupos"""
    usuario = models.ForeignKey(
        Usuario, on_delete=models.CASCADE, related_name='pronosticos'
    )
    partido = models.ForeignKey(
        Partido, on_delete=models.CASCADE, related_name='pronosticos'
    )
    goles_local = models.PositiveSmallIntegerField()
    goles_visitante = models.PositiveSmallIntegerField()
    puntos_obtenidos = models.PositiveSmallIntegerField(null=True, blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    modificado_en = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('usuario', 'partido')
        verbose_name = 'Pronóstico'
        verbose_name_plural = 'Pronósticos'

    def __str__(self):
        return (
            f'{self.usuario.username}: '
            f'{self.partido.equipo_local.codigo_fifa} {self.goles_local}'
            f'-{self.goles_visitante} '
            f'{self.partido.equipo_visitante.codigo_fifa}'
        )

    def calcular_puntos(self):
        """
        Sistema de puntos:
          3 pts → resultado exacto
          2 pts → ganador correcto + diferencia de goles exacta
          1 pt  → solo el ganador o empate correcto
          0 pts → nada
        """
        p = self.partido
        if p.goles_local is None or p.goles_visitante is None:
            return None

        # Resultado real
        rl, rv = p.goles_local, p.goles_visitante
        # Pronóstico
        pl, pv = self.goles_local, self.goles_visitante

        # 3 pts: exacto
        if rl == pl and rv == pv:
            return 3

        # Ganador real
        def ganador(l, v):
            if l > v: return 'local'
            if v > l: return 'visitante'
            return 'empate'

        if ganador(rl, rv) == ganador(pl, pv):
            # 2 pts: ganador + diferencia igual
            if (rl - rv) == (pl - pv):
                return 2
            # 1 pt: solo el ganador
            return 1

        return 0

    def save(self, *args, **kwargs):
        # Recalcular puntos si el partido ya tiene resultado
        if self.partido.goles_local is not None:
            self.puntos_obtenidos = self.calcular_puntos()
        super().save(*args, **kwargs)
