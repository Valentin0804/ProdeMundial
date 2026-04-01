"""
motor_llaves.py
===============
Corazón del sistema: genera las llaves eliminatorias de cada usuario
basándose en sus pronósticos de fase de grupos.

Flujo:
  1. calcular_tabla_grupo()   → ordena los equipos de un grupo según puntos/DG/GF
  2. obtener_clasificados()   → extrae 1ro y 2do de cada grupo
  3. generar_cruces_octavos() → arma los 16 partidos de octavos según FIFA 2026
  4. LlavesUsuario            → objeto que encapsula todo el bracket del usuario
"""

from collections import defaultdict
from apps.fixture.models import Equipo, Partido
from apps.pronosticos.models import Pronostico


# ─── Mundial 2026: 12 grupos (A-L), 48 equipos, 32 clasificados ───────────────
# Cruces oficiales FIFA 2026 (sujeto a confirmación del reglamento definitivo):
# 1A vs 2B, 1C vs 2D, 1E vs 2F, 1G vs 2H, 1I vs 2J, 1K vs 2L
# 1B vs 2A, 1D vs 2C, 1F vs 2E, 1H vs 2G, 1J vs 2I, 1L vs 2K
# Más los 4 mejores terceros (simplificado: completar según reglamento final)

CRUCES_OCTAVOS = [
    ('1A', '2B'),
    ('1B', '2A'),
    ('1C', '2D'),
    ('1D', '2C'),
    ('1E', '2F'),
    ('1F', '2E'),
    ('1G', '2H'),
    ('1H', '2G'),
    ('1I', '2J'),
    ('1J', '2I'),
    ('1K', '2L'),
    ('1L', '2K'),
    # Los 4 mejores terceros (posiciones 13-16 del bracket)
    # Se resuelven una vez terminada la fase de grupos
    ('3A/B/C', '3D/E/F'),
    ('3G/H/I', '3J/K/L'),
    ('3A/B/D', '3C/E/F'),
    ('3G/H/J', '3I/K/L'),
]


def _resultado_pronostico(pronostico, equipo_local_id, equipo_visitante_id):
    """Devuelve (goles_local, goles_visitante) desde el pronóstico del usuario."""
    gl = pronostico.goles_local
    gv = pronostico.goles_visitante
    # Si los equipos están invertidos respecto al partido almacenado, invertir
    if pronostico.partido.equipo_local_id != equipo_local_id:
        return gv, gl
    return gl, gv


def calcular_tabla_grupo(usuario, grupo):
    """
    Calcula la tabla de posiciones de un grupo basándose en los
    pronósticos del usuario (o en los resultados reales si existen).

    Retorna lista de dicts ordenada: puntos → DG → GF → nombre.
    """
    partidos_grupo = Partido.objects.filter(grupo=grupo).select_related(
        'equipo_local', 'equipo_visitante'
    )

    # Inicializar stats para cada equipo
    equipos_ids = set()
    for p in partidos_grupo:
        equipos_ids.add(p.equipo_local_id)
        equipos_ids.add(p.equipo_visitante_id)

    stats = {
        eid: {'puntos': 0, 'dg': 0, 'gf': 0, 'gc': 0, 'pj': 0, 'equipo': None}
        for eid in equipos_ids
    }

    # Cargar equipos
    for p in partidos_grupo:
        stats[p.equipo_local_id]['equipo'] = p.equipo_local
        stats[p.equipo_visitante_id]['equipo'] = p.equipo_visitante

    # Índice de pronósticos del usuario para este grupo
    pronosticos_dict = {
        pr.partido_id: pr
        for pr in Pronostico.objects.filter(
            usuario=usuario,
            partido__grupo=grupo
        )
    }

    for partido in partidos_grupo:
        pid = partido.id

        # Usar resultado real si ya existe, si no usar pronóstico del usuario
        if partido.goles_local is not None:
            gl, gv = partido.goles_local, partido.goles_visitante
        elif pid in pronosticos_dict:
            pr = pronosticos_dict[pid]
            gl, gv = pr.goles_local, pr.goles_visitante
        else:
            continue  # Sin datos, no se cuenta

        lid = partido.equipo_local_id
        vid = partido.equipo_visitante_id

        # Actualizar stats
        stats[lid]['pj'] += 1
        stats[vid]['pj'] += 1
        stats[lid]['gf'] += gl
        stats[lid]['gc'] += gv
        stats[lid]['dg'] += gl - gv
        stats[vid]['gf'] += gv
        stats[vid]['gc'] += gl
        stats[vid]['dg'] += gv - gl

        if gl > gv:
            stats[lid]['puntos'] += 3
        elif gv > gl:
            stats[vid]['puntos'] += 3
        else:
            stats[lid]['puntos'] += 1
            stats[vid]['puntos'] += 1

    # Ordenar: puntos → DG → GF → nombre
    tabla = sorted(
        stats.values(),
        key=lambda s: (
            -s['puntos'],
            -s['dg'],
            -s['gf'],
            s['equipo'].nombre if s['equipo'] else ''
        )
    )
    return tabla


def obtener_clasificados(usuario):
    """
    Devuelve dict con los clasificados de cada grupo:
    {
      '1A': <Equipo>, '2A': <Equipo>,
      '1B': <Equipo>, '2B': <Equipo>,
      ...
    }
    """
    grupos = list('ABCDEFGHIJKL')
    clasificados = {}

    for grupo in grupos:
        tabla = calcular_tabla_grupo(usuario, grupo)
        if len(tabla) >= 1 and tabla[0]['equipo']:
            clasificados[f'1{grupo}'] = tabla[0]['equipo']
        if len(tabla) >= 2 and tabla[1]['equipo']:
            clasificados[f'2{grupo}'] = tabla[1]['equipo']
        # Guardar terceros para resolver mejores terceros
        if len(tabla) >= 3 and tabla[2]['equipo']:
            clasificados[f'3{grupo}'] = tabla[2]  # Guardamos stats completos

    return clasificados


def _resolver_mejor_tercero(clasificados, clave):
    """
    Placeholder para resolver los mejores terceros del Mundial 2026.
    La lógica exacta depende del reglamento FIFA definitivo.
    Por ahora devuelve el primero disponible de los grupos indicados.
    """
    grupos_posibles = [c for c in clave if c.isalpha()]
    for g in grupos_posibles:
        if f'3{g}' in clasificados:
            return clasificados[f'3{g}']['equipo']
    return None


def generar_bracket_usuario(usuario):
    """
    Genera el bracket completo del usuario basado en sus pronósticos.

    Retorna:
    {
      'tablas': { 'A': [tabla_ordenada], 'B': [...], ... },
      'octavos': [
        { 'orden': 1, 'local': Equipo|None, 'visitante': Equipo|None,
          'llave_local': '1A', 'llave_visitante': '2B' },
        ...
      ],
      'clasificados_completos': bool  # True si el usuario pronosticó todos los partidos
    }
    """
    grupos = list('ABCDEFGHIJKL')

    # Verificar si el usuario completó todos los pronósticos de grupos
    total_partidos = Partido.objects.count()
    pronosticos_usuario = Pronostico.objects.filter(usuario=usuario).count()
    clasificados_completos = (pronosticos_usuario >= total_partidos)

    # Calcular tablas
    tablas = {}
    for grupo in grupos:
        tabla = calcular_tabla_grupo(usuario, grupo)
        tablas[grupo] = [
            {
                'equipo': {
                    'id': s['equipo'].id,
                    'nombre': s['equipo'].nombre,
                    'codigo_fifa': s['equipo'].codigo_fifa,
                } if s['equipo'] else None,
                'puntos': s['puntos'],
                'pj': s['pj'],
                'gf': s['gf'],
                'gc': s['gc'],
                'dg': s['dg'],
            }
            for s in tabla
        ]

    # Obtener clasificados
    clasificados = obtener_clasificados(usuario)

    # Generar octavos
    octavos = []
    for i, (llave_l, llave_v) in enumerate(CRUCES_OCTAVOS):
        local = clasificados.get(llave_l)
        if isinstance(local, dict):
            local = local.get('equipo')

        visitante = clasificados.get(llave_v)
        if isinstance(visitante, dict):
            visitante = visitante.get('equipo')

        # Resolver mejores terceros si aplica
        if local is None and '/' in llave_l:
            local = _resolver_mejor_tercero(clasificados, llave_l)
        if visitante is None and '/' in llave_v:
            visitante = _resolver_mejor_tercero(clasificados, llave_v)

        octavos.append({
            'orden': i + 1,
            'llave_local': llave_l,
            'llave_visitante': llave_v,
            'local': {
                'id': local.id,
                'nombre': local.nombre,
                'codigo_fifa': local.codigo_fifa,
            } if local else None,
            'visitante': {
                'id': visitante.id,
                'nombre': visitante.nombre,
                'codigo_fifa': visitante.codigo_fifa,
            } if visitante else None,
        })

    return {
        'tablas': tablas,
        'octavos': octavos,
        'clasificados_completos': clasificados_completos,
        'pronosticos_cargados': pronosticos_usuario,
        'total_partidos': total_partidos,
    }
