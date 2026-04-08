import os
import requests
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.fixture.models import Jugador

def descargar():
    jugadores = Jugador.objects.exclude(id_externo__isnull=True).exclude(id_externo='')
    print(f"DEBUG: Se encontraron {jugadores.count()} jugadores.")

    ruta_media = os.path.join('media', 'jugadores')
    if not os.path.exists(ruta_media):
        os.makedirs(ruta_media, exist_ok=True)

    # NUEVA URL DE EA FC 25 (MUY ESTABLE)
    # Ejemplo para Messi (158023): https://ratings-images-prod.asindcontent.g9g.it/F25/full/player-portraits/158023.png
    # Si ese falla, usamos esta alternativa de respaldo:
    
    for j in jugadores:
        # Intentamos la versión FC25 primero
        url = f"https://www.ea.com/ea-sports-fc/ultimate-team/web-app/content/25C73J91/2025/fut/items/images/mobile/portraits/{j.id_externo}.png"
        
        nombre_archivo = f"{j.id_externo}.png"
        ruta_archivo = os.path.join(ruta_media, nombre_archivo)

        print(f"Descargando foto de {j.nombre}...", end=" ")
        try:
            # Headers mínimos para que no nos bloqueen
            headers = {'User-Agent': 'Mozilla/5.0'}
            res = requests.get(url, headers=headers, timeout=10)
            
            if res.status_code == 200:
                with open(ruta_archivo, 'wb') as f:
                    f.write(res.content)
                j.foto = f"jugadores/{nombre_archivo}"
                j.save()
                print("✅")
            else:
                # PLAN C: Si EA falla, usamos una API de renders genérica que no muere nunca
                url_respaldo = f"https://media.api-sports.io/football/players/{j.id_externo}.png"
                res_resp = requests.get(url_respaldo, headers=headers, timeout=5)
                if res_resp.status_code == 200:
                    with open(ruta_archivo, 'wb') as f:
                        f.write(res_resp.content)
                    j.foto = f"jugadores/{nombre_archivo}"
                    j.save()
                    print("✅ (Respaldo)")
                else:
                    print(f"❌ Error {res.status_code}")
                
        except Exception as e:
            print(f"🔥 Error: {e}")

if __name__ == '__main__':
    descargar()