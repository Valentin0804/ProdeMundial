"""
Fixture completo Mundial 2026 - 48 equipos, 72 partidos confirmados.
Uso: python manage.py cargar_fixture [--limpiar]
"""
from django.core.management.base import BaseCommand
from datetime import datetime, timezone as dt_timezone
from apps.fixture.models import Equipo, Partido

EQUIPOS = [
    ("México","MEX","mx","A","CONCACAF"),
    ("Sudáfrica","RSA","za","A","CAF"),
    ("Corea del Sur","KOR","kr","A","AFC"),
    ("Rep. Checa","CZE","cz","A","UEFA"),
    ("Canadá","CAN","ca","B","CONCACAF"),
    ("Suiza","SUI","ch","B","UEFA"),
    ("Qatar","QAT","qa","B","AFC"),
    ("Bosnia-Herz.","BIH","ba","B","UEFA"),
    ("Brasil","BRA","br","C","CONMEBOL"),
    ("Marruecos","MAR","ma","C","CAF"),
    ("Escocia","SCO","gb-sct","C","UEFA"),
    ("Haití","HAI","ht","C","CONCACAF"),
    ("Estados Unidos","USA","us","D","CONCACAF"),
    ("Australia","AUS","au","D","AFC"),
    ("Paraguay","PAR","py","D","CONMEBOL"),
    ("Turquía","TUR","tr","D","UEFA"),
    ("Alemania","GER","de","E","UEFA"),
    ("Costa de Marfil","CIV","ci","E","CAF"),
    ("Ecuador","ECU","ec","E","CONMEBOL"),
    ("Curazao","CUW","cu","E","CONCACAF"),
    ("Países Bajos","NED","nl","F","UEFA"),
    ("Japón","JPN","jp","F","AFC"),
    ("Túnez","TUN","tn","F","CAF"),
    ("Suecia","SWE","se","F","UEFA"),
    ("Bélgica","BEL","be","G","UEFA"),
    ("Irán","IRN","ir","G","AFC"),
    ("Egipto","EGY","eg","G","CAF"),
    ("Nueva Zelanda","NZL","nz","G","OFC"),
    ("España","ESP","es","H","UEFA"),
    ("Cabo Verde","CPV","cv","H","CAF"),
    ("Arabia Saudita","KSA","sa","H","AFC"),
    ("Uruguay","URU","uy","H","CONMEBOL"),
    ("Francia","FRA","fr","I","UEFA"),
    ("Senegal","SEN","sn","I","CAF"),
    ("Noruega","NOR","no","I","UEFA"),
    ("Irak","IRQ","iq","I","AFC"),
    ("Argentina","ARG","ar","J","CONMEBOL"),
    ("Argelia","ALG","dz","J","CAF"),
    ("Austria","AUT","at","J","UEFA"),
    ("Jordania","JOR","jo","J","AFC"),
    ("Portugal","POR","pt","K","UEFA"),
    ("Uzbekistán","UZB","uz","K","AFC"),
    ("Colombia","COL","co","K","CONMEBOL"),
    ("RD del Congo","COD","cd","K","CAF"),
    ("Inglaterra","ENG","gb-eng","L","UEFA"),
    ("Croacia","CRO","hr","L","UEFA"),
    ("Ghana","GHA","gh","L","CAF"),
    ("Panamá","PAN","pa","L","CONCACAF"),
]

# (local, visitante, grupo, jornada, fecha_UTC, estadio, ciudad)
PARTIDOS = [
    # Jornada 1
    ("MEX","RSA","A",1,"2026-06-11 20:00","Estadio Azteca","Ciudad de México"),
    ("KOR","CZE","A",1,"2026-06-12 03:00","Estadio Akron","Guadalajara"),
    ("CAN","QAT","B",1,"2026-06-13 01:00","BC Place","Vancouver"),
    ("SUI","BIH","B",1,"2026-06-12 20:00","SoFi Stadium","Los Ángeles"),
    ("BRA","MAR","C",1,"2026-06-13 20:00","MetLife Stadium","Nueva York/NJ"),
    ("SCO","HAI","C",1,"2026-06-14 00:00","AT&T Stadium","Dallas"),
    ("USA","AUS","D",1,"2026-06-14 20:00","SoFi Stadium","Los Ángeles"),
    ("PAR","TUR","D",1,"2026-06-15 04:00","Levi's Stadium","San Francisco"),
    ("GER","CUW","E",1,"2026-06-14 18:00","NRG Stadium","Houston"),
    ("CIV","ECU","E",1,"2026-06-15 00:00","Lincoln Financial","Filadelfia"),
    ("NED","SWE","F",1,"2026-06-20 18:00","NRG Stadium","Houston"),
    ("TUN","JPN","F",1,"2026-06-21 03:00","Estadio BBVA","Monterrey"),
    ("BEL","EGY","G",1,"2026-06-15 20:00","Lumen Field","Seattle"),
    ("IRN","NZL","G",1,"2026-06-16 02:00","SoFi Stadium","Los Ángeles"),
    ("ESP","CPV","H",1,"2026-06-16 20:00","Hard Rock Stadium","Miami"),
    ("KSA","URU","H",1,"2026-06-16 23:00","Hard Rock Stadium","Miami"),
    ("FRA","SEN","I",1,"2026-06-15 20:00","MetLife Stadium","Nueva York/NJ"),
    ("NOR","IRQ","I",1,"2026-06-15 23:00","Gillette Stadium","Boston"),
    ("ARG","ALG","J",1,"2026-06-15 02:00","Arrowhead Stadium","Kansas City"),
    ("AUT","JOR","J",1,"2026-06-16 04:00","Levi's Stadium","San Francisco"),
    ("POR","COD","K",1,"2026-06-17 18:00","NRG Stadium","Houston"),
    ("UZB","COL","K",1,"2026-06-18 03:00","Estadio Azteca","Ciudad de México"),
    ("ENG","CRO","L",1,"2026-06-17 21:00","AT&T Stadium","Dallas"),
    ("GHA","PAN","L",1,"2026-06-18 00:00","BMO Field","Toronto"),
    # Jornada 2
    ("CZE","RSA","A",2,"2026-06-18 17:00","Mercedes-Benz Stadium","Atlanta"),
    ("MEX","KOR","A",2,"2026-06-19 02:00","Estadio Akron","Guadalajara"),
    ("SUI","CAN","B",2,"2026-06-19 20:00","SoFi Stadium","Los Ángeles"),
    ("QAT","BIH","B",2,"2026-06-20 00:00","BC Place","Vancouver"),
    ("BRA","SCO","C",2,"2026-06-19 00:00","AT&T Stadium","Dallas"),
    ("MAR","HAI","C",2,"2026-06-20 00:00","Lincoln Financial","Filadelfia"),
    ("TUR","USA","D",2,"2026-06-19 21:00","Levi's Stadium","San Francisco"),
    ("AUS","PAR","D",2,"2026-06-20 03:00","Levi's Stadium","San Francisco"),
    ("GER","CIV","E",2,"2026-06-20 21:00","BMO Field","Toronto"),
    ("ECU","CUW","E",2,"2026-06-21 01:00","Arrowhead Stadium","Kansas City"),
    ("JPN","SWE","F",2,"2026-06-25 22:00","AT&T Stadium","Dallas"),
    ("TUN","NED","F",2,"2026-06-26 00:00","Arrowhead Stadium","Kansas City"),
    ("BEL","IRN","G",2,"2026-06-21 20:00","Lumen Field","Seattle"),
    ("EGY","NZL","G",2,"2026-06-22 00:00","Gillette Stadium","Boston"),
    ("ESP","KSA","H",2,"2026-06-22 20:00","Estadio Akron","Guadalajara"),
    ("CPV","URU","H",2,"2026-06-23 00:00","Estadio Akron","Guadalajara"),
    ("FRA","NOR","I",2,"2026-06-21 00:00","MetLife Stadium","Nueva York/NJ"),
    ("SEN","IRQ","I",2,"2026-06-22 02:00","Gillette Stadium","Boston"),
    ("ARG","AUT","J",2,"2026-06-22 03:00","Levi's Stadium","San Francisco"),
    ("ALG","JOR","J",2,"2026-06-23 04:00","Levi's Stadium","San Francisco"),
    ("POR","UZB","K",2,"2026-06-23 18:00","NRG Stadium","Houston"),
    ("COD","COL","K",2,"2026-06-24 03:00","Estadio Akron","Guadalajara"),
    ("ENG","GHA","L",2,"2026-06-23 21:00","Gillette Stadium","Boston"),
    ("PAN","CRO","L",2,"2026-06-24 00:00","BMO Field","Toronto"),
    # Jornada 3
    ("CZE","MEX","A",3,"2026-06-25 02:00","Estadio Azteca","Ciudad de México"),
    ("RSA","KOR","A",3,"2026-06-25 02:00","Estadio BBVA","Monterrey"),
    ("SUI","QAT","B",3,"2026-06-25 22:00","SoFi Stadium","Los Ángeles"),
    ("CAN","BIH","B",3,"2026-06-25 22:00","BC Place","Vancouver"),
    ("BRA","HAI","C",3,"2026-06-26 02:00","MetLife Stadium","Nueva York/NJ"),
    ("MAR","SCO","C",3,"2026-06-26 02:00","Lincoln Financial","Filadelfia"),
    ("USA","PAR","D",3,"2026-06-26 22:00","SoFi Stadium","Los Ángeles"),
    ("TUR","AUS","D",3,"2026-06-26 22:00","Levi's Stadium","San Francisco"),
    ("ECU","GER","E",3,"2026-06-26 21:00","MetLife Stadium","Nueva York/NJ"),
    ("CUW","CIV","E",3,"2026-06-26 21:00","Lincoln Financial","Filadelfia"),
    ("JPN","TUN","F",3,"2026-06-26 22:00","AT&T Stadium","Dallas"),
    ("SWE","NED","F",3,"2026-06-26 22:00","Arrowhead Stadium","Kansas City"),
    ("BEL","NZL","G",3,"2026-06-27 02:00","Lumen Field","Seattle"),
    ("EGY","IRN","G",3,"2026-06-27 02:00","Gillette Stadium","Boston"),
    ("ESP","URU","H",3,"2026-06-28 01:00","Estadio Akron","Guadalajara"),
    ("CPV","KSA","H",3,"2026-06-28 01:00","Hard Rock Stadium","Miami"),
    ("FRA","IRQ","I",3,"2026-06-27 22:00","MetLife Stadium","Nueva York/NJ"),
    ("SEN","NOR","I",3,"2026-06-27 22:00","Gillette Stadium","Boston"),
    ("ARG","JOR","J",3,"2026-06-28 03:00","AT&T Stadium","Dallas"),
    ("ALG","AUT","J",3,"2026-06-28 03:00","Arrowhead Stadium","Kansas City"),
    ("COL","POR","K",3,"2026-06-28 00:30","Hard Rock Stadium","Miami"),
    ("COD","UZB","K",3,"2026-06-28 00:30","Mercedes-Benz Stadium","Atlanta"),
    ("PAN","ENG","L",3,"2026-06-28 22:00","MetLife Stadium","Nueva York/NJ"),
    ("CRO","GHA","L",3,"2026-06-28 22:00","Lincoln Financial","Filadelfia"),
]

def dt_utc(s):
    return datetime.strptime(s, "%Y-%m-%d %H:%M").replace(tzinfo=dt_timezone.utc)

class Command(BaseCommand):
    help = "Carga el fixture completo del Mundial 2026 (48 equipos, 72 partidos)"

    def add_arguments(self, parser):
        parser.add_argument('--limpiar', action='store_true')

    def handle(self, *args, **options):
        if options['limpiar']:
            self.stdout.write(self.style.WARNING("Limpiando..."))
            Partido.objects.all().delete()
            Equipo.objects.all().delete()

        # Equipos
        em = {}
        creados_e = 0
        for nombre, codigo, iso, grupo, conf in EQUIPOS:
            obj, nuevo = Equipo.objects.get_or_create(
                codigo_fifa=codigo,
                defaults={"nombre": nombre, "grupo": grupo, "confederacion": conf, "codigo_iso": iso}
            )
            if not nuevo:
                obj.nombre = nombre; obj.grupo = grupo; obj.save()
            else:
                creados_e += 1
            em[codigo] = obj

        self.stdout.write(self.style.SUCCESS(f"Equipos: {Equipo.objects.count()}/48 ({creados_e} nuevos)"))

        # Partidos
        creados_p = 0
        for local_c, visit_c, grupo, jornada, fecha, estadio, ciudad in PARTIDOS:
            _, nuevo = Partido.objects.get_or_create(
                equipo_local=em[local_c], equipo_visitante=em[visit_c], grupo=grupo,
                defaults={"jornada": jornada, "fecha_hora": dt_utc(fecha), "estadio": estadio, "ciudad": ciudad}
            )
            if nuevo: creados_p += 1

        self.stdout.write(self.style.SUCCESS(f"Partidos: {Partido.objects.count()}/72 ({creados_p} nuevos)"))
        self.stdout.write(self.style.SUCCESS("✓ Fixture cargado. Verificá en /api/fixture/grupos/"))