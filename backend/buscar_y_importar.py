import os
import django
import requests
from bs4 import BeautifulSoup

# Configura el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.fixture.models import Jugador, Equipo

# Lista de prueba con nombres exactos de estrellas
JUGADORES_A_BUSCAR = [
    {"nombre_busqueda": "Lionel Messi", "equipo": "Argentina"},
    {"nombre_busqueda": "Kylian Mbappe", "equipo": "Francia"},
    {"nombre_busqueda": "Erling Haaland", "equipo": "Noruega"},
    {"nombre_busqueda": "Jude Bellingham", "equipo": "Inglaterra"},
    {"nombre_busqueda": "Lamine Yamal", "equipo": "España"},
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def buscar_en_transfermarkt(nombre_jugador):
    url_busqueda = f"https://www.transfermarkt.com/schnellsuche/ergebnis/schnellsuche?query={nombre_jugador.replace(' ', '+')}"
    print(f"Buscando a {nombre_jugador} en Transfermarkt...")
    
    try:
        response = requests.get(url_busqueda, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Transfermarkt es complejo, este selector intenta buscar la tabla de resultados principales
        tabla_resultados = soup.find('table', class_='items')
        
        if tabla_resultados:
            # Buscamos la primera fila de resultados que parece ser el jugador
            fila_jugador = tabla_resultados.find('a', class_='spielprofil_tooltip')
            
            if fila_jugador:
                link_jugador = "https://www.transfermarkt.com" + fila_jugador['href']
                print(f"✅ ¡Jugador encontrado! {link_jugador}")
                return link_jugador
        
    except Exception as e:
        print(f"❌ Error buscando a {nombre_jugador}: {e}")
    
    print(f"❌ No se encontró link para {nombre_jugador}")
    return None

def importar_con_link():
    print(f"Iniciando importación inteligente de {len(JUGADORES_A_BUSCAR)} jugadores...")

    for data in JUGADORES_A_BUSCAR:
        link_tm = buscar_en_transfermarkt(data['nombre_busqueda'])
        
        if link_tm:
            # Buscamos o creamos el equipo
            equipo, _ = Equipo.objects.get_or_create(nombre=data['equipo'])

            # Crear o actualizar el jugador, usando el link como id_externo (temporalmente)
            jugador, creado = Jugador.objects.update_or_create(
                nombre=data['nombre_busqueda'],
                equipo=equipo,
                defaults={
                    'posicion': 'DEL', # Por defecto para la prueba
                    'edad': 25,       # Por defecto para la prueba
                    # ¡AQUÍ ESTÁ LA MAGIA! Guardamos el link entero
                    'id_externo': link_tm # Si tu campo es CharField. Si es IntegerField, no funcionará.
                }
            )
            
            status = "Creado" if creado else "Actualizado"
            print(f"[{status}] {jugador.nombre} (con link)")

    print("\n✅ ¡Importación inteligente finalizada con éxito!")

if __name__ == '__main__':
    # Esta solución requiere que tu campo id_externo en Django sea un CharField para guardar el link.
    # Si es un IntegerField, tendríamos que extraer el ID del link.
    importar_con_link()