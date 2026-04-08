import os
import json
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.fixture.models import Jugador, Equipo

def importar():
    ruta_json = 'jugadores.json'
    
    with open(ruta_json, 'r', encoding='utf-8') as f:
        datos = json.load(f)

    # Si el JSON es un diccionario con una clave 'jugadores', usamos esa lista
    # Si es directamente una lista, usamos 'datos'
    lista_jugadores = datos['jugadores'] if isinstance(datos, dict) and 'jugadores' in datos else datos

    if not isinstance(lista_jugadores, list):
        print("❌ Error: El formato del JSON no es una lista.")
        return

    print(f"Iniciando importación de {len(lista_jugadores)} jugadores...")

    for data in lista_jugadores:
        try:
            # Buscamos o creamos el equipo
            # Nota: Si tu modelo Equipo requiere otros campos obligatorios (como codigo_fifa), 
            # agregalos en defaults.
            equipo, _ = Equipo.objects.get_or_create(
                nombre=data['equipo']
            )

            # Creamos o actualizamos el jugador
            jugador, creado = Jugador.objects.update_or_create(
                nombre=data['nombre'],
                equipo=equipo,
                defaults={
                    'posicion': data.get('posicion', 'DEL'),
                    'edad': data.get('edad'),
                    'id_externo': data.get('id_externo')
                }
            )
            
            print(f"✅ {'Creado' if creado else 'Actualizado'}: {jugador.nombre}")

        except Exception as e:
            print(f"⚠️ Error procesando a {data}: {e}")

if __name__ == '__main__':
    importar()