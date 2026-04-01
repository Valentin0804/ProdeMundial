"""
Management command: cargar_fixture
===================================
Descarga el fixture del Mundial 2026 desde el repo público de openfootball
(sin API key, dominio público) y lo carga en la base de datos.

Uso:
    python manage.py cargar_fixture
    python manage.py cargar_fixture --limpiar   # borra todo antes de cargar

Fuente:
    https://github.com/openfootball/worldcup.json
    Raw JSON: https://raw.githubusercontent.com/openfootball/worldcup.json/master/2026/worldcup.json
"""

import urllib.request
import json
from datetime import datetime, timezone as dt_timezone
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from apps.fixture.models import Equipo, Partido

URL_FIXTURE = (
    "https://raw.githubusercontent.com/"
    "openfootball/worldcup.json/master/2026/worldcup.json"
)

# Mapeo de nombre de país (openfootball) → código FIFA de 3 letras
# Completar/ajustar según los nombres que devuelva el JSON
CODIGOS_FIFA = {
    "Mexico":                  "MEX",
    "South Africa":            "RSA",
    "South Korea":             "KOR",
    "Argentina":               "ARG",
    "Morocco":                 "MAR",
    "Portugal":                "POR",
    "USA":                     "USA",
    "United States":           "USA",
    "Panama":                  "PAN",
    "Honduras":                "HON",
    "Spain":                   "ESP",
    "China":                   "CHN",
    "Switzerland":             "SUI",
    "New Zealand":             "NZL",
    "Germany":                 "GER",
    "Japan":                   "JPN",
    "Uruguay":                 "URU",
    "Australia":               "AUS",
    "Serbia":                  "SRB",
    "Netherlands":             "NED",
    "France":                  "FRA",
    "Ecuador":                 "ECU",
    "Canada":                  "CAN",
    "England":                 "ENG",
    "Senegal":                 "SEN",
    "Brazil":                  "BRA",
    "Saudi Arabia":            "KSA",
    "Belgium":                 "BEL",
    "Colombia":                "COL",
    "Croatia":                 "CRO",
    "Poland":                  "POL",
    "Iran":                    "IRN",
    "Nigeria":                 "NGA",
    "Ivory Coast":             "CIV",
    "Cameroon":                "CMR",
    "Venezuela":               "VEN",
    "Peru":                    "PER",
    "Paraguay":                "PAR",
    "Bolivia":                 "BOL",
    "Chile":                   "CHI",
    "Egypt":                   "EGY",
    "Algeria":                 "ALG",
    "Tunisia":                 "TUN",
    "Ghana":                   "GHA",
    "Mali":                    "MLI",
    "Kenya":                   "KEN",
    "Tanzania":                "TAN",
    "Uganda":                  "UGA",
    "Zambia":                  "ZAM",
    "Uzbekistan":              "UZB",
    "Qatar":                   "QAT",
    "Iraq":                    "IRQ",
    "Turkey":                  "TUR",
    "Romania":                 "ROU",
    "Ukraine":                 "UKR",
    "Slovakia":                "SVK",
    "Czechia":                 "CZE",
    "Austria":                 "AUT",
    "Hungary":                 "HUN",
    "Albania":                 "ALB",
    "Scotland":                "SCO",
    "Wales":                   "WAL",
    "Greece":                  "GRE",
    "Denmark":                 "DEN",
    "Sweden":                  "SWE",
    "Norway":                  "NOR",
    "Finland":                 "FIN",
    "Iceland":                 "ISL",
    "Slovenia":                "SVN",
    "Costa Rica":              "CRC",
    "Jamaica":                 "JAM",
    "Trinidad and Tobago":     "TRI",
    "Guatemala":               "GUA",
    "Cuba":                    "CUB",
    "New Caledonia":           "NCL",
    "Tahiti":                  "TAH",
    "Fiji":                    "FIJ",
    "Solomon Islands":         "SOL",
    "Vanuatu":                 "VAN",
    "Indonesia":               "IDN",
    "Thailand":                "THA",
    "Vietnam":                 "VIE",
    "Philippines":             "PHI",
    "Malaysia":                "MAS",
    "Jordan":                  "JOR",
    "Bahrain":                 "BHR",
    "Oman":                    "OMA",
    "Kuwait":                  "KUW",
    "Palestine":               "PLE",
    "Syria":                   "SYR",
    "Bosnia and Herzegovina":  "BIH",
    "North Macedonia":         "MKD",
    "Kosovo":                  "KVX",
    "Israel":                  "ISR",
    "Azerbaijan":              "AZE",
    "Georgia":                 "GEO",
    "Armenia":                 "ARM",
    "Montenegro":              "MNE",
    "Luxembourg":              "LUX",
    "Malta":                   "MLT",
    "Andorra":                 "AND",
    "Russia":                  "RUS",
}

# Mapeo de nombre del grupo en el JSON → letra del grupo
# openfootball usa "Group A", "Group B", etc.
def extraer_grupo(group_str):
    """Extrae la letra del grupo desde 'Group A' → 'A'"""
    if not group_str:
        return None
    partes = group_str.strip().split()
    if len(partes) >= 2:
        return partes[-1].upper()
    return None


def parsear_fecha(date_str, time_str=None):
    """
    Convierte fecha/hora del JSON a datetime con timezone.
    El JSON usa formato: date="2026-06-11", time="13:00 UTC-6"
    Lo convertimos a UTC.
    """
    try:
        if time_str:
            # Extraer offset UTC si viene
            # Formato: "13:00 UTC-6" o "20:00 UTC+0"
            partes = time_str.strip().split()
            hora = partes[0]
            offset_horas = 0
            if len(partes) > 1 and 'UTC' in partes[1]:
                offset_str = partes[1].replace('UTC', '')
                if offset_str:
                    offset_horas = int(offset_str)
            dt_naive = datetime.strptime(f"{date_str} {hora}", "%Y-%m-%d %H:%M")
            # Ajustar el offset: si UTC-6, sumar 6 horas para llegar a UTC
            from datetime import timedelta
            dt_utc = dt_naive - timedelta(hours=offset_horas)
            return dt_utc.replace(tzinfo=dt_timezone.utc)
        else:
            dt_naive = datetime.strptime(date_str, "%Y-%m-%d")
            return dt_naive.replace(hour=12, tzinfo=dt_timezone.utc)
    except Exception:
        dt_naive = datetime.strptime(date_str, "%Y-%m-%d")
        return dt_naive.replace(hour=12, tzinfo=dt_timezone.utc)


class Command(BaseCommand):
    help = "Carga el fixture del Mundial 2026 desde openfootball/worldcup.json (sin API key)"

    def add_arguments(self, parser):
        parser.add_argument(
            '--limpiar',
            action='store_true',
            help='Elimina todos los equipos y partidos antes de cargar',
        )

    def handle(self, *args, **options):
        if options['limpiar']:
            self.stdout.write(self.style.WARNING("Limpiando datos existentes..."))
            Partido.objects.all().delete()
            Equipo.objects.all().delete()
            self.stdout.write(self.style.SUCCESS("  Datos eliminados."))

        # ── 1. Descargar JSON ──────────────────────────────────────────────
        self.stdout.write(f"\nDescargando fixture desde:\n  {URL_FIXTURE}\n")
        try:
            req = urllib.request.Request(
                URL_FIXTURE,
                headers={"User-Agent": "ProdeWorldCup/1.0"}
            )
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read().decode("utf-8"))
        except Exception as e:
            raise CommandError(f"Error al descargar el fixture: {e}")

        matches = data.get("matches", [])
        self.stdout.write(f"  {len(matches)} partidos encontrados en el JSON.\n")

        # ── 2. Extraer equipos únicos de fase de grupos ───────────────────
        equipos_vistos = {}  # nombre → Equipo

        partidos_grupos = [
            m for m in matches
            if m.get("group") and "Group" in m.get("group", "")
        ]

        self.stdout.write(f"  Partidos de fase de grupos: {len(partidos_grupos)}\n")

        for match in partidos_grupos:
            for key in ("team1", "team2"):
                nombre = match.get(key, "")
                if nombre and nombre not in equipos_vistos and "winner" not in nombre.lower() and "runner" not in nombre.lower():
                    grupo_letra = extraer_grupo(match.get("group", ""))
                    codigo = CODIGOS_FIFA.get(nombre, nombre[:3].upper())
                    equipo, creado = Equipo.objects.get_or_create(
                        codigo_fifa=codigo,
                        defaults={
                            "nombre": nombre,
                            "grupo": grupo_letra or "A",
                        }
                    )
                    if not creado:
                        # Actualizar grupo si cambió
                        if grupo_letra and equipo.grupo != grupo_letra:
                            equipo.grupo = grupo_letra
                            equipo.save()
                    equipos_vistos[nombre] = equipo
                    if creado:
                        self.stdout.write(f"  + Equipo: {nombre} ({codigo}) → Grupo {grupo_letra}")

        self.stdout.write(
            self.style.SUCCESS(f"\n  {len(equipos_vistos)} equipos cargados.\n")
        )

        # ── 3. Cargar partidos de fase de grupos ──────────────────────────
        partidos_cargados = 0
        partidos_omitidos = 0

        # Determinar jornada por ronda
        # openfootball usa "Matchday 1", "Matchday 2"... o "Round 1"
        def extraer_jornada(round_str):
            if not round_str:
                return 1
            round_str = round_str.lower()
            for num in ("1", "2", "3"):
                if num in round_str:
                    return int(num)
            return 1

        for match in partidos_grupos:
            nombre1 = match.get("team1", "")
            nombre2 = match.get("team2", "")

            # Saltear partidos con equipos TBD
            if (not nombre1 or not nombre2 or
                    nombre1 not in equipos_vistos or
                    nombre2 not in equipos_vistos):
                partidos_omitidos += 1
                continue

            equipo_local = equipos_vistos[nombre1]
            equipo_visitante = equipos_vistos[nombre2]
            grupo_letra = extraer_grupo(match.get("group", ""))
            jornada = extraer_jornada(match.get("round", ""))
            fecha_hora = parsear_fecha(
                match.get("date", "2026-06-11"),
                match.get("time")
            )
            estadio = match.get("ground", "")

            # Evitar duplicados
            if Partido.objects.filter(
                equipo_local=equipo_local,
                equipo_visitante=equipo_visitante,
                grupo=grupo_letra
            ).exists():
                partidos_omitidos += 1
                continue

            Partido.objects.create(
                equipo_local=equipo_local,
                equipo_visitante=equipo_visitante,
                fecha_hora=fecha_hora,
                jornada=jornada,
                grupo=grupo_letra or "A",
                estadio=estadio,
            )
            partidos_cargados += 1
            self.stdout.write(
                f"  + Partido Grupo {grupo_letra} J{jornada}: "
                f"{equipo_local.codigo_fifa} vs {equipo_visitante.codigo_fifa} "
                f"({fecha_hora.strftime('%Y-%m-%d %H:%M')} UTC)"
            )

        # ── 4. Resumen ────────────────────────────────────────────────────
        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS("═" * 50))
        self.stdout.write(self.style.SUCCESS("  FIXTURE CARGADO EXITOSAMENTE"))
        self.stdout.write(self.style.SUCCESS("═" * 50))
        self.stdout.write(f"  Equipos en DB:    {Equipo.objects.count()}")
        self.stdout.write(f"  Partidos cargados: {partidos_cargados}")
        self.stdout.write(f"  Partidos omitidos: {partidos_omitidos} (TBD o duplicados)")
        self.stdout.write("")
        self.stdout.write("  Podés verificar en: http://127.0.0.1:8000/admin")
        self.stdout.write("  Y en: http://127.0.0.1:8000/api/fixture/grupos/")
        self.stdout.write("")
