from django.db import models
from django.utils import timezone


GRUPOS = [(g, f'Grupo {g}') for g in 'ABCDEFGHIJKL']  # Mundial 2026 tiene 12 grupos

FASES = [
    ('GRUPOS',   'Fase de grupos'),
    ('OCTAVOS',  'Octavos de final'),
    ('CUARTOS',  'Cuartos de final'),
    ('SEMIS',    'Semifinales'),
    ('TERCERO',  'Tercer puesto'),
    ('FINAL',    'Final'),
]

ESTADOS = [
    ('PENDIENTE',  'Pendiente'),
    ('EN_JUEGO',   'En juego'),
    ('FINALIZADO', 'Finalizado'),
]

POSICIONES = [
    ('POR', 'Portero'),
    ('DEF', 'Defensa'),
    ('MED', 'Mediocampista'),
    ('DEL', 'Delantero'),
]


class Equipo(models.Model):
    nombre = models.CharField(max_length=100)
    codigo_fifa = models.CharField(max_length=3, unique=True)  # Ej: ARG, BRA
    codigo_iso = models.CharField(max_length=2, null=True, blank=True)  # Ej: AR, BR
    grupo = models.CharField(max_length=1, choices=GRUPOS)
    escudo = models.ImageField(upload_to='escudos/', null=True, blank=True)
    confederacion = models.CharField(max_length=50, blank=True)

    class Meta:
        ordering = ['grupo', 'nombre']
        verbose_name = 'Equipo'
        verbose_name_plural = 'Equipos'

    def __str__(self):
        return f'{self.nombre} ({self.codigo_fifa})'


class Jugador(models.Model):
    nombre = models.CharField(max_length=100)
    equipo = models.ForeignKey(
        Equipo, on_delete=models.CASCADE, related_name='jugadores'
    )
    posicion = models.CharField(max_length=3, choices=POSICIONES)
    numero_camiseta = models.PositiveSmallIntegerField(null=True, blank=True)
    foto = models.ImageField(upload_to='jugadores/', null=True, blank=True)
    edad = models.PositiveSmallIntegerField(null=True, blank=True)

    class Meta:
        ordering = ['equipo', 'numero_camiseta']
        verbose_name = 'Jugador'
        verbose_name_plural = 'Jugadores'

    def __str__(self):
        return f'{self.nombre} ({self.equipo.codigo_fifa})'

    @property
    def es_sub21(self):
        """Usado para filtrar candidatos a Mejor Jugador Joven"""
        return self.edad is not None and self.edad <= 21


class Partido(models.Model):
    equipo_local = models.ForeignKey(
        Equipo, on_delete=models.CASCADE, related_name='partidos_local'
    )
    equipo_visitante = models.ForeignKey(
        Equipo, on_delete=models.CASCADE, related_name='partidos_visitante'
    )
    fecha_hora = models.DateTimeField()
    jornada = models.PositiveSmallIntegerField()  # 1, 2 o 3
    grupo = models.CharField(max_length=1, choices=GRUPOS)
    estadio = models.CharField(max_length=100, blank=True)
    ciudad = models.CharField(max_length=100, blank=True)

    # Resultado real (lo carga el admin)
    goles_local = models.PositiveSmallIntegerField(null=True, blank=True)
    goles_visitante = models.PositiveSmallIntegerField(null=True, blank=True)
    estado = models.CharField(max_length=12, choices=ESTADOS, default='PENDIENTE')

    class Meta:
        ordering = ['grupo', 'jornada', 'fecha_hora']
        verbose_name = 'Partido'
        verbose_name_plural = 'Partidos'

    def __str__(self):
        return (
            f'Grupo {self.grupo} J{self.jornada}: '
            f'{self.equipo_local.codigo_fifa} vs {self.equipo_visitante.codigo_fifa}'
        )

    @property
    def bloqueado(self):
        """El pronóstico se bloquea 5 minutos antes del partido"""
        return timezone.now() >= self.fecha_hora - timezone.timedelta(minutes=5)

    @property
    def resultado(self):
        if self.goles_local is None:
            return None
        return {'local': self.goles_local, 'visitante': self.goles_visitante}
